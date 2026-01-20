# WOS Development Backlog

**Last Updated:** January 20, 2026

Items tracked here are also in Notion tasks-masterlist with Context: "Backlog"

---

## Integrations - Social Media Auto-Send

**Priority:** Post-launch (after manual outreach validates messaging)
**Effort:** 2-3 hours per platform
**Added:** Jan 20, 2026

- [ ] Set up Facebook Graph API for auto-DM sending
  - Requires: App review, business verification, DM write permissions
  - Benefit: Auto-send approved Facebook DMs instead of copy-paste

- [ ] Set up Instagram Graph API for auto-DM sending
  - Requires: App review, Instagram Business Account, permissions
  - Benefit: Auto-send approved Instagram DMs

- [ ] Set up LinkedIn API for messaging
  - Requires: LinkedIn App, messaging permissions
  - Benefit: Auto-send approved LinkedIn messages

- [ ] Set up Twitter API v2 for DMs
  - Requires: Twitter API v2 access, DM write permissions
  - Benefit: Auto-send approved Twitter DMs

**Note:** User has business accounts already. Manual copy-paste works fine for now.

---

## Infrastructure - Third-Party Decisions

**Priority:** Before Sprint 2
**Blocked by:** Dev team input needed
**Added:** Jan 20, 2026

- [ ] Decide on crash monitoring platform
  - Options: Sentry vs Firebase Crashlytics
  - Action: Ask dev team which they prefer/use

- [ ] Decide on ticketing system
  - Options: Linear vs Zendesk vs Help Scout
  - Action: Ask dev team for preference
  - Needed for: Support Triage agent (Sprint 2)

- [ ] Get Mixpanel API key
  - Needed for: Activation Funnel Radar agent (Sprint 4)

---

## Agents - Template Improvements

**Priority:** Before launch outreach
**Effort:** 30 minutes
**Added:** Jan 20, 2026

- [ ] Fix Creator Outreach template selection logic
  - Issue: Prioritizes email existence over Contact Method field
  - Should: Use Contact Method field to determine DM vs Email template
  - Impact: DM contacts get wrong (formal) template if they have email

- [ ] Update outreach message templates for launch
  - Current: Placeholder pre-launch messaging
  - Needed: Final launch messaging when app goes live
  - User wants short DM format referencing original post

---

## How to Use This File

**Adding items:**
- Run: `python3 add_to_backlog.py "Your task description"`
- Adds to this file + creates Notion task

**Completing items:**
- Mark as done in Notion
- Delete the completed section from this file
- Commit the update

**Reviewing:**
- Check this file at session start
- Pick what to work on
- Items stay here until completed or cancelled
