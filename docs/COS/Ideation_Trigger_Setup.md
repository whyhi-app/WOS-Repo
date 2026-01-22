# Ideation Trigger Workflow Setup

**Created:** January 22, 2026
**Phase:** 2, Day 4
**Purpose:** Auto-trigger Content Idea Miner for captured content ready for ideation

---

## What This Workflow Does

The `ideation_trigger_v1` workflow runs every 15 minutes and:

1. **Polls Content & Creator Capture** database for entries with:
   - `Ideation Status = "Sent to COS"`
   - `Action Type` contains "💡 Content Ideation"
   - Sorted by Relevance Score (highest first)
   - Limit: 5 entries per run

2. **Triggers Content Idea Miner** handler if entries found:
   - Sends request to WOS `/execute` endpoint
   - Intent ID: `content_idea_miner_v1`
   - Minimum relevance score: 3/5

3. **Logs results**: Success with idea count or "no entries found"

---

## Installation

### Step 1: Import Workflow to n8n

1. Open n8n at `https://n8n.whyhi.app`
2. Click **Workflows** → **Import from File**
3. Select: `/Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/packs/P3.2/WORKFLOWS/ideation_trigger_v1.json`
4. Click **Import**

### Step 2: Configure Credentials

The workflow needs two credentials:

**A. Notion API Credential:**
- Node: "Query Content Capture"
- Should already be configured as "Notion WOS"
- If not, select your existing Notion credential

**B. WOS API Key Credential (HTTP Header Auth):**
- Node: "Trigger Content Idea Miner"
- Create new credential if needed:
  1. Click "Create New Credential"
  2. Select "HTTP Header Auth"
  3. Name: `WOS API Key`
  4. Header Name: `X-API-Key`
  5. Header Value: `your_wos_api_key_here` (if WOS requires auth)
  6. Save

### Step 3: Activate Workflow

1. Click **Activate** toggle in top-right
2. Workflow will now run every 15 minutes

---

## How to Use

### Manual Trigger (for testing):

1. **Capture some content** using the iOS shortcut
2. **Open the entry in Notion** (Content & Creator Capture database)
3. **Triage the entry:**
   - Set `Action Type` to "💡 Content Ideation"
   - Add `Topic Tags` (e.g., "Loneliness", "Telephobia")
   - Set `Relevance Score` to 4 or 5
4. **Change status** to trigger ideation:
   - Set `Ideation Status` to "Sent to COS"
5. **Wait up to 15 minutes** or manually trigger the workflow
6. **Check the Ideas Queue** - you should see 2-5 new ideas generated!

### Check Results:

**In Notion:**
- Original entry should now have `Ideation Status = "Ideas Generated"`
- Check **Content Ideas Queue** database for new entries
- Each idea will be linked back to the source content

**In WOS Artifacts:**
- Check `/artifacts/ideation/` folder
- Look for `content_ideas_YYYY-MM-DD.md` file
- Contains full log of all ideas generated that day

---

## Workflow Settings

### Schedule Interval

Default: Every 15 minutes

To change:
1. Click on "Schedule" node
2. Modify "Minutes Interval" field
3. Recommended: 15-30 minutes (balance between responsiveness and API costs)

### Entry Limit

Default: 5 entries per run

To change:
1. Click on "Query Content Capture" node
2. Modify "Limit" field
3. Recommended: 3-10 entries (Claude API rate limits apply)

### Minimum Relevance Score

Default: 3/5

To change:
1. Click on "Trigger Content Idea Miner" node
2. Edit JSON body → `min_relevance_score` field
3. Set to 0 to process all entries regardless of score

---

## Troubleshooting

**Issue: "No entries found" every time**
- Check that entries have BOTH:
  - `Ideation Status = "Sent to COS"` (exact text)
  - `Action Type` contains "💡 Content Ideation"
- Verify the database ID matches in the "Query Content Capture" node

**Issue: Workflow triggers but no ideas created**
- Check WOS server logs for errors
- Verify `ANTHROPIC_API_KEY` is set in `.env`
- Ensure Canon documents exist in `/canon/` directory

**Issue: Ideas generated but quality is poor**
- Increase `min_relevance_score` to only process high-quality captures
- Improve content notes when capturing (more context = better ideas)
- Refine Brand Foundation or Content Playbook in Canon

---

## Next Steps

After ideation is working:
1. **Phase 3:** Build Content Drafter agent to turn ideas into platform-specific drafts
2. **Phase 4:** Integrate with Buffer for scheduling and publishing
3. **Phase 5:** Optional - build outreach workflow for creator partnerships

---

**END OF IDEATION TRIGGER SETUP**
