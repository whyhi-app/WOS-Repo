# COS Setup Documentation

**Created:** January 21, 2026
**Purpose:** Configuration reference for Content Operating System (COS)

---

## Notion Configuration

### Existing Databases

#### Content & Creator Capture
**Database ID:** `23d632f5307e8001a1d6fb31be92d59e`
**Purpose:** Unified database for capturing both content ideas and creator profiles
**Current Schema (Before COS):**
- Name (Title)
- Platform (Select)
- URL (URL)
- Contact Method (Select)
- Outreach Status (Select)
- Sending Email (Email)

**COS Enhancements (Phase 1, Day 2):**
- Action Type (Multi-select) - Values: "💡 Content Ideation", "🤝 Outreach"
- Topic Tags (Multi-select) - Values: TBD (Loneliness, Telephobia, Connection, etc.)
- Relevance Score (Number) - 1-5 rating
- Content Notes (Text) - User's observations about captured content
- Ideation Status (Select) - Values: "New", "Sent to COS", "Ideas Generated"
- Generated Ideas (Relation) → Content Ideas Queue
- Related Drafts (Relation) → Drafts for Review

---

### New Databases (To Be Created)

#### Content Ideas Queue
**Database ID:** `dae2c9d9-83ce-46b4-be71-f057c0dc5230`
**Purpose:** Store AI-generated content ideas from Content Idea Miner
**Schema:**
- Title (Title) - Idea headline
- Idea Description (Text) - Full idea explanation
- Status (Select) - Values: "Proposed", "Approved", "Rejected", "Done"
- Platform (Select) - Values: "LinkedIn", "Facebook", "Instagram", "All"
- Content Type (Select) - Values: "Social Post", "Video", "Blog Post"
- Use Case Reference (Text) - Which use case this relates to
- Formula Used (Select) - Which writing formula: "Use Case Spotlight", "Hidden Cost", etc.
- Source Content (Relation) → Content & Creator Capture
- Generated Draft (Relation) → Drafts for Review
- Notes (Text) - Tom's feedback or adjustments

**Views:**
- Proposed (filter: Status = "Proposed")
- Approved (filter: Status = "Approved")
- Done (filter: Status = "Done")

---

#### Drafts for Review
**Database ID:** `c38b205a-31d2-4499-9cba-bb3b59af5a4e`
**Purpose:** Store AI-generated content drafts from Content Drafter
**Schema:**
- Title (Title) - Draft headline/hook
- Status (Select) - Values: "Draft", "Needs Revision", "Approved", "Scheduled"
- Content Type (Select) - Values: "Social Post", "Social Video", "Instructional Video"
- Platform (Select) - Values: "LinkedIn", "Facebook", "Instagram", "All Platforms"
- LinkedIn Content (Text) - Platform-specific version
- Facebook Content (Text) - Platform-specific version
- Instagram Content (Text) - Platform-specific version
- Video Script (Text) - For video content types
- Storyboard Notes (Text) - Visual direction for videos
- Image Suggestions (Text) - AI-suggested Unsplash/Pexels images
- Source Idea (Relation) → Content Ideas Queue
- Scheduled Post (Relation) → Content Calendar
- Created Date (Date) - Auto-populated
- Last Edited (Date) - Auto-populated
- Notes (Text) - Tom's edits or feedback

**Views:**
- By Status (group by Status)
- By Platform (group by Platform)
- By Content Type (group by Content Type)

---

#### Content Calendar
**Database ID:** `ceaf6b8a-1d36-4b60-92c0-87155c3a47b7`
**Purpose:** Track scheduled and posted content with engagement metrics
**Schema:**
- Title (Title) - Post headline
- Scheduled Date (Date) - When post will publish
- Status (Select) - Values: "Scheduled", "Posted", "Failed"
- Platform (Select) - Values: "LinkedIn", "Facebook", "Instagram"
- Content Type (Select) - Values: "Social Post", "Video"
- Buffer Post ID (Text) - Reference to Buffer scheduled post
- Post URL (URL) - Published post link (once live)
- Likes (Number) - Engagement metric
- Comments (Number) - Engagement metric
- Shares (Number) - Engagement metric
- Reach (Number) - Engagement metric
- Source Draft (Relation) → Drafts for Review
- Notes (Text) - Performance observations

**Views:**
- Calendar View (timeline by Scheduled Date)
- Platform Performance (group by Platform, show metrics)
- This Week (filter: Scheduled Date within current week)

---

## n8n Workflows

### Existing Workflows (To Be Updated)

