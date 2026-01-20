"""
WOS Artifact Publisher v0.1
Centralized utility for publishing agent artifacts to filesystem + Canon
Sprint 1 foundational infrastructure
"""

import os
import logging
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger("wos.artifact_publisher")


class ArtifactPublisher:
    """
    Artifact Publisher

    Provides consistent artifact handling for all WOS agents:
    - Writes markdown files to /artifacts/<category>/<filename>.md
    - Records artifact_uri in Canon Index
    - Optional git commit

    Used by ALL agents to prevent inconsistent file handling.
    """

    def __init__(self, repo_root: str, canon_tools=None, git_enabled: bool = True):
        """
        Initialize Artifact Publisher

        Args:
            repo_root: Path to WOS repository root
            canon_tools: CanonTools instance (optional, for Canon integration)
            git_enabled: Enable git commits (default True)
        """
        self.repo_root = Path(repo_root)
        self.artifacts_dir = self.repo_root / "artifacts"
        self.canon_tools = canon_tools
        self.git_enabled = git_enabled

        # Ensure artifacts directory exists
        self.artifacts_dir.mkdir(exist_ok=True)
        logger.info(f"Artifact Publisher initialized: {self.artifacts_dir}")

    def publish_artifact(
        self,
        markdown: str,
        category: str,
        filename: str,
        artifact_id: str = None,
        title: str = None,
        artifact_type: str = "agent_output",
        summary: str = None,
        tags: list = None,
        metadata: Dict[str, Any] = None,
        git_commit: bool = True,
        commit_message: str = None
    ) -> Dict[str, Any]:
        """
        Publish an artifact

        Args:
            markdown: Markdown content to write
            category: Category folder (e.g., "support", "incidents", "feedback")
            filename: Filename (e.g., "triage-2026-01-19.md")
            artifact_id: Unique ID for Canon (auto-generated if not provided)
            title: Human-readable title for Canon
            artifact_type: Type for Canon ("agent_output", "decision", "log", etc.)
            summary: Brief summary for Canon search
            tags: List of tags for Canon
            metadata: Additional metadata for Canon
            git_commit: Whether to git commit (default True, overrides instance setting)
            commit_message: Custom commit message (optional)

        Returns:
        {
            "success": bool,
            "artifact_path": str,
            "artifact_uri": str,
            "canon_stored": bool,
            "git_committed": bool,
            "error": str (if failed)
        }
        """

        try:
            # Step 1: Write markdown file
            category_dir = self.artifacts_dir / category
            category_dir.mkdir(exist_ok=True)

            artifact_path = category_dir / filename

            with open(artifact_path, 'w') as f:
                f.write(markdown)

            logger.info(f"Artifact written: {artifact_path}")

            # Generate artifact URI (relative path from repo root)
            artifact_uri = f"artifacts/{category}/{filename}"

            # Step 2: Record in Canon (if canon_tools provided)
            canon_stored = False
            if self.canon_tools:
                # Auto-generate artifact_id if not provided
                if not artifact_id:
                    artifact_id = f"{category}_{filename.replace('.md', '')}".replace('-', '_')

                # Auto-generate title if not provided
                if not title:
                    title = f"{category.title()} - {filename.replace('.md', '')}"

                # Auto-generate summary if not provided
                if not summary:
                    # Use first 200 chars of markdown as summary
                    summary = markdown[:200].replace('\n', ' ').strip() + "..."

                # Store in Canon with artifact_uri in metadata
                canon_metadata = metadata or {}
                canon_metadata["artifact_uri"] = artifact_uri
                canon_metadata["published_at"] = datetime.utcnow().isoformat()

                canon_stored = self.canon_tools.store(
                    artifact_id=artifact_id,
                    title=title,
                    content=markdown,
                    artifact_type=artifact_type,
                    category=category,
                    summary=summary,
                    source="artifact_publisher",
                    source_url=artifact_uri,
                    tags=tags,
                    metadata=canon_metadata,
                    auto_embed=True
                )

                if canon_stored:
                    logger.info(f"Artifact stored in Canon: {artifact_id}")
                else:
                    logger.warning(f"Failed to store artifact in Canon: {artifact_id}")

            # Step 3: Git commit (if enabled)
            git_committed = False
            should_commit = git_commit and self.git_enabled

            if should_commit:
                try:
                    # Auto-generate commit message if not provided
                    if not commit_message:
                        commit_message = f"Add artifact: {category}/{filename}\n\nPublished by WOS Artifact Publisher"

                    # Add file to git
                    subprocess.run(
                        ['git', 'add', str(artifact_path)],
                        cwd=self.repo_root,
                        check=True,
                        capture_output=True
                    )

                    # Commit
                    subprocess.run(
                        ['git', 'commit', '-m', commit_message],
                        cwd=self.repo_root,
                        check=True,
                        capture_output=True
                    )

                    git_committed = True
                    logger.info(f"Artifact committed to git: {artifact_uri}")

                except subprocess.CalledProcessError as e:
                    logger.warning(f"Git commit failed: {e}")
                    # Don't fail the whole operation if git fails

            return {
                "success": True,
                "artifact_path": str(artifact_path),
                "artifact_uri": artifact_uri,
                "canon_stored": canon_stored,
                "git_committed": git_committed,
                "error": None
            }

        except Exception as e:
            logger.error(f"Artifact publishing failed: {e}", exc_info=True)
            return {
                "success": False,
                "artifact_path": None,
                "artifact_uri": None,
                "canon_stored": False,
                "git_committed": False,
                "error": str(e)
            }

    def publish_daily_artifact(
        self,
        markdown: str,
        category: str,
        prefix: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Convenience method for daily artifacts

        Auto-generates filename with today's date: <prefix>-YYYY-MM-DD.md

        Args:
            markdown: Markdown content
            category: Category folder
            prefix: Filename prefix (e.g., "triage", "dashboard")
            **kwargs: Additional arguments passed to publish_artifact()

        Returns: Same as publish_artifact()
        """
        today = datetime.utcnow().strftime("%Y-%m-%d")
        filename = f"{prefix}-{today}.md"

        return self.publish_artifact(
            markdown=markdown,
            category=category,
            filename=filename,
            **kwargs
        )

    def publish_weekly_artifact(
        self,
        markdown: str,
        category: str,
        prefix: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Convenience method for weekly artifacts

        Auto-generates filename with week number: <prefix>-YYYY-WW.md

        Args:
            markdown: Markdown content
            category: Category folder
            prefix: Filename prefix (e.g., "exec-dashboard")
            **kwargs: Additional arguments passed to publish_artifact()

        Returns: Same as publish_artifact()
        """
        # ISO week format: YYYY-WW
        week_id = datetime.utcnow().strftime("%Y-W%W")
        filename = f"{prefix}-{week_id}.md"

        return self.publish_artifact(
            markdown=markdown,
            category=category,
            filename=filename,
            **kwargs
        )


# Factory function
def create_artifact_publisher(repo_root: str = None, canon_tools=None, git_enabled: bool = True) -> ArtifactPublisher:
    """
    Factory function to create ArtifactPublisher

    Args:
        repo_root: Path to WOS repository (auto-detected if None)
        canon_tools: CanonTools instance (optional)
        git_enabled: Enable git commits
    """
    if not repo_root:
        # Auto-detect repo root (look for .git directory)
        current = Path.cwd()
        while current != current.parent:
            if (current / '.git').exists():
                repo_root = str(current)
                break
            current = current.parent

        if not repo_root:
            raise ValueError("Could not auto-detect git repository root. Please provide repo_root.")

    return ArtifactPublisher(
        repo_root=repo_root,
        canon_tools=canon_tools,
        git_enabled=git_enabled
    )
