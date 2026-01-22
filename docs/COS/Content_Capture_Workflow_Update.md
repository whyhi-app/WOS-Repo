# Content Capture Workflow Update

**Created:** January 21, 2026
**Phase:** 1, Day 2
**Purpose:** Instructions for updating content_capture workflow with new COS fields

---

## What Changed

The workflow has been updated from `creator_capture_v0` to `content_capture_v1` with the following changes:

### New Notion Fields Added:
1. **Content Notes** - Populated with user's submitted notes from iOS share sheet
2. **Ideation Status** - Automatically set to "New" for all captured content

### Fields Left Empty (User Triages Manually):
- **Action Type** (multi-select) - User selects "💡 Content Ideation" or "🤝 Outreach"
- **Topic Tags** (multi-select) - User adds relevant topic tags
- **Relevance Score** (number) - User rates 1-5

---

## Installation Steps

### Option 1: Import New Workflow (Recommended)

1. Open n8n at `https://n8n.whyhi.app`
2. Click **Workflows** → **Import from File**
3. Select `/Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/packs/P3.2/WORKFLOWS/content_capture_v1.json`
4. Click **Import**
5. Activate the workflow
6. Copy the webhook URL (you'll need this for iOS Shortcut)

### Option 2: Update Existing Workflow Manually

If you prefer to update the existing `creator_capture_v0` workflow:

1. Open the existing workflow in n8n
2. Click on the **"Create CRM Entry"** node
3. In the **Properties** section, add two new custom properties:
   - **Content Notes**: `={{$json.user_notes}}`
   - **Ideation Status**: Select value = "New"
4. Click on the **"Extract Creator Info"** code node
5. Update the JavaScript to capture user notes from webhook:
   ```javascript
   const userNotes = $input.item.json.body.notes || '';
   // Add to creator object:
   user_notes: userNotes
   ```
6. Save the workflow
7. Test with a sample URL

---

## iOS Shortcut Update

**IMPORTANT:** If you import a new workflow, you'll need to update your iOS shortcut with the new webhook URL.

### How to Update:
1. Open **Shortcuts** app on iOS
2. Find your **"Share to WhyHi CRM"** shortcut (or whatever you named it)
3. Edit the shortcut
4. Update the webhook URL to the new `content_capture_v1` endpoint
5. Test by sharing a URL from Safari/Twitter/Instagram

---

## Testing the Updated Workflow

### Test Case 1: Capture an Article (Content Ideation)
1. Share an article URL from Safari via iOS shortcut
2. Add notes: "Good example of loneliness epidemic stats"
3. Check Notion database:
   - ✓ Entry created with article URL
   - ✓ "Content Notes" contains your notes
   - ✓ "Ideation Status" = "New"
   - ✓ Action Type, Topic Tags, Relevance Score are empty (manual triage)

### Test Case 2: Capture a Creator Profile (Outreach)
1. Share a Twitter/Instagram profile URL
2. Add notes: "Creator with 50k followers, talks about phone anxiety"
3. Check Notion database:
   - ✓ Entry created with creator handle
   - ✓ Platform detected correctly
   - ✓ "Content Notes" contains your notes
   - ✓ "Ideation Status" = "New"

### Test Case 3: Dual Purpose (Both Outreach + Ideation)
1. Capture a creator's post URL
2. Manually triage in Notion:
   - Set Action Type: "💡 Content Ideation" + "🤝 Outreach"
   - Add Topic Tags: "Telephobia", "Connection"
   - Set Relevance Score: 5
3. Later, when ready, set "Ideation Status" to "Sent to COS" to trigger idea generation

---

## Webhook Endpoint

**New Webhook URL:** `https://n8n.whyhi.app/webhook/wos/intent/content_capture_v1`

**Method:** POST

**Payload:**
```json
{
  "url": "https://example.com/article",
  "notes": "Optional user notes about the content"
}
```

**Response:**
```json
{
  "ok": true,
  "status": "Content added to CRM",
  "name": "example.com",
  "platform": "Article/Blog",
  "contact_method": "Email"
}
```

---

## Troubleshooting

**Workflow not triggering:**
- Check workflow is activated in n8n
- Verify webhook URL is correct in iOS shortcut
- Check n8n execution log for errors

**New fields not appearing in Notion:**
- Verify Content & Creator Capture database has the new properties
- Check property names match exactly (case-sensitive)
- Re-run the database setup script if needed

**User notes not being saved:**
- Check iOS shortcut is passing `notes` field in request body
- Verify Extract Creator Info node is capturing `user_notes`
- Check Create CRM Entry node maps `user_notes` to "Content Notes"

---

## Next Steps

After updating the workflow:
1. ✅ Test with multiple content types (articles, social posts, creator profiles)
2. ✅ Verify all new fields populate correctly
3. ✅ Practice manual triage workflow (Action Type, Topic Tags, Relevance Score)
4. ⏭️ Proceed to Phase 2: Build Content Idea Miner agent

---

**END OF WORKFLOW UPDATE GUIDE**