#### content_capture
**Purpose:** Capture content/creator URLs from iOS share sheet
**Trigger:** Webhook (iOS Shortcuts integration)
**Current Behavior:**
- Receives URL + optional notes
- Extracts platform, handle, creator name from URL
- Creates entry in Content & Creator Capture database

**COS Enhancement (Phase 1, Day 2):**
- Add new fields to Notion API node:
  - Action Type: Leave empty (user triages manually)
  - Topic Tags: Leave empty
  - Relevance Score: Leave empty
  - Content Notes: Use user's submitted notes
  - Ideation Status: Set to "New"

---

### New Workflows (To Be Created)

#### ideation_trigger (Phase 2, Day 4)
**Purpose:** Poll Notion for content marked "Sent to COS", generate ideas
**Trigger:** Cron (every 5 minutes)
**Flow:**
1. Poll Content & Creator Capture database
2. Filter: Action Type contains "💡 Content Ideation" AND Ideation Status = "Sent to COS"
3. For each entry:
   - Read Canon (Brand Foundation, Content Playbook)
   - Call Content Idea Miner agent (via Claude API)
   - Create 2-5 ideas in Content Ideas Queue
   - Update source entry: Ideation Status = "Ideas Generated"
   - Link ideas to source via "Generated Ideas" relation

---

#### drafting_trigger (Phase 3, Days 6-7)
**Purpose:** Poll Notion for approved ideas, generate drafts
**Trigger:** Cron (every 5 minutes)
**Flow:**
1. Poll Content Ideas Queue database
2. Filter: Status = "Approved"
3. For each approved idea:
   - Read Canon (Brand Foundation, Content Playbook, Founder Voice Profile)
   - Call Content Drafter agent (via Claude API)
   - Create entry in Drafts for Review with platform-specific content
   - Update idea status: "Done"
   - Link draft to idea via "Generated Draft" relation

---

#### buffer_scheduling (Phase 4, Day 8-9)
**Purpose:** Schedule approved drafts in Buffer
**Trigger:** Cron (every 5 minutes)
**Flow:**
1. Poll Drafts for Review database
2. Filter: Status = "Approved" AND Content Type = "Social Post"
3. For each approved draft:
   - For each platform (LinkedIn, Facebook, Instagram):
     - Call Buffer API to schedule post
     - Use platform-specific content variant
   - Create entry in Content Calendar
   - Store Buffer Post ID
   - Update draft status: "Scheduled"
   - Link calendar entry to draft via "Scheduled Post" relation

---

#### engagement_tracking (Phase 4, Day 9)
**Purpose:** Pull engagement metrics from Buffer, update Content Calendar
**Trigger:** Cron (daily at 9:00 AM PST)
**Flow:**
1. Query Content Calendar for posted items (last 7 days)
2. For each post:
   - Call Buffer API to get analytics (Buffer Post ID)
   - Update Content Calendar with metrics: Likes, Comments, Shares, Reach

---

#### outreach_trigger (Phase 5, Day 10 - Optional)
**Purpose:** Generate creator outreach messages
**Trigger:** Cron (every 15 minutes)
**Flow:**
1. Poll Content & Creator Capture database
2. Filter: Action Type contains "🤝 Outreach" AND Outreach Status = "Draft Ready"
3. For each entry:
   - Read Canon (Brand Foundation)
   - Call Creator Outreach agent
   - Store draft message in Notion (update Outreach Status = "Awaiting Approval")

---

## AI Agents (Claude API via MCP)

### Content Idea Miner (Phase 2, Day 3)
**Purpose:** Analyze captured content and generate 2-5 WhyHi content ideas
**Input:**
```json
{
  "source_url": "string (original captured content)",
  "content_notes": "string (Tom's observations)",
  "platform": "string (where content was found)",
  "brand_foundation": "string (Canon reference)",
  "content_playbook": "string (Canon reference)"
}
```

**Output:**
```json
{
  "ideas": [
    {
      "title": "string",
      "description": "string",
      "platform": "LinkedIn|Facebook|Instagram|All",
      "content_type": "Social Post|Video",
      "use_case_reference": "string (which cluster/scenario)",
      "formula_used": "Use Case Spotlight|Hidden Cost|etc"
    }
    // ... 2-5 ideas total
  ]
}
```

**Canon References:**
- `/canon/brand_foundation.md` - Messaging, voice, themes
- `/canon/cos_content_playbook.md` - Writing formulas, use cases

---

