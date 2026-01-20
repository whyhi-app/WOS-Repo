# Setup Gmail for Outreach Sending

## WhyHi Email Strategy

You have three Gmail accounts on Google Workspace:

- **tom@whyhi.app** → Personal outreach (creator/journalist outreach)
- **admin@whyhi.app** → Operations/automation (WOS system emails, monitoring)
- **hello@whyhi.app** → Public marketing (newsletters, social announcements)

The Approval Queue has a "Sending Email" field to specify which account sends each message.

## Setup Steps

### Step 1: Generate App Passwords for All Accounts

You need to generate app passwords for each Gmail account you want to send from.

#### For tom@whyhi.app (Required for Creator Outreach)

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with **tom@whyhi.app**
3. Click **"Select app"** → Choose **"Mail"**
4. Click **"Select device"** → Choose **"Other"** → Type: "WOS Outreach Tom"
5. Click **"Generate"**
6. Copy the 16-character password (format: xxxx xxxx xxxx xxxx)
7. Save it - you'll add it to .env in Step 2

#### For admin@whyhi.app (Optional - for system emails)

Repeat the process above:
1. Sign in with **admin@whyhi.app**
2. Generate app password with name: "WOS System Admin"
3. Copy the password

#### For hello@whyhi.app (Optional - for public marketing)

Repeat the process above:
1. Sign in with **hello@whyhi.app**
2. Generate app password with name: "WOS Marketing Hello"
3. Copy the password

### Step 2: Add to .env File

Open `/Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/.env` and add these lines:

```bash
# Gmail App Passwords for Outreach Sending
GMAIL_PASSWORD_TOM=xxxx xxxx xxxx xxxx
GMAIL_PASSWORD_ADMIN=xxxx xxxx xxxx xxxx
GMAIL_PASSWORD_HELLO=xxxx xxxx xxxx xxxx
```

Replace with your actual app passwords from Step 1.

**Note:** You only need to set up the accounts you'll actually use. For testing Creator Outreach, just `GMAIL_PASSWORD_TOM` is required.

### Step 3: Test Email Sending

**Set up test recipient:**
What email address should receive the test? Update Sarah Chen's email in the CRM to your personal email address, or let me know and I'll create a script to update it.

**Then run the test:**

```bash
# 1. Create approval (will use Sarah Chen from CRM)
python3 test_creator_outreach_workflow.py

# 2. Open the Notion URL it gives you
#    - Review the outreach message
#    - Verify "Sending Email" is set to "tom@whyhi.app"
#    - Change Status from "Pending" to "Approved"

# 3. Process approved requests and send emails
python3 process_approved_outreach.py
```

The email will be sent from **tom@whyhi.app** to the recipient's email address.

## How It Works

1. **Approval Creation**: When an approval is created, "Sending Email" is set based on the outreach type:
   - Creator/Journalist outreach → tom@whyhi.app
   - System notifications → admin@whyhi.app
   - Public marketing → hello@whyhi.app

2. **Processing**: When you approve an outreach request, the processor:
   - Reads the "Sending Email" field
   - Uses the corresponding Gmail app password
   - Sends from that account

3. **You can override**: Change "Sending Email" in any approval to use a different account

## Security Notes

- App passwords are **not** your regular Gmail passwords
- They're specifically for apps/scripts to access Gmail
- You can revoke them anytime at https://myaccount.google.com/apppasswords
- Don't commit .env file to git (already in .gitignore)
- Each account has its own independent app password

## Troubleshooting

**Error: "Username and Password not accepted"**
- Make sure you're using the app password, not your regular password
- App password should be 16 characters (remove spaces when adding to .env)
- Verify you generated the password for the correct Gmail account

**Email not sending:**
- Check that GMAIL_PASSWORD_TOM (or corresponding account) is set in .env
- Verify the "Sending Email" field is set in the Notion approval
- Check process_approved_outreach.py output for error messages
