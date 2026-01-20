# Creator Capture - iOS Shortcut Setup Guide

**Purpose:** Capture creator/journalist links from any iOS app and automatically populate your Notion CRM.

---

## Prerequisites

1. n8n workflow `creator_capture_v0.json` imported and activated
2. Notion CRM database shared with your "WOS Approval Gate" integration
3. iOS device with Shortcuts app

---

## Part 1: Deploy n8n Workflow

### Step 1: Import Workflow
1. Open n8n
2. Go to **Workflows** → **Import from File**
3. Select: `/Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/packs/P3.2/WORKFLOWS/creator_capture_v0.json`
4. Click **Import**

### Step 2: Configure Credentials
The workflow needs:
- **Notion API** credential (should already exist as "Notion WOS")
  - If missing, create new credential with your Notion API key

### Step 3: Activate Workflow
1. Click the **Inactive** toggle to activate
2. Workflow will start listening for webhooks

### Step 4: Get Webhook URL
1. Click on the **Webhook** node (first node)
2. Copy the **Production URL**
   - Format: `https://n8n.whyhi.app/webhook/wos/intent/creator_capture_v0`
3. Save this URL - you'll need it for the iOS Shortcut

---

## Part 2: Create iOS Shortcut

### Step 1: Open Shortcuts App
1. Open **Shortcuts** app on iPhone/iPad
2. Tap **+** (top right) to create new shortcut

### Step 2: Add "Get URLs from Input" Action
1. Search for "Get URLs from Input"
2. Add it as the first action
3. This extracts the URL from whatever you share

### Step 3: Add "Get Contents of URL" Action
1. Search for "Get Contents of URL"
2. Add it after "Get URLs from Input"
3. Set URL to: **URLs** (from previous step)
4. This will fetch the page content for creator extraction

### Step 4: Add "Get Text from Input" Action
1. Search for "Get Text from Input"
2. Add it after "Get Contents of URL"
3. Set input to: **Contents of URL**
4. This converts the page to text for parsing

### Step 5: Add "Get URLs from Input" (Again)
1. Add another "Get URLs from Input"
2. This extracts the original URL we're sharing

### Step 6: Add "Get Contents of URL" (Webhook Call)
1. Add another "Get Contents of URL"
2. Set **URL** to: `https://n8n.whyhi.app/webhook/wos/intent/creator_capture_v0`
   (Use the webhook URL from Part 1, Step 4)
3. Tap **Show More**
4. Set **Method** to: **POST**
5. Set **Request Body** to: **JSON**
6. Add JSON body:
```json
{
  "url": "{{URL from Step 5}}"
}
```

To add the URL variable:
- Tap in the quotes after "url": "
- Tap the **{}** variable button
- Select **URL** (from the second "Get URLs from Input" step)

### Step 7: Add "Show Notification" (Optional)
1. Search for "Show Notification"
2. Add at the end
3. Set text to: "Creator added to CRM!"
4. This confirms the capture worked

### Step 8: Configure Shortcut Settings
1. Tap the info button (i) next to shortcut name
2. Name it: **Capture Creator**
3. Add icon: Choose a relevant icon (📝 or 🎯)
4. Enable **Show in Share Sheet**
5. Set **Accepted Types**: **URLs**, **Safari Web Pages**, **Text**

### Step 9: Save
1. Tap **Done**
2. Shortcut is ready!

---

## Part 3: Test the Shortcut

### Test 1: Share from Safari
1. Open Safari
2. Go to a creator's Twitter profile, article, or YouTube channel
3. Tap the **Share** button
4. Scroll down and select **Capture Creator**
5. Wait for notification: "Creator added to CRM!"
6. Check your Notion CRM - new entry should appear with:
   - Name extracted from URL/page
   - Platform detected (Twitter, YouTube, etc.)
   - Contact method auto-set (DM vs email)
   - Outreach Status: "New Lead"

### Test 2: Share from Twitter/X App
1. Open a creator's Twitter profile
2. Tap **Share** → **Share via...**
3. Select **Capture Creator**
4. Check Notion CRM for new entry

### Test 3: Share from Instagram
1. Open a creator's Instagram profile
2. Tap **...** → **Copy Profile URL**
3. Open Shortcuts app
4. Tap **Capture Creator**
5. Paste the URL when prompted
6. Check Notion CRM

---

## Part 4: Usage Workflow

### Daily Usage
1. **Find creator content** (Twitter, Instagram, YouTube, articles, etc.)
2. **Share → Capture Creator** (1 tap)
3. Creator info automatically added to Notion CRM with "New Lead" status

### Research Phase
1. Review CRM entries
2. Update status to "Researched" when you've checked them out
3. Add notes about why they're relevant

### Outreach Phase
1. Update status to "Draft Ready" when ready for outreach
2. Execute Creator Outreach intent:
   ```bash
   ~/.local/bin/claude "execute the creator_outreach intent with status_filter='Draft Ready' and limit=5"
   ```
3. Review/approve personalized messages in Notion
4. Send approved messages
5. CRM status auto-updates to "Outreach Sent"

---

## Troubleshooting

### Shortcut doesn't appear in share sheet
- Check Shortcut settings: "Show in Share Sheet" must be enabled
- Accepted Types must include "URLs" or "Safari Web Pages"

### "Creator added to CRM!" but nothing in Notion
- Check n8n execution logs for errors
- Verify Notion credential is valid
- Verify CRM database ID is correct in workflow (23d632f5307e8001a1d6fb31be92d59e)

### Wrong creator info extracted
- The workflow uses URL patterns and HTML parsing
- Some platforms may need manual cleanup in Notion
- You can always edit the CRM entry after capture

### Webhook timeout
- Check n8n workflow is activated
- Verify webhook URL is correct
- Check network connection

---

## CRM Outreach Status Field Values

- **New Lead** - Just captured, not reviewed
- **Researched** - Reviewed and relevant
- **Draft Ready** - Ready for outreach message generation
- **Outreach Sent** - Message sent (auto-set by Creator Outreach agent)
- **Responded** - They replied (manually set)
- **No Response** - Follow-up needed (manually set)
- **Not Interested** - Declined/not relevant (manually set)

---

## Platform Support

The workflow automatically detects and handles:

- **Twitter/X** - Extracts @handle, sets contact method to "Twitter DM"
- **Instagram** - Extracts @handle, sets contact method to "Instagram DM"
- **YouTube** - Extracts channel name, sets contact method to "YouTube Comment/Email"
- **TikTok** - Extracts @handle, sets contact method to "TikTok DM"
- **LinkedIn** - Extracts name, sets contact method to "LinkedIn Message"
- **Articles/Blogs** - Extracts author name and email (if found), sets contact method to "Email"

---

## Next Steps

1. Deploy the workflow (Part 1)
2. Create the iOS Shortcut (Part 2)
3. Test with a few creators (Part 3)
4. Start building your creator pipeline!

When you have creators with "Draft Ready" status, run the Creator Outreach intent to generate personalized messages with approval workflow.

**Happy capturing! 🎯**