### Content Drafter (Phase 3, Day 5)
**Purpose:** Generate platform-specific content drafts from approved ideas
**Input:**
```json
{
  "idea_title": "string",
  "idea_description": "string",
  "content_type": "Social Post|Video",
  "platform": "LinkedIn|Facebook|Instagram|All",
  "use_case_reference": "string",
  "formula_used": "string",
  "brand_foundation": "string (Canon reference)",
  "content_playbook": "string (Canon reference)",
  "founder_voice_profile": "string (Canon reference)"
}
```

**Output (Social Post):**
```json
{
  "linkedin_content": "string (150-250 words)",
  "facebook_content": "string (100-200 words)",
  "instagram_content": "string (80-150 words)",
  "image_suggestions": "string (Unsplash/Pexels search terms)"
}
```

**Output (Video):**
```json
{
  "video_script": "string (full script with timestamps)",
  "storyboard_notes": "string (visual direction)",
  "video_length": "30-60s|60-90s",
  "video_format": "Talking Head|Reenactment|Educational"
}
```

**Canon References:**
- `/canon/brand_foundation.md`
- `/canon/cos_content_playbook.md`
- `/canon/founder_voice_profile.md`

---

### Creator Outreach (Existing - May Need Updates)
**Purpose:** Generate personalized outreach messages to creators
**Updates for COS Integration:**
- Reference Brand Foundation for WhyHi positioning
- Platform-specific tone (Twitter DM vs LinkedIn vs Email)
- Personalization based on source content captured

---

## Buffer Configuration

### Setup (Phase 4, Day 8 - Tom's Tasks)
- Create Buffer account (free tier)
- Connect platforms: LinkedIn, Facebook, Instagram
- Generate API access token
- Provide token to Claude Code

### API Integration
**Buffer API Token:** [TBD - Tom will provide]
**Base URL:** `https://api.bufferapp.com/1/`
**Endpoints Used:**
- `POST /updates/create.json` - Schedule post
- `GET /updates/{id}.json` - Get post analytics

**Platform Profile IDs:** [TBD - Will be retrieved from Buffer API after setup]

---

## Environment Variables

Add to `.env`:
```bash
# COS-specific
BUFFER_API_TOKEN=[TBD - Tom will provide]

# Existing (for reference)
NOTION_API_KEY=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
NOTION_APPROVAL_DB_ID=2ee632f5-307e-8153-a5b9-d4264517b035
NOTION_CRM_DB_ID=23d632f5307e8001a1d6fb31be92d59e
```

---

## Webhook URLs

### content_capture (iOS Shortcut)
**Webhook URL:** [TBD - Will be documented after workflow update]
**Method:** POST
**Payload:**
```json
{
  "url": "string (captured URL)",
  "notes": "string (optional user notes)"
}
```

---

## Database Relation Map

```
Content & Creator Capture
    ↓ Generated Ideas (relation)
Content Ideas Queue
    ↓ Generated Draft (relation)
Drafts for Review
    ↓ Scheduled Post (relation)
Content Calendar
```

---

## Phase Completion Checklist

### Phase 1: Foundation (In Progress)
- [x] Canon documents created (brand_foundation.md, cos_content_playbook.md, founder_voice_profile.md)
- [x] Content & Creator Capture updated with new fields
- [x] Content Ideas Queue database created
- [x] Drafts for Review database created
- [x] Content Calendar database created
- [x] Database relations configured (4/4)
- [ ] content_capture workflow updated
- [x] COS_SETUP.md created

### Phase 2: Ideation Flow
- [ ] Content Idea Miner agent created
- [ ] ideation_trigger workflow created
- [ ] End-to-end test: Capture → Ideas

### Phase 3: Drafting Flow
- [ ] Content Drafter agent created
- [ ] drafting_trigger workflow created
- [ ] End-to-end test: Idea → Draft

### Phase 4: Scheduling
- [ ] Buffer credentials configured
- [ ] buffer_scheduling workflow created
- [ ] engagement_tracking workflow created
- [ ] End-to-end test: Draft → Buffer → Calendar

### Phase 5: Outreach (Optional)
- [ ] Creator Outreach agent updated
- [ ] outreach_trigger workflow created

---

## Support & Troubleshooting

### Common Issues

**Ideation workflow not triggering:**
- Check Notion filter: Action Type contains "💡 Content Ideation"
- Verify Ideation Status is set to "Sent to COS"
- Check n8n execution log

**Drafts not generating:**
- Verify idea Status is "Approved"
- Check Content Drafter agent has access to Canon
- Review n8n execution log for errors

**Buffer scheduling fails:**
- Verify Buffer API token valid
- Check platform profile IDs configured
- Ensure draft has platform-specific content

---

**END OF COS_SETUP.md**
