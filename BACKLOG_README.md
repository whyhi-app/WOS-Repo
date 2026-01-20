# Backlog System - How It Works

## Quick Reference

**Add to backlog:**
```bash
python3 add_to_backlog.py "Your task description"
```

**Complete a backlog item:**
1. Mark it done in Notion
2. Delete the section from BACKLOG.md
3. Commit the change

---

## The System

### Two Places, Same Tasks

Every backlog item exists in **both**:

1. **BACKLOG.md** (detailed, version controlled)
   - Full context and notes
   - Grouped by category
   - Git history of what was added/removed

2. **Notion tasks-masterlist** (Context: "Backlog")
   - Quick filtering and triage
   - Can add due dates, priorities, etc.
   - Your normal task workflow

### When to Add to Backlog

**During our sessions, I'll ask:**
> "Should I add this to the backlog?"

When we encounter:
- Things that take too long to do now
- Items that need other work done first (blocked)
- Ideas for later that shouldn't be forgotten
- Features to build after initial launch

**You say:** "yes" or "add to backlog"

**I run:** `python3 add_to_backlog.py "Task description"`

**Result:** Task in both BACKLOG.md and Notion (Context: "Backlog")

---

## Workflow Example

### Adding an Item

**Scenario:** We're working on Creator Outreach and realize we need Facebook API setup, but it's 3 hours of work.

**Me:** "Should I add 'Set up Facebook Graph API for auto-DM sending' to the backlog?"

**You:** "yes"

**Me:** *Runs add_to_backlog.py*

**Result:**
- ✅ Added to BACKLOG.md with details
- ✅ Created in Notion tasks-masterlist
- ✅ Tagged with Context: "Backlog"
- ✅ Work continues without interruption

### Completing an Item

**Later:** You decide to work on the Facebook API task

**In Notion:**
1. Filter by Context: "Backlog"
2. Find "Set up Facebook Graph API..."
3. Add details, due date, etc.
4. Work on it
5. Mark as complete

**In BACKLOG.md:**
1. Find the "Facebook Graph API" section
2. Delete it (no longer pending)
3. Commit: `git commit -am "Complete: Facebook API setup"`

**Why delete from BACKLOG.md?**
- Keeps the backlog file clean (only pending items)
- Git history preserves what was done
- Notion has the full completion record

---

## BACKLOG.md Structure

```markdown
# WOS Development Backlog

## Category Name

**Priority:** High/Medium/Low
**Effort:** Time estimate
**Added:** Date

- [ ] Task description
  - Detail 1
  - Detail 2

---
```

Categories:
- **Integrations** - Third-party API setups
- **Infrastructure** - Core systems, decisions
- **Agents** - New agent development
- **Improvements** - Enhancements to existing features

---

## Current Backlog Items

See **BACKLOG.md** for the full list.

In Notion, filter tasks-masterlist by:
- Context: "Backlog"

---

## Why This System?

### BACKLOG.md Benefits
- **Version controlled** - See what was added when
- **Detailed context** - More space for notes than Notion titles
- **Code proximity** - Right in the repo
- **Session continuity** - I can see it in every session

### Notion Benefits
- **Your workflow** - Already using Notion for tasks
- **Filtering** - Easy to see all backlog items
- **Prioritization** - Add due dates, priorities
- **Status tracking** - Mark progress

### Both Together
- Quick capture during sessions (doesn't break flow)
- Detailed planning when ready (promote from backlog to sprint)
- History preserved (git + Notion)
- Nothing gets forgotten

---

## Pro Tips

1. **Don't overthink it** - Just add things when they come up
2. **Review weekly** - Look at BACKLOG.md to pick what's next
3. **Delete completed items** - Keep BACKLOG.md lean
4. **Use Notion for details** - BACKLOG.md is the list, Notion is the workspace
5. **Commit often** - Each backlog change should be committed

---

## Questions?

Just ask during our next session!
