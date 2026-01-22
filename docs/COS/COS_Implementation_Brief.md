COS (Content Operating System) - Complete Implementation Brief
Version: 1.0
Date: January 21, 2026
For: Claude Code
Project: WhyHi Content Operating System

TABLE OF CONTENTS

CC Handoff Prompt
Executive Summary
Canon Documents Content

Brand Foundation
COS Content Playbook


Technical Specifications

Notion Database Architecture
n8n Workflow Specifications
Agent Specifications


Build Order & Timeline
Pre-Launch Content Sprint Plan
Immediate Post-Build Tasks
Items for BACKLOG.md
Testing & Validation


CC HANDOFF PROMPT
Copy this section and use it to start your conversation with Claude Code:

COS (Content Operating System) Implementation
I need you to build the Content Operating System (COS) for WhyHi based on the complete specifications I'm providing. This is a multi-agent system that automates content creation and creator outreach.
Context

You have access to the WOS repository with existing n8n workflows and Notion integrations
The content_capture workflow (formerly creator_capture_v0) already exists and needs amendment
Canon directory exists at /canon/ for storing reference documents
I'm using Notion as the master repository and Buffer for social media scheduling
I have a BACKLOG.md system for tracking future enhancements

What I'm Providing
This complete COS Implementation Brief includes:

Brand Foundation - Core positioning and messaging (save to /canon/brand_foundation.md)
COS Content Playbook - Writing formulas, use cases, video frameworks (save to /canon/cos_content_playbook.md)
Technical Specifications - Notion database structures, workflow specs, agent requirements
Build Order - Phased implementation plan over 2 weeks
Pre-Launch Content Sprint Plan - How to build content library before launch
Post-Build Tasks - What Tom handles separately vs what goes in BACKLOG.md

Your Tasks
Phase 1: Foundation (Week 1, Days 1-2)

Save Brand Foundation and Content Playbook to Canon (extract from this brief)
Create placeholder for Founder Voice Profile in Canon
Update the existing Notion database (Content & Creator Capture) with new fields
Create three new Notion databases (Content Ideas Queue, Drafts for Review, Content Calendar)
Amend the existing content_capture workflow to populate new fields

Phase 2: Ideation Flow (Week 1, Days 3-4)
6. Build the Content Idea Miner agent
7. Build the ideation_trigger workflow
Phase 3: Drafting Flow (Week 1-2, Days 5-7)
8. Build the Content Drafter agent
9. Build the drafting_trigger workflow
Phase 4: Scheduling (Week 2, Days 8-9)
10. Set up Buffer integration (Tom will provide API credentials)
11. Build buffer_scheduling workflow
12. Build engagement_tracking workflow
Phase 5: Outreach (Week 2, Day 10, If Time)
13. Update existing Creator Outreach agent for unified database
14. Build outreach_trigger workflow
Important Notes
Iterative & Flexible Design:

These documents (Brand Foundation, Content Playbook) are LIVING documents that will evolve
Build the system to support ongoing revision based on performance data
Tom will have weekly strategy sessions with WOS to refine messaging
Agents always reference the CURRENT version of Canon documents
If Tom says "update the playbook," you should edit the markdown file and confirm changes

Notion Database Changes:

Walk Tom through each database modification BEFORE executing
Explain what each new field does and why it's needed
Offer to create backups before making changes
Show test entries after creation
Be prepared to adjust based on Tom's feedback

Testing at Each Phase:

Don't move to next phase until current phase is tested and working
Show Tom test results and get approval before proceeding
Include error handling and logging in all workflows

Documentation:

Document all webhook URLs, API endpoints, database IDs
Create a COS_SETUP.md file with configuration details
Note any credentials/tokens Tom needs to provide

Questions to Ask Me Before Starting

What's the Notion database ID for the existing Creator CRM (Content & Creator Capture)?
Do you want me to create a backup of the existing database before modifying it?
Should I start with Phase 1 or do you want to review the database structures first?
Do you have Buffer API credentials ready, or should we defer Phase 4 until you set that up?
Any specific preferences for how you want to be notified during the build (error messages, completion confirmations)?


END OF CC HANDOFF PROMPT - Everything below is reference material for Claude Code

EXECUTIVE SUMMARY
What is COS?
The Content Operating System (COS) is a multi-agent automation system that transforms WhyHi's content creation from manual ideation/writing to a streamlined pipeline:
Input: Tom captures interesting content from social media, articles, creators
Process: AI agents analyze, generate ideas, draft posts/videos, schedule to Buffer
Output: Platform-specific content posted automatically, engagement tracked, insights fed back
System Architecture
┌─────────────────────────────────────────────────────────────────┐
│                    CONTENT OPERATIONS SYSTEM                     │
└─────────────────────────────────────────────────────────────────┘

LAYER 1: CAPTURE
    Tom finds content → iOS share → content_capture workflow → Notion
    
LAYER 2: KNOWLEDGE BASE (Canon)
    Brand Foundation + Content Playbook + Founder Voice Profile
    
LAYER 3: IDEATION
    Content Idea Miner analyzes captured content → generates 2-5 ideas → Notion
    
LAYER 4: DRAFTING
    Content Drafter takes approved ideas → generates posts/scripts → Notion
    
LAYER 5: SCHEDULING & PUBLISHING
    Approved drafts → Buffer → Auto-post → Engagement metrics → Notion
Key Components
Notion Databases:

Content & Creator Capture (unified inbox - existing, needs amendment)
Content Ideas Queue (new)
Drafts for Review (new)
Content Calendar (new)

n8n Workflows:

content_capture (existing - amend)
ideation_trigger (new)
drafting_trigger (new)
buffer_scheduling (new)
engagement_tracking (new)
outreach_trigger (new - optional Phase 5)

AI Agents:

Content Idea Miner (new)
Content Drafter (new)
Creator Outreach (existing - may need update)

External Integrations:

Buffer (social media scheduling)
Unsplash/Pexels (royalty-free images)
CapCut (Tom's manual video editing)

Success Criteria
After Phase 5, Tom should be able to:

Capture content from social media with one tap
Triage in Notion: outreach, ideation, or both
Get AI-generated content ideas automatically
Approve ideas and receive platform-specific drafts
Schedule posts to Buffer with one click
Track engagement metrics automatically
Have weekly strategy discussions with WOS to refine messaging

Pre-Launch Goal:

Build library of 30 posts + 15 videos before mid-March launch
Content calendar populated through April
Posting runs on autopilot post-launch


CANON DOCUMENTS CONTENT
Instructions for Claude Code: Extract the following content and save to the specified file paths in the WOS repository.

Document 1: Brand Foundation
File Path: /canon/brand_foundation.md
Content:
markdown# WhyHi Brand Foundation

**Version:** 1.0  
**Last Updated:** January 21, 2026  
**Purpose:** Core reference document for all content generation. Informs Content Drafter agent when creating posts, scripts, and messaging.

---

## POSITIONING

### What WhyHi Is
WhyHi is a calling app that shows you why someone is calling and how long they need before you answer.

### The Problem It Solves
Phone calls have become anxiety-inducing because they're blind and open-ended. Texting feels safer but doesn't create real connection. We're lonelier than ever in a hyperconnected world.

### Why It's Different
WhyHi gives you the control of texting (you know what's coming, you can choose when) combined with the connection of live conversation. It transforms calls from interruptions into informed choices.

---

## CORE INSIGHT

### The Hidden Truth
Messaging has fooled us into thinking constant texting equals connection. It doesn't. Real connection requires presence, and that only happens in live conversation. But we avoid calling because calls feel risky—we don't know why someone's calling or how long it will take.

### The Revelation
Once you experience seeing "5 min · Question" before answering a call, you immediately realize you'd want this for every call. The problem becomes obvious the moment it's named.

---

## TARGET AUDIENCES

### 1. Busy Professionals & Parents
**Pain Point:** Too many commitments, too little time. Can't take random calls but wants connection.

**WhyHi Value:** "I can say yes to a 10-minute call because I know it won't derail my day."

**Blind Spot:** Thinks texting is efficient—doesn't realize it's actually time-consuming AND emotionally unsatisfying.

**Key Messaging:** Time-bounded communication, respects your schedule, spontaneous connection without sacrifice.

---

### 2. Call-Anxious / Telephobia Community
**Pain Point:** Phone anxiety, dread of unexpected calls, avoidance spirals.

**WhyHi Value:** "Calls become predictable events, not surprise demands."

**Blind Spot:** Believes their anxiety is personal—doesn't realize the *design* of phone calls is the problem.

**Key Messaging:** Predictability, removing uncertainty, design solution not personal failing.

---

### 3. Neurodivergent Community (Autism, ADHD)
**Pain Point:** Unexpected interactions cause overwhelm. Need structure and boundaries.

**WhyHi Value:** "WhyHi is a boundary-first calling system. It's like a mini-agreement before the call."

**Blind Spot:** Has adapted to avoiding calls—hasn't seen that calls can be redesigned to work with their needs.

**Key Messaging:** Clear expectations, routine-friendly, reduces activation energy, respects processing needs.

---

### 4. Relationship Maintainers
**Pain Point:** Friendships slipping away. Wants to stay close but life gets busy.

**WhyHi Value:** "Makes spontaneous connection feel possible again. 10-minute catch-ups that actually happen."

**Blind Spot:** Puts off calling because it feels like a big commitment—doesn't realize a 10-minute boundary changes everything.

**Key Messaging:** Stay close without overstepping, lightweight friendship upkeep, connection without guilt.

---

## VOICE GUARDRAILS

### WhyHi DOES Sound Like:
- Warm and conversational
- Observational (naming universal truths)
- Casual but intelligent
- Self-aware and self-deprecating
- Direct and honest
- Fast-paced and energetic (matches Tom's speaking style)
- Uses natural analogies and relatable scenarios

### WhyHi NEVER Sounds Like:
- Clinical or therapeutic
- Sales-y or pushy
- Corporate or formal
- Preachy or judgmental
- Tech-bro or jargon-heavy
- Overly polished or scripted
- Apologetic or tentative

---

## LANGUAGE GUIDELINES

### Words/Phrases TO USE:
- "Shared contract" (not "agreement")
- "Live connection" (not "real-time communication")
- "Presence" and "being present"
- "Blind call" / "open-ended imposition"
- "Intentional calling"
- "You know what you're signing up for"
- "It just makes sense"
- "Mini-agreement"
- "Informed choice"
- "Time-bounded" / "Time-boxed"
- "Context before commitment"

### Words/Phrases TO AVOID:
- "Revolutionary" / "game-changing"
- "Anxiety solution" (too clinical)
- "Better than [competitor name]"
- "Productivity hack"
- "Must-have app"
- Medical/diagnostic language ("treats anxiety," "cures telephobia")
- "Cutting-edge" / "innovative" (show, don't tell)
- "Seamless" / "frictionless" (overused tech jargon)

### Competitor Stance:
- Stay generic. Never name other apps.
- Frame as "better than just texting" not "better than WhatsApp/iMessage."
- Position as *different category*, not *better version* of existing tools.
- If comparison is necessary: "Unlike traditional calling apps..."

---

## CONTENT THEMES (Recurring Topics)

These themes should appear regularly across all content:

1. **The Loneliness Paradox**
   - Hyperconnected but lonelier than ever
   - Social media ≠ social connection
   - The irony of communication overload

2. **Texting is Transactional**
   - Efficient for logistics, empty for emotion
   - 20 messages to schedule one call
   - The illusion of staying in touch

3. **Call Anxiety is Real**
   - It's a design problem, not a personal failing
   - Blind calls create reasonable anxiety
   - Context removes the fear

4. **The Hidden Cost**
   - What we lose by not hearing each other's voices
   - Missed moments of genuine connection
   - Relationships slipping away slowly

5. **Spontaneous Connection**
   - How to stay close without scheduling everything
   - Permission to call without overthinking
   - Making "just checking in" feel normal again

6. **Boundaries Enable Connection**
   - Knowing duration makes saying "yes" easier
   - 10 minutes is doable, "unknown" isn't
   - Structure creates freedom

7. **The Moment of Clarity**
   - When you realize the problem exists
   - "Once you see it, you can't unsee it"
   - The obvious solution hiding in plain sight

---

## WHYHI PRO (B2B POSITIONING)

**For LinkedIn and Enterprise Content:**

### What It Is
WhyHi Pro helps service-based businesses increase pickup rates and strengthen customer relationships by adding context to outbound calls.

### Core Pitch
Calling works when it gets answered. WhyHi Pro shows customers *why* you're calling and *how long* it will take before they pick up—turning ambiguous interruptions into respectful, informed interactions.

### Key Industries
- **Home services:** plumbers, HVAC, contractors, property management
- **Real estate:** agents, brokers, lenders, coordinators
- **Insurance:** claims agents, adjusters, emergency response
- **Healthcare:** scheduling, patient outreach, care coordination
- **Financial services:** advisors, banking, retirement planning
- **Recruiting/staffing:** candidate engagement, scheduling
- **Transportation/logistics:** dispatch, delivery coordination

### Value Propositions
1. **Higher pickup rates** - Customers know what to expect, answer more readily
2. **Fewer missed connections** - Reduces phone tag loops and voicemail waste
3. **Stronger relationships** - Calls feel respectful, not intrusive
4. **Operational efficiency** - Clear intent leads to faster outcomes and better prioritization
5. **Measurable improvement** - Track pickup rates, time-to-reach, callback loops

### Messaging Angle for LinkedIn
"Professional relationships suffer when all you do is text back and forth. Calling works—when people actually pick up."

"Your sales team spends hours leaving voicemails. What if customers knew exactly why you were calling before they decided to answer?"

"Missed calls = missed revenue. WhyHi Pro helps your team get through to customers on the first try."

---

## TONE BY PLATFORM

### LinkedIn
- **Tone:** Professional but conversational (not corporate)
- **Focus:** Business relationships, sales, customer success, WhyHi Pro
- **Themes:** ROI, efficiency, relationship quality, pickup rates
- **Length:** 150-250 words
- **CTA:** Soft invitation to consider or discuss ("What if calls worked differently?")
- **Example hook:** "Sales reps know this: calling works. Getting someone to pick up? That's the hard part."

### Instagram
- **Tone:** Personal, relatable, visual storytelling
- **Focus:** Use case scenarios, emotional connection, friendship
- **Themes:** Life moments, spontaneous connection, staying close
- **Length:** 80-150 words (punchy captions)
- **CTA:** Question to audience ("When's the last time you called instead of texted?")
- **Example hook:** "Why do we overthink calling our best friend?"

### Facebook
- **Tone:** Warm, community-focused, family-oriented
- **Focus:** Parenting scenarios, life logistics, friendship maintenance
- **Themes:** Busy parent life, coordinating, staying connected
- **Length:** 100-200 words
- **CTA:** Tag a friend or share a relatable moment
- **Example hook:** "You have 30 minutes until soccer practice. Your best friend calls. Do you pick up?"

---

## VULNERABILITY & PERSONAL NARRATIVE

### Founder Story (Use Sparingly - 1-2 Posts Max)

"I invented WhyHi because I realized close friends were slipping away. I was keeping in touch through texting, but I didn't feel close to them. I found myself finding reasons not to call them—or not to pick up when they called. I didn't understand why until I realized it was the lack of context. Phone calls feel blind. They're open-ended impositions. I built WhyHi to fix that—for myself first, and now for everyone."

### Usage Guidelines
- Reserve this for authentic "why I built this" content
- Use when establishing credibility or connecting on personal level
- Maximum 1-2 posts with this level of personal vulnerability
- Most content should stay observational and universal, not personal
- Can reference personal experience without full story: "I used to avoid calls from my best friend..."

---

## ANTI-PATTERNS (What COS Must NEVER Generate)

### Content to Avoid

❌ **Don't cite academic studies in social content**
- Save research/citations for investor decks and press materials
- Social content should feel conversational, not academic
- Example of what NOT to do: "According to a 2023 study in the Journal of Social Psychology..."

❌ **Don't name competitors**
- "Better than texting" not "better than iMessage"
- "Unlike traditional calling apps" not "unlike FaceTime"
- Position as different category, not improved version

❌ **Don't use clinical language**
- "Makes calls less stressful" not "reduces anxiety"
- "Predictable interactions" not "anxiety management tool"
- Not a medical device, it's better design

❌ **Don't hard-sell**
- No "download WhyHi now!" CTAs
- No "limited time offer" urgency
- Lead with insight, let value speak
- Soft invitations only: "There's a better way" or "Try it free"

❌ **Don't solve with platitudes**
- "Call more often!" doesn't help—WhyHi does
- Don't just say "stay connected"—show how WhyHi enables it
- Actionable solutions, not inspirational fluff

❌ **Don't claim medical benefits**
- Not "treats anxiety"—it's just better call design
- Not "therapeutic"—it's functional
- Not "clinically proven"—it's common sense

❌ **Don't use empty buzzwords**
- No "revolutionary," "disruptive," "paradigm shift"
- No "leverage synergies" or corporate speak
- Show the benefit directly, skip the hype

❌ **Don't be preachy or judgmental**
- Not "you should call more" (guilt)
- Not "people these days don't talk" (condescending)
- Observational and empathetic, not prescriptive

---

## CALL-TO-ACTION GUIDELINES

### Preferred CTAs (Soft Invitation)
- "There's a better way."
- "Try it free."
- "See how it works."
- "What if calls worked differently?"
- "Worth exploring."
- Tag a friend who gets it.
- When's the last time you [relatable action]?

### CTAs to Avoid (Too Sales-y)
- "Download now!"
- "Don't wait!"
- "Limited time offer!"
- "Sign up today!"
- "Join thousands of users!"
- Any sense of urgency or FOMO

### Platform-Specific CTAs

**LinkedIn:** Professional curiosity
- "Would this change how your team communicates with customers?"
- "How many voicemails does your sales team leave per day?"

**Instagram:** Social engagement
- "Tag someone who never picks up the phone 😅"
- "When's the last time you called instead of texted?"

**Facebook:** Community sharing
- "Share if you've felt this"
- "Tag a friend who needs this"

---

## CONTENT CADENCE & MIX

### Posting Frequency
- **Social Posts:** 3-4x per week across all platforms
- **Social Videos:** 1-2x per week (30-90 seconds)
- **Instructional Videos:** One-time creation (7 videos for onboarding drip)

### Content Mix for Social Posts
- **40%** Use Case Spotlights (relatable scenarios)
- **30%** Hidden Cost / Moment of Clarity (problem awareness)
- **20%** Educational (how WhyHi works)
- **10%** Personal / Founder Story

### Content Mix for Social Videos
- **50%** Use case reenactments (show problem + solution)
- **30%** Talking head (observational insights)
- **20%** Educational (how to use WhyHi)

### Platform Distribution
- **LinkedIn:** 2x/week (Tuesday morning, Thursday afternoon)
- **Facebook:** 1-2x/week (weekday evenings)
- **Instagram:** 2x/week (mix of posts and Reels)

### Pre-Launch Strategy
- Build content library of 20-30 posts + 10-15 videos BEFORE launch
- Schedule via Buffer so posting runs on autopilot
- Focus production time now, execution happens automatically later

---

## REVISION & EVOLUTION

### This Document is Living
- Brand Foundation evolves based on market feedback and performance data
- Tom will have weekly strategy sessions with WOS to refine messaging
- Agents always reference the CURRENT version of this document
- Updates should be committed to git with clear change notes

### When to Update
- **Monthly review:** Are core messages still resonating?
- **After performance analysis:** Which themes drive engagement?
- **After user feedback:** What language do actual users use?
- **Before major campaigns:** Ensure messaging is current

### How to Update
Tom can tell WOS: "Update Brand Foundation to [specific change]"
- WOS edits this markdown file
- Commits change with explanation
- Agents automatically use updated version

---

**END OF BRAND FOUNDATION**

Document 2: COS Content Playbook
File Path: /canon/cos_content_playbook.md
Content:
markdown# COS Content Playbook

**Version:** 1.0  
**Last Updated:** January 21, 2026  
**Purpose:** Operational guide for Content Drafter agent. Contains writing formulas, examples, frameworks, and community engagement guidelines.

---

## TABLE OF CONTENTS

- [Section A: Writing Formulas](#section-a-writing-formulas)
- [Section B: Use Case Library](#section-b-use-case-library)
- [Section C: Voice in Action (Example Posts)](#section-c-voice-in-action-example-posts)
- [Section D: Video Script Frameworks](#section-d-video-script-frameworks)
- [Section E: Instructional/Onboarding Video Scripts](#section-e-instructionalonboarding-video-scripts)
- [Section F: Community Engagement Frameworks](#section-f-community-engagement-frameworks)
- [Section G: Content Cadence & Scheduling](#section-g-content-cadence--scheduling)

---

## SECTION A: WRITING FORMULAS

These are proven structures for generating high-quality social content. Content Drafter should reference these when creating posts.

---

### Formula 1: Use Case Spotlight

**Structure:**
1. Set the scene (specific, relatable situation)
2. Show the friction (what goes wrong with current tools)
3. Reveal WhyHi solution (natural, not forced)
4. Land the insight (why this matters)

**When to Use:**
- When you have a concrete scenario from Use Case Library
- For Instagram/Facebook (visual storytelling)
- When demonstrating value without explaining features

**Example:**

"You're locked out of your friend's apartment. You need to ask where the spare key is. You're not going to text back and forth for 10 minutes—you need an answer NOW. So you call.

But your friend forgot you were coming. They see your call and think, 'Oh no, what's wrong? Do I have time for this?' So they don't pick up.

With WhyHi, you'd send a 5-minute 'Question' call. Your friend sees exactly what you need. They pick up. Problem solved in 2 minutes.

Once you experience this, you realize: every call should work this way."

**Formula Elements:**
- Opening: Immediate, specific scenario
- Conflict: Current tool failure (call ignored)
- Resolution: WhyHi solution (context shown)
- Insight: Universal realization

**Platform Adaptations:**
- **LinkedIn:** Professional scenario (client needs answer before meeting)
- **Facebook:** Parent scenario (coordinating pickup)
- **Instagram:** Friend scenario (shorter, punchier)

---

### Formula 2: The Hidden Cost

**Structure:**
1. Name what we've normalized (texting instead of calling)
2. Reveal the hidden cost (what we're losing)
3. Show the contrast (what live conversation gives us)
4. Soft invitation (there's a better way)

**When to Use:**
- For problem awareness content
- When audience might not realize the issue
- For LinkedIn (professional relationship angle)
- When you want reflective, not action-oriented tone

**Example:**

"We've gotten really good at texting back and forth. Twenty messages just to schedule a 30-minute call. It feels efficient. But is it?

What we don't realize: those 20 texts took 45 minutes spread across two days. And we still don't feel any closer.

A 5-minute call would've scheduled the thing AND let us hear each other's voice. That's what we're actually missing.

There's a better way."

**Formula Elements:**
- Acknowledgment: We do this (validate behavior)
- Question: But what's the real cost?
- Contrast: What we could have instead
- Invitation: Not a command, an offer

**Platform Adaptations:**
- **LinkedIn:** Focus on professional time waste
- **Facebook:** Focus on emotional cost (missing connection)
- **Instagram:** Visual contrast (texts vs call duration)

---

### Formula 3: The Moment of Clarity

**Structure:**
1. Present the universal behavior (we all do this)
2. Ask the revealing question (why DO we do this?)
3. Name the real reason (it's not us, it's the design)
4. Show the alternative

**When to Use:**
- When addressing call avoidance directly
- For audiences who already experience the problem
- When you want "aha moment" impact
- For video content (talking head style)

**Example:**

"Why don't we call people anymore?

It's not because we're too busy. We spend hours texting. It's not because we don't want connection—we're lonelier than ever.

It's because phone calls are blind. You don't know why someone's calling or how long it'll take. So it feels risky. So we text instead.

But what if calls weren't blind? What if you saw '10 min · Connection' before you answered?

You'd pick up."

**Formula Elements:**
- Universal question (we've all wondered this)
- Rule out false answers (not busy, not antisocial)
- True answer (design problem, not personal failing)
- Simple solution reveal

**Platform Adaptations:**
- **LinkedIn:** Professional version (missed opportunities)
- **Facebook:** Personal version (lost friendships)
- **Instagram:** Quick version (faster pacing)

---

### Formula 4: The Problem People Don't Know They Have

**Structure:**
1. Name something we've accepted as normal
2. Peel back the layer (but wait, that's actually broken)
3. Show how obvious it becomes once named
4. Position WhyHi as the clear solution

**When to Use:**
- For problem education content
- When targeting people who don't yet know they have the problem
- For launching new messaging angles
- When you want to shift perception

**Example:**

"We accept that no one picks up the phone anymore. That's just how it is now, right?

But think about it: when's the last time you answered a call from a friend without hesitation? When's the last time you called someone without overthinking it?

Phone calls are broken. Not because we don't want connection—but because we have no idea what we're signing up for when we answer.

The moment someone shows you WHY they're calling and HOW LONG they need, everything changes. Suddenly, picking up feels reasonable again.

That's WhyHi."

**Formula Elements:**
- Acceptance: We've normalized this
- Question: But is it actually okay?
- Reframe: The problem is the system, not people
- Solution: Simple change, dramatic impact

**Platform Adaptations:**
- **LinkedIn:** Professional communication breakdown
- **Facebook:** Personal relationships suffering
- **Instagram:** Quick realization moment

---

## SECTION B: USE CASE LIBRARY

**Purpose:** Concrete, relatable scenarios for content generation. Content Drafter references these when creating posts/videos.

**How to Use:**
- Each use case = potential post or video
- Cluster themes for weekly content series
- Reference specific scenarios in Use Case Spotlight formula
- Mix clusters to avoid repetition

---

### Cluster 1: Everyday Logistics & Quick Questions

**Theme:** "I just need an answer—fast."

**WhyHi Message:** "When a call should take 5 minutes, it finally does."

**Marketing Angle:** Efficiency, time-saving, reducing friction for quick coordination

**Use Cases:**

1. **Locked out, can't find the key** → 5 min · Question
   - *Scenario:* At friend's door, need spare key location immediately
   - *Friction:* Texting "where's the key?" takes too long, calling feels like an imposition
   - *WhyHi Win:* 5-min Question call gets answered, problem solved in 2 minutes

2. **One quick answer before a meeting** → 5 min · Question
   - *Scenario:* About to walk into presentation, need to verify one detail from coworker
   - *Friction:* Text might not get seen in time, call feels interruptive
   - *WhyHi Win:* Coworker sees "5 min Question," knows it's urgent and quick, picks up

3. **Babysitter is late** → 5 min · Question
   - *Scenario:* Need ETA from babysitter to adjust plans
   - *Friction:* Texts back and forth while juggling kids
   - *WhyHi Win:* Quick call gets immediate answer, no message thread

4. **Utility bill confusion** → 5 min · Question
   - *Scenario:* Roommate needs to know which utility company to pay
   - *Friction:* Trying to explain via text is clunky
   - *WhyHi Win:* 5-minute call clarifies everything at once

5. **Coordinating dinner pickup** → 5 min · Planning
   - *Scenario:* Partner needs to know what to grab on way home
   - *Friction:* Texting menu options back and forth is tedious
   - *WhyHi Win:* Quick planning call makes decision in real-time

6. **Calendar mix-up** → 5 min · Question
   - *Scenario:* Confused about meeting time, need clarification
   - *Friction:* Email thread is getting confusing
   - *WhyHi Win:* 5-minute call sorts it out instantly

7. **Package delivery question** → 5 min · Question
   - *Scenario:* Neighbor asking if you received their package
   - *Friction:* Back-and-forth texts about package details
   - *WhyHi Win:* Quick call confirms or not, done

8. **Checking availability later** → 5 min · Planning
   - *Scenario:* Want to know if friend is free tonight
   - *Friction:* Text "are you free?" leads to 10-message thread
   - *WhyHi Win:* 5-minute call schedules plans immediately

9. **Where did I park?** → 5 min · Question
   - *Scenario:* At crowded event, can't remember parking location
   - *Friction:* Trying to describe via text is confusing
   - *WhyHi Win:* Quick call gets directions right away

10. **Clarifying a misunderstanding** → 10 min · Question
    - *Scenario:* Text was misinterpreted, need to clear the air
    - *Friction:* More texting makes it worse
    - *WhyHi Win:* 10-minute call resolves tone issues immediately

---

### Cluster 2: Connection & Relationship Maintenance

**Theme:** "I want to talk—but I don't want to interrupt."

**WhyHi Message:** "Stay close without overstepping."

**Marketing Angle:** Permission to connect, spontaneous intimacy, low-commitment check-ins

**Use Cases:**

1. **Checking in with dad** → 10 min · Connection
   - *Scenario:* Haven't talked in a week, want to hear how he's doing
   - *Friction:* Calling feels like it needs a reason, might catch him at bad time
   - *WhyHi Win:* He sees "10 min Connection," knows it's just checking in, picks up when free

2. **Calling mom on lunch break** → 10 min · Connection
   - *Scenario:* Have 15 minutes between meetings, perfect time for quick catch-up
   - *Friction:* If she doesn't pick up, feels like wasted opportunity
   - *WhyHi Win:* She sees duration, knows it fits her schedule too

3. **Catching up with college friend** → 20 min · Connection
   - *Scenario:* Haven't talked in months, want to reconnect
   - *Friction:* Calling feels like huge commitment, keeps getting postponed
   - *WhyHi Win:* 20 minutes feels doable, actually happens

4. **Quick call to your kid** → 5 min · Connection
   - *Scenario:* Kid is at school/camp, just want to say hi
   - *Friction:* Don't want to interrupt their day
   - *WhyHi Win:* They see "5 min Connection from Mom/Dad," can pick up between activities

5. **Thinking-of-you walk call** → 10 min · Connection
   - *Scenario:* On a walk, friend pops into mind
   - *Friction:* Spontaneous calls feel presumptuous
   - *WhyHi Win:* Friend sees intention, knows it's casual, can choose to pick up

6. **Between school pickup and practice** → 10 min · Connection
   - *Scenario:* Parent has 15 minutes in car, perfect for quick friend call
   - *Friction:* Friend might not answer random call
   - *WhyHi Win:* Friend sees "10 min Connection," knows it's doable right now

7. **Calling a parent to say goodnight** → 5 min · Connection
   - *Scenario:* End of day ritual with elderly parent
   - *Friction:* Sometimes they're already asleep or busy
   - *WhyHi Win:* They see it's just 5 minutes, can opt in or suggest morning call

8. **Checking in after silence** → 10 min · Connection
   - *Scenario:* Haven't heard from friend in a while, want to make sure they're okay
   - *Friction:* Calling might feel intrusive if they're going through something
   - *WhyHi Win:* They see caring intention, can respond when ready

9. **Thank-you call** → 5 min · Connection
   - *Scenario:* Friend did you a favor, want to say thanks properly
   - *Friction:* Text feels insufficient, call feels like burden
   - *WhyHi Win:* 5 minutes shows appreciation without asking for much time

10. **End-of-day "how was your day?"** → 10 min · Connection
    - *Scenario:* Partner/close friend, daily debrief ritual
    - *Friction:* Timing varies, don't want to interrupt their evening
    - *WhyHi Win:* They see it's routine connection, can join when winding down

11. **Reconnecting with old coworker** → 20 min · Connection
    - *Scenario:* Saw their LinkedIn post, reminded you to reach out
    - *Friction:* Calling out of the blue feels awkward after years
    - *WhyHi Win:* 20-minute catch-up feels appropriate, not too short or too long

12. **Old friend calls while between errands** → 10 min · Connection
    - *Scenario:* Running errands, have 15-minute window
    - *Friction:* Answering unknown-length call might make you late
    - *WhyHi Win:* See it's 10 minutes, know you have time, pick up

13. **Friend driving, can only talk briefly** → 5 min · Connection
    - *Scenario:* Friend on commute, wants quick chat
    - *Friction:* You don't know they're driving and only have a few minutes
    - *WhyHi Win:* You see 5 minutes, know it's short window, make it count

---

### Cluster 3: Emotional Support & Care

**Theme:** "I need to be there—but I don't know how long it will take."

**WhyHi Message:** "Support, with boundaries."

**Marketing Angle:** Being there for people, emotional availability without burnout, structured care

**Use Cases:**

1. **Partner overwhelmed at work** → 20 min · Support
   - *Scenario:* Partner texts "rough day," needs to vent
   - *Friction:* Calling back immediately might catch them in meeting, timing unclear
   - *WhyHi Win:* 20-minute Support call signals "I'm here," they pick up when ready

2. **Breakup support** → 30 min · Support
   - *Scenario:* Friend just went through breakup, needs to talk
   - *Friction:* Open-ended call feels daunting when you have limited availability
   - *WhyHi Win:* 30 minutes feels generous but bounded, you can plan around it

3. **Post-surgery check-in** → 10 min · Support
   - *Scenario:* Friend had minor surgery, want to see how they're doing
   - *Friction:* Don't know if they're up for talking, how long they can talk
   - *WhyHi Win:* They see duration, can decline if too tired or accept if feeling okay

4. **Job decision support** → 20 min · Support
   - *Scenario:* Friend needs help thinking through job offer
   - *Friction:* This could turn into hour-long conversation, you're not sure you have time
   - *WhyHi Win:* 20 minutes gives space to talk through it without open-ended commitment

5. **Family event debrief** → 20 min · Support
   - *Scenario:* Sibling needs to process difficult family gathering
   - *Friction:* These conversations can spiral, hard to contain
   - *WhyHi Win:* Time boundary helps both of you stay focused and supportive

6. **After a bad exam** → 10 min · Support
   - *Scenario:* Kid/friend bombed a test, needs encouragement
   - *Friction:* Want to be there but also don't want to dwell too long
   - *WhyHi Win:* 10 minutes is perfect for pep talk without over-processing

7. **Pre-presentation nerves** → 5 min · Support
   - *Scenario:* Friend about to give big presentation, needs quick reassurance
   - *Friction:* Long call might make them more nervous, but want to help
   - *WhyHi Win:* 5-minute boost gives confidence without eating into prep time

8. **Friend moving to new city** → 10 min · Support
   - *Scenario:* Friend in midst of stressful move, feeling overwhelmed
   - *Friction:* Want to check in but don't want to add to their stress
   - *WhyHi Win:* 10 minutes shows care without demanding too much during chaos

9. **Reassurance after hard conversation** → 20 min · Support
   - *Scenario:* Friend had difficult talk with family member, needs processing
   - *Friction:* These can become therapy sessions, you're not equipped for that
   - *WhyHi Win:* 20 minutes gives space to support without becoming therapist

10. **Nervous first day** → 5 min · Support
    - *Scenario:* Kid's first day at new school, quick check-in before start
    - *Friction:* They're nervous but also trying to get ready
    - *WhyHi Win:* 5-minute encouragement call doesn't add to morning rush

11. **Talking through tough decision** → 20 min · Support
    - *Scenario:* Friend needs sounding board for major life choice
    - *Friction:* Don't want to give advice too quickly, but also can't talk for hours
    - *WhyHi Win:* 20 minutes is enough to explore without forcing resolution

---

### Cluster 4: News & Life Updates

**Theme:** "This matters—but it doesn't need an hour."

**WhyHi Message:** "Share the moment—without the pressure."

**Marketing Angle:** Celebrating together, sharing important moments, being present for milestones

**Use Cases:**

1. **Sharing good news (got the job)** → 5 min · News
   - *Scenario:* Just got job offer, want to tell friend/parent immediately
   - *Friction:* Texting doesn't capture excitement, but don't want long recap
   - *WhyHi Win:* 5-minute News call lets them hear joy in your voice, celebrate quickly

2. **Arrived safely** → 5 min · News
   - *Scenario:* Got home from trip, promised to let parent/partner know
   - *Friction:* Text is impersonal, call might turn into long trip recap
   - *WhyHi Win:* 5 minutes confirms arrival plus quick highlight

3. **Big life announcement** → 10 min · News
   - *Scenario:* Engaged, pregnant, moving—major life change to share
   - *Friction:* This deserves live conversation but timing is tricky
   - *WhyHi Win:* 10-minute window lets friend/family react and ask questions

4. **Unexpected good news** → 5 min · News
   - *Scenario:* Got surprise promotion, won award, received good medical results
   - *Friction:* Want to share NOW but don't want to interrupt their day
   - *WhyHi Win:* 5 minutes of "you won't believe this!" excitement

5. **Plans changed** → 5 min · News
   - *Scenario:* Tonight's plans shifted, need to update friend
   - *Friction:* Text thread might miss details, call feels excessive
   - *WhyHi Win:* Quick call clarifies new plan instantly

6. **Sharing difficult news gently** → 10 min · News
   - *Scenario:* Have to share bad news (pet died, job loss, health scare)
   - *Friction:* Text is too impersonal, but don't want to trap them in long call
   - *WhyHi Win:* 10 minutes lets you share with care, they can process and respond

7. **Running late, heads-up** → 5 min · News
   - *Scenario:* Traffic or delay, need to let people know you're behind schedule
   - *Friction:* Text might not be seen in time
   - *WhyHi Win:* Quick call ensures they get update and can adjust plans

---

### Cluster 5: Planning & Coordination

**Theme:** "Let's figure this out—clearly."

**WhyHi Message:** "Calls with an agenda—minus the formality."

**Marketing Angle:** Efficiency, real-time problem-solving, group coordination

**Use Cases:**

1. **Holiday plans** → 10 min · Planning
   - *Scenario:* Family coordinating Thanksgiving/Christmas logistics
   - *Friction:* Group text becomes chaotic, email is too formal
   - *WhyHi Win:* 10-minute call with key people makes decisions quickly

2. **Surprise party coordination** → 30 min · Planning
   - *Scenario:* Planning friend's birthday, multiple people need to coordinate
   - *Friction:* Texts miss nuance, scheduling in-person meeting is hard
   - *WhyHi Win:* 30-minute planning call knocks out major decisions

3. **Travel pickup** → 10 min · Planning
   - *Scenario:* Friend arriving at airport, coordinating pickup logistics
   - *Friction:* Texting while navigating traffic is dangerous
   - *WhyHi Win:* 10-minute call while friend walks to pickup spot

4. **Family decision** → 10 min · Planning
   - *Scenario:* Siblings need to decide on parent care, house repairs, etc.
   - *Friction:* Text thread goes nowhere, everyone has different opinions
   - *WhyHi Win:* 10-minute call forces real discussion and decision

5. **Weekend trip planning** → 30 min · Planning
   - *Scenario:* Friends coordinating weekend getaway (dates, location, lodging)
   - *Friction:* Endless group chat, no decisions made
   - *WhyHi Win:* 30-minute call with key people locks in plans

6. **Childcare handoff** → 10 min · Planning
   - *Scenario:* Co-parents coordinating pickup/dropoff changes
   - *Friction:* Text miscommunication leads to confusion
   - *WhyHi Win:* 10-minute call confirms details, no ambiguity

7. **Short call while driving** → 5 min · Connection
   - *Scenario:* On commute, perfect time for quick catch-up
   - *Friction:* Other person doesn't know you're driving and have limited time
   - *WhyHi Win:* 5-minute duration sets clear expectation

8. **Availability check** → 5 min · Planning
   - *Scenario:* Want to know if friend is free for dinner/movie later
   - *Friction:* "Are you free tonight?" text turns into 15-message thread
   - *WhyHi Win:* 5-minute call makes plan or not, no back-and-forth

---

### Cluster 6: True Emergencies

**Theme:** "This is urgent. Please pick up."

**WhyHi Message:** "When it really matters, they know."

**Marketing Angle:** Urgency signaling, peace of mind, being there in crisis

**Use Cases:**

1. **Neighbor's dog got loose** → 5 min · Emergency
   - *Scenario:* Saw neighbor's dog running down street, need to alert them NOW
   - *Friction:* Text might not be seen immediately
   - *WhyHi Win:* Emergency flag + 5 minutes signals "pick up right now"

2. **Lost phone/wallet panic** → 5 min · Emergency
   - *Scenario:* Can't find phone/wallet, need help retracing steps
   - *Friction:* This is time-sensitive, texting delays response
   - *WhyHi Win:* Emergency call gets immediate attention

3. **Stranded on the roadside** → 5 min · Emergency
   - *Scenario:* Car broke down, need pickup or help ASAP
   - *Friction:* Text doesn't convey urgency, AAA call takes forever
   - *WhyHi Win:* Friend sees Emergency + location, responds immediately

**Note on Emergencies:**
- These use cases are rare but important
- WhyHi's value here is urgency signaling
- Marketing angle: "When it's really urgent, they'll know"
- Don't overuse Emergency examples (makes app seem crisis-focused)

---

## SECTION C: VOICE IN ACTION (Example Posts)

**Purpose:** Demonstrate Tom's voice through complete example posts. Content Drafter should reference these to match tone, style, and energy.

---

### Example 1: Use Case Spotlight (Instagram)

**Platform:** Instagram  
**Format:** Carousel (3 slides)  
**Use Case:** Locked out scenario  
**Formula:** Use Case Spotlight

**Caption:**

"You're about to walk into a meeting but you need one quick answer from your coworker. Do you:

A) Text and wait 20 minutes for a response  
B) Call and hope they're free

With WhyHi, you send a '5 min · Question' call. They see exactly what you need. They pick up. You get your answer. Meeting starts on time.

Once you experience this, you can't go back."

**Slide 1 Text:** "You need a quick answer"  
**Slide 2 Text:** "But you don't want to interrupt"  
**Slide 3 Text:** "'5 min · Question' changes everything"

**Why This Works:**
- Opens with relatable scenario (A/B choice)
- Shows friction (texting delay, call uncertainty)
- WhyHi solution feels natural, not forced
- Ending is aspirational without being sales-y
- Short, punchy, Instagram-appropriate length

---

### Example 2: The Hidden Cost (LinkedIn)

**Platform:** LinkedIn  
**Format:** Text post (no image)  
**Theme:** Professional relationships  
**Formula:** The Hidden Cost

**Post:**

"How many texts does it take to schedule a 30-minute call?

In my experience: about 20 messages spread across two days.

'When are you free?'  
'Tuesday or Thursday?'  
'Morning or afternoon?'  
'10am work?'  
'Actually can we do 11?'

We think texting is efficient. But is it?

A 5-minute call would've scheduled the thing AND given you a chance to actually connect. That's what we're missing.

Professional relationships suffer when all you do is message back and forth. There's a better way."

**Why This Works:**
- Leads with specific question (hooks attention)
- Real scenario (everyone has experienced this)
- Doesn't explain WhyHi explicitly (lets insight do the work)
- Professional tone but conversational
- Soft CTA ("there's a better way" not "download now")
- No emojis (LinkedIn appropriate)

---

### Example 3: The Moment of Clarity (Facebook)

**Platform:** Facebook  
**Format:** Text post  
**Theme:** Personal relationships  
**Formula:** The Moment of Clarity

**Post:**

"Why don't we call people anymore?

It's not that we're too busy. We spend hours texting.

It's not that we don't want connection. We're lonelier than ever.

It's because phone calls are blind. You don't know why someone's calling or how long it'll take. So it feels risky.

But what if you saw '10 min · Connection' before you answered?

You'd pick up. I would. We all would.

That's the idea behind WhyHi."

**Why This Works:**
- Universal question (we've all wondered this)
- Rules out false explanations (builds to real answer)
- "Blind calls" language (clear problem naming)
- Simple solution reveal (not feature dump)
- Inclusive language ("we all would")
- Ends with soft brand introduction
- Appropriate length for Facebook

---

### Example 4: Professional Use Case (LinkedIn)

**Platform:** LinkedIn  
**Format:** Text post  
**Theme:** WhyHi Pro / B2B  
**Formula:** Use Case Spotlight

**Post:**

"Your field tech needs to call a customer about a delayed appointment.

The customer sees an unknown number. Thinks: 'Spam? Bill collector? Do I have time for this?'

They don't pick up. Your tech leaves a voicemail. The customer calls back two hours later when your tech is at another job. Phone tag begins.

Now imagine: the customer sees 'ABC Plumbing: 5 min · Appointment Update' before their phone even rings.

They know exactly what it is. They pick up. Issue resolved in 2 minutes. Next appointment confirmed. Customer feels respected.

That's how WhyHi Pro turns missed calls into completed conversations.

Calling works—when people actually pick up."

**Why This Works:**
- B2B scenario (service business)
- Shows real cost (phone tag, lost time)
- WhyHi Pro solution is clear value (higher pickup rate)
- Professional tone with stakes
- Ends with memorable tagline
- Implies ROI without being salesy

---

### Example 5: Short Instagram Caption

**Platform:** Instagram  
**Format:** Single image post (person looking at phone)  
**Theme:** Connection  
**Formula:** Simple observation

**Caption:**

"When's the last time you called your best friend?

Not texted. Called.

Heard their voice. Laughed together. Felt close.

WhyHi makes calling feel easy again."

**Why This Works:**
- Opens with question (engagement)
- Distinction between texting and calling
- Emotional payoff (laughed, felt close)
- Direct but not pushy
- Short (Instagram sweet spot: 80-100 words)

---

## SECTION D: VIDEO SCRIPT FRAMEWORKS

**Purpose:** Templates for creating video scripts. Content Drafter uses these when approved idea is video format.

---

### Framework 1: Talking Head (Use Case)

**Length:** 30-60 seconds  
**Format:** Direct to camera, conversational  
**Best For:** Quick use case demonstrations, relatable scenarios

**Structure:**
1. **Hook (0-3 sec):** Relatable scenario, immediate grab
2. **Setup (4-15 sec):** Show the friction with current approach
3. **WhyHi Reveal (16-40 sec):** How it works differently (show phone if possible)
4. **Closer (41-60 sec):** "Once you see it, you can't unsee it" style insight

**Example Script: Locked Out Scenario**
```
[0-3s - Direct to camera, energetic]
"You're locked out. You need to call your friend for the spare key."

[4-15s - Expressive, showing frustration]
"But you know they're at work. They see your call and think, 'Do I have time for this?' They don't pick up. Now you're stuck outside."

[16-40s - Hold up phone, show WhyHi interface]
"With WhyHi, you send a 5-minute 'Question' call. They see exactly what you need before they answer. They pick up. You get the key. Done."

[41-60s - Back to direct eye contact]
"Once you know calls can work this way, going back feels insane."
```

**Storyboard Notes:**
- **Shot 1:** Talking head, medium close-up, casual setting (home/office)
- **Shot 2:** Optional B-roll of frustrated person at door (or stay on talking head)
- **Shot 3:** Close-up of phone showing "5 min · Question" on WhyHi interface
- **Shot 4:** Return to talking head, confident/satisfied expression
- **Text Overlay at 20s:** "5 min · Question" (sync with phone reveal)
- **End Screen:** WhyHi logo + "Try it free" (small, unobtrusive)

**Platform Adaptations:**
- **Instagram Reel:** Cut to 45 seconds, faster pacing
- **TikTok:** Add trending audio, more energetic delivery
- **YouTube Short:** Keep at 60 seconds, can be slightly more explanatory
- **LinkedIn:** Keep professional examples, tone down hand gestures slightly

---

### Framework 2: Scenario Reenactment

**Length:** 45-90 seconds  
**Format:** Act out the scenario (can be solo with voiceover or simple acting)  
**Best For:** Showing before/after, emotional impact, visual storytelling

**Structure:**
1. **Old Way (0-25s):** Show frustration with current tools (texting, ignored calls)
2. **Transition (26-35s):** "But what if..." or "There's a better way..."
3. **WhyHi Way (36-70s):** Show relief, clarity, problem solved
4. **Reflection (71-90s):** Talking head wrap-up, "This is how calls should work"

**Example Script: Texting vs. Calling**
```
[0-25s - Acting/B-roll: Person texting, looking frustrated]
VOICEOVER: "When are you free?"
[Text bubble appears on screen: "When are you free?"]

VOICEOVER: "Tuesday or Thursday?"
[Another text bubble: "Tuesday or Thursday?"]

[Person sighs, puts phone down, exasperated]

VOICEOVER: "Twenty texts later, you're still trying to schedule one call."

[26-35s - Transition: Person picks up phone again, thoughtful look]
VOICEOVER: "Or... you could just send a 10-minute 'Planning' call and figure it out in real time."

[36-70s - Acting: Person initiates WhyHi call, show interface]
[Show phone screen: "10 min · Planning" ]
[Person smiles, speaks briefly (we don't hear audio, just see them talking)]
[Person hangs up, looks satisfied, gives thumbs up]

[71-90s - Switch to talking head]
"This is how calls should work. You know what you need, they know what they're signing up for. Done."
```

**Storyboard Notes:**
- **Scene 1:** Sitting at desk/table, phone in hand, texting animation overlays
- **Scene 2:** Put phone down, frustrated gesture (hand on forehead, etc.)
- **Scene 3:** Pick up phone again, open WhyHi app
- **Scene 4:** Screen recording of WhyHi interface setting intention + duration
- **Scene 5:** Act out brief call (can be silent or vague audio)
- **Scene 6:** Satisfied close (smile, nod, move on with day)
- **Scene 7:** Direct to camera for final insight
- **Graphics:** Text bubbles for texts, WhyHi interface overlay, arrow showing "before → after"

---

### Framework 3: Educational/Explainer

**Length:** 60-90 seconds  
**Format:** Screen recording + voiceover OR talking head with graphics  
**Best For:** Explaining how WhyHi works, feature demonstrations, onboarding content

**Structure:**
1. **Problem Statement (0-15s):** What's broken about current calls
2. **WhyHi Introduction (16-30s):** Here's how we fix it
3. **Feature Demo (31-70s):** Show the app in action (screen recording)
4. **Call to Action (71-90s):** Try it yourself

**Example Script: How WhyHi Works**
```
[0-15s - Talking head OR voiceover over generic phone footage]
"Phone calls are broken. No one picks up because we don't know what we're signing up for."

[16-30s - Talking head continues OR transition to screen recording]
"WhyHi fixes this. Before you call, you set two things: how long you need, and why you're calling."

[31-70s - Screen recording of WhyHi app]
[Show: Opening app]
VOICEOVER: "Here's how it works. Open WhyHi, select your contact."

[Show: Selecting duration]
VOICEOVER: "Choose your call duration: 5, 10, 20, or 30 minutes."

[Show: Selecting intention]
VOICEOVER: "Choose your intention: Connection, Question, Planning, or Support."

[Show: Initiating call]
VOICEOVER: "When I call you, you see '10 min · Connection' before you answer. Now you know you have time. So you pick up."

[71-90s - Return to talking head OR end on app screen]
"That's it. Calls with context. Try it free."
[Show: WhyHi logo + download link]
```

**Storyboard Notes:**
- **Option A (Talking Head + Graphics):**
  - Talking head for intro and outro
  - Animated graphics showing "call intention" and "call duration" concepts
  - Screen recording in middle section

- **Option B (Full Screen Recording):**
  - Voiceover throughout
  - Clean screen recording of app flow
  - Highlight UI elements with arrows/circles
  - Text captions for key points

- **Graphics:**
  - "Before WhyHi" vs "After WhyHi" split screen
  - Icons for each intention (Connection, Question, etc.)
  - Clock icon for duration visualization

---

## SECTION E: INSTRUCTIONAL/ONBOARDING VIDEO SCRIPTS

**Purpose:** Evergreen product education videos delivered via in-app drip campaign, YouTube, Help Center.

**Tone:** Clear, helpful, concise (not marketing-heavy). Focus on user success, not selling.

**Format:** Screen recording + voiceover OR talking head with screen recording inserts.

**Note:** These are EXAMPLE scripts demonstrating the pattern. More can be added as needed through conversations with WOS.

---

### Video 1: Welcome to WhyHi

**Length:** 60-90 seconds  
**Audience:** New users, first app open  
**Goal:** Orient user to core concept

**Script:**
```
[0-10s - App logo animation or talking head]
"Welcome to WhyHi."

[11-30s - Screen recording: App home screen]
"WhyHi makes phone calls better by adding two things: intention and duration.

Before you call someone, you tell them why you're calling and how long you need. They see this before they answer."

[31-50s - Screen recording: Incoming call view]
"So instead of wondering 'Do I have time for this?' they know exactly what you need."

[51-70s - Talking head or continue screen recording]
"This makes calling feel easy again—for both of you."

[71-90s - Outro]
"In the next few videos, we'll show you how to make your first call, set your intentions, and get your friends on WhyHi.

Let's get started."
```

**Visual Elements:**
- Show app home screen (clean, simple)
- Highlight "intention" and "duration" selectors
- Show incoming call view with context displayed
- Use simple animations (arrows, highlights) to draw attention
- Keep text overlays minimal, let voiceover guide

---

### Video 2: How to Make Your First WhyHi Call

**Length:** 45-60 seconds  
**Audience:** New users, onboarding flow  
**Goal:** Guide through first call experience

**Script:**
```
[0-5s - Title card or talking head]
"Here's how to make your first WhyHi call."

[6-55s - Screen recording with voiceover]
"Step 1: Open WhyHi and tap the contact you want to call.

Step 2: Choose your call duration: 5, 10, 20, or 30 minutes.

Step 3: Choose your intention: Connection, Question, Planning, or Support.

Step 4: Tap 'Call.'

Your friend sees your intention and duration before they pick up. If they can't talk now, they can tap 'Call back in 1 hour' and WhyHi will remind them both.

That's it. You just made your first intentional call."

[56-60s - Confirmation screen or talking head]
"Easy, right? Now let's talk about what happens when you call someone who doesn't have WhyHi yet."
```

**Visual Elements:**
- Clear screen recording of each step
- Highlight buttons/selectors as they're mentioned
- Show incoming call view (recipient perspective)
- Show callback option interface
- Use numbered steps overlay (1, 2, 3, 4)

---

### Video 3: What Happens When You Call Someone Who Doesn't Have WhyHi

**Length:** 60 seconds  
**Audience:** New users worried about network effects  
**Goal:** Explain hybrid calling (WhyHi → cellular bridge)

**Script:**
```
[0-10s - Talking head or title card]
"What if you have WhyHi but your friend doesn't? No problem."

[11-35s - Screen recording + phone SMS screenshot]
"When you call them, WhyHi does two things:

First, it sends them a text message that says '[Your name] is calling for 10 min to connect!'

Then, their phone rings like a normal call."

[36-50s - Talking head or illustration]
"They see the text, understand why you're calling, and they're way more likely to pick up.

After the call, they usually ask, 'Wait, how did you do that?' That's when you tell them about WhyHi."

[51-60s - Outro]
"Your calls become your best marketing. Next up: how to set call intentions and durations."
```

**Visual Elements:**
- Show SMS preview (actual text message format)
- Show cellular call coming in simultaneously
- Use split-screen: sender view vs recipient view
- Simple animation of message → ring sequence

---

### Video 4: How to Set Call Intentions & Durations

**Length:** 45 seconds  
**Audience:** New users, feature education  
**Goal:** Explain when to use each intention

**Script:**
```
[0-10s - Talking head or screen recording]
"WhyHi has four call intentions:

Connection – catching up, checking in  
Question – need a quick answer  
Planning – coordinating schedules  
Support – someone needs to talk"

[11-30s - Continue]
"And four durations: 5, 10, 20, or 30 minutes.

Pick what feels right. If you're not sure, start with 10 minutes and Connection. You can always adjust."

[31-45s - Outro]
"The goal isn't to be perfect—it's to give the other person context so they can say yes.

Next: tips for getting your friends to download WhyHi."
```

**Visual Elements:**
- Show all four intentions with icons
- Show duration selector with time options
- Brief visual example for each intention (icon + text description)
- Keep simple, not overwhelming

---

### Video 5: Tips for Getting Friends to Download WhyHi

**Length:** 60 seconds  
**Audience:** Engaged users wanting to grow their network  
**Goal:** Provide social proof strategies

**Script:**
```
[0-5s - Talking head]
"Want your friends on WhyHi? Here's what works:"

[6-25s - Point 1]
"1. Just use it. When you call them, they'll get that text with your intention and duration. They'll ask about it."

[26-40s - Point 2]
"2. Tell them the truth: 'I got tired of phone tag. This app lets me say exactly what I need so you know if you have time.'"

[41-55s - Point 3]
"3. Share this video. Send them a link and say, 'Check this out—I think you'd love it.'"

[56-60s - Outro]
"The more people in your circle using WhyHi, the easier it is to stay connected.

And that's the whole point."
```

**Visual Elements:**
- Numbered list overlay (1, 2, 3)
- Show example text message inviting friend
- Show share button in app
- Keep conversational, friendly tone

---

### Video 6: Managing Your Contacts & Favorites

**Length:** 30-45 seconds  
**Audience:** Active users, feature discovery  
**Goal:** Explain contact management features

**Script:**
```
[0-10s - Screen recording]
"You can add anyone to WhyHi—even if they don't have the app yet.

Tap 'Add Contact' and pull from your phone's contact list."

[11-25s - Continue screen recording]
"Mark your closest people as 'Favorites' so they're easy to find.

When you call a favorite, WhyHi remembers your usual call type. So if you always do 10-minute catch-ups with your mom, it'll suggest that next time."

[26-45s - Outro]
"Small things that make calling easier. Next up: frequently asked questions."
```

**Visual Elements:**
- Show contact import flow
- Show favorites list (star icon)
- Show suggestion feature (remembered preferences)
- Clean, simple UI walkthrough

---

### Video 7: FAQ / Common Questions

**Length:** 90 seconds  
**Audience:** New and existing users  
**Goal:** Address common concerns/confusion

**Script:**
```
[0-10s - Talking head]
"Quick answers to common questions:"

[11-25s - Q1]
"Q: Does the other person need WhyHi?  
A: Nope. If they don't have it, they'll get a text with your intention and then a regular call."

[26-40s - Q2]
"Q: What if I need more than 30 minutes?  
A: You can extend the call once you're talking. The duration is just a starting agreement."

[41-55s - Q3]
"Q: Can I decline a call without being rude?  
A: Yes. Tap 'Call back in 1 hour' and WhyHi will remind you both."

[56-70s - Q4]
"Q: Is this just for personal calls?  
A: It works for everything—friends, family, work, clients. Anywhere you want clear communication."

[71-85s - Q5]
"Q: How much does it cost?  
A: WhyHi is free. Always will be for personal use."

[86-90s - Outro]
"Any other questions? Hit us up in the app."
```

**Visual Elements:**
- Split screen: Q on left, A on right
- Show relevant app features for each answer
- Keep pacing quick (15 seconds per Q&A)
- End with "Contact Support" button shown

---

## SECTION F: COMMUNITY ENGAGEMENT FRAMEWORKS

**Purpose:** Guidelines for posting in niche communities and reaching out to aligned organizations.

---

### SUBREDDIT POSTING GUIDELINES

**Approved Subreddits for WhyHi:**

**Consumer/Personal Use:**
- r/Telephobia (highest fit - entire sub is the problem)
- r/autism, r/AutisticAdults, r/AutismInWomen
- r/ADHD, r/adhdwomen
- r/socialanxiety
- r/socialskills
- r/introvert
- r/AskWomenOver30
- r/LongDistance
- r/InternetIsBeautiful
- r/apps, r/iosapps, r/androidapps
- r/productivity

**Founder/Startup Angle:**
- r/Entrepreneur
- r/startups

---

### Universal Reddit Posting Rules

**DO:**
1. **Lead with the problem they already discuss**
   - Example: "I used to dread unexpected calls. Turns out, the problem wasn't me—it was the design."
   - NOT: "Check out my new app WhyHi!"

2. **Ask for feedback, don't hard-sell**
   - "I built this tool to help with [problem]. Would this help you?"
   - "Looking for beta testers who struggle with [pain point]."

3. **Be transparent about being the founder**
   - "Full disclosure: I made this because I had this exact problem."
   - Redditors respect honesty, hate stealth marketing

4. **Offer value before asking**
   - Share insight about the problem
   - Then mention WhyHi as one solution you built

5. **Use comment/DM for access**
   - "Comment 'BETA' and I'll DM you a link"
   - Keeps main post conversational, not promotional

**DON'T:**
1. Make medical/clinical claims ("reduces anxiety")
2. Post the same content across multiple subs in short time (looks like spam)
3. Argue with skeptics (respond once politely, then disengage)
4. Post without reading sub rules first (many have strict self-promo policies)
5. Delete and repost if first attempt flops (Reddit tracks this)

---

### Community-Specific Messaging Templates

#### r/Telephobia
**Lead:** "I used to avoid calls for weeks. Turns out, the uncertainty was the problem, not me."

**Frame:** Predictability tool, removes surprise element

**Avoid:** Clinical language ("cures phone anxiety")

**Example Post:**
```
Title: I fixed my phone anxiety by removing the one thing that made calls scary

I used to see an incoming call and immediately feel my chest tighten. Not because I don't like the person—because I had no idea what I was signing up for.

A 5-minute question? A 2-hour crisis? Was I interrupting their day by calling back?

I built WhyHi to solve this: before you call someone, you tell them how long you need and why you're calling. They see "10 min · Connection" before they answer.

Suddenly, picking up feels reasonable. You know what you're committing to.

I'm not saying it cures phone anxiety—it's not therapy. But for me, removing the uncertainty removed 90% of the dread.

Full disclosure: I'm the founder, building this because I needed it. Would this help anyone else here?
```

---

#### r/autism, r/AutisticAdults, r/AutismInWomen
**Lead:** "Phone calls felt impossible until I redesigned them as mini-agreements."

**Frame:** Boundary-first calling, reduces script uncertainty

**Avoid:** Othering language ("for people with autism"), focus on design not diagnosis

**Example Post:**
```
Title: How I made phone calls less overwhelming (by adding structure)

Unexpected phone calls were one of my worst nightmare scenarios. I never knew:
- Why they're calling
- How long it would take
- What script I was supposed to follow

So I'd either not answer, or answer and spend the whole call anxious about when I could end it.

I built WhyHi to add the structure I needed: before calling, you set intention + duration. The other person sees "15 min · Planning" before answering.

It's like a mini-agreement before the interaction starts. No surprises. Clear expectations.

Not a cure-all, but it's helped me actually stay in touch with people instead of avoiding calls for weeks.

Anyone else need this kind of structure to make communication manageable?

(Yes, I made this app—specifically for this problem.)
```

---

#### r/ADHD, r/adhdwomen
**Lead:** "I'd put off returning calls for days. Then I realized: I just needed to know how long they'd take."

**Frame:** Reduces activation energy, one-tap callback reminders

**Avoid:** "Fixes ADHD" (it doesn't), focus on executive function support

**Example Post:**
```
Title: The one change that made me actually return phone calls

My "call back [friend]" task would sit on my list for WEEKS because:
- What if they want to talk for an hour and I only have 10 minutes?
- What if they're calling about something heavy and I don't have the bandwidth?
- What if I call at a bad time and now I've wasted 20 minutes of anxiety?

I built WhyHi so calls come with context: "10 min · Question" or "20 min · Connection."

Now I know what I'm signing up for. The activation energy dropped from "impossible mountain" to "okay I can do 10 minutes."

Also: if I miss the call, one-tap "call back in 1 hour" sets a reminder for both of us.

Not saying it fixes ADHD (lol nothing does), but it removed the decision paralysis around phone calls.

Does anyone else have this exact problem?

(Built this for myself, figured others might need it too.)
```

---

#### r/socialanxiety
**Lead:** "Calls felt like ambushes. Turns out, they don't have to be."

**Frame:** Gentler, predictable interactions

**Avoid:** Medical/therapeutic claims

**Example Post:**
```
Title: What if phone calls weren't a surprise attack?

For years I thought I just "wasn't good at phone calls." Turns out, I'm fine at phone calls when I know what to expect.

The surprise is what kills me:
- Why are they calling?
- Do I have time for this?
- Is something wrong?

I made WhyHi so calls come with context BEFORE you answer. "5 min · Question" tells you everything you need to know.

It's not therapy. It's just... design that makes sense?

For me, it's the difference between avoiding calls for a week vs actually picking up.

Anyone else?

(Yes I made it, yes I'm biased, but I genuinely needed this to exist.)
```

---

#### r/socialskills
**Lead:** "How do you stay close to friends when everyone's busy? I tried this..."

**Frame:** Proactive connection tool, makes calling normal again

**Avoid:** Preaching ("you should call more")

**Example Post:**
```
Title: Making "just checking in" calls feel normal again

I noticed my close friendships were getting weaker because all we did was text. But calling felt like this big THING that required scheduling and reasons.

So I made WhyHi: before calling, you set a duration and intention. They see "10 min · Connection" before answering.

Suddenly it's not a big deal. They know:
- I'm not in crisis
- I'm not going to trap them in a 2-hour call
- I just want to catch up

And if they can't talk, they tap "call back later" and we both get reminded.

It's helped me actually stay in touch instead of letting months go by.

Has anyone else struggled with this? What's worked for you?

(Built this for myself, sharing in case it helps others.)
```

---

#### r/introvert
**Lead:** "I like connection. I hate surprise interactions. Here's what worked."

**Frame:** Saying yes to calls without losing your evening

**Avoid:** Stereotyping introverts as anti-social

**Example Post:**
```
Title: How to take calls without losing your whole evening to them

I want to stay close to people. I just can't handle surprise 2-hour phone calls when I only have 20 minutes of social energy left.

Made WhyHi so calls come with duration upfront: "15 min · Connection."

Now I can say yes because I know:
- It's not going to derail my evening
- I'm not trapped if it goes long (we agreed on 15 minutes)
- I can plan my energy around it

It's not about avoiding people—it's about knowing what I'm signing up for so I can actually show up.

Anyone else need this level of predictability?

(I'm the founder, built it for me first, sharing in case it resonates.)
```

---

#### r/AskWomenOver30
**Lead:** "Friendship maintenance is hard when everyone's busy. This helped."

**Frame:** Adult friendship upkeep, lightweight routine

**Avoid:** Mom guilt or "should" statements

**Example Post:**
```
Title: How I stopped letting friendships slip away

Between work, kids, life... I'd realize I hadn't talked to a close friend in 3 months. Not because I don't care—because calling felt like A THING.

Like I needed to set aside a whole evening. Or have a reason. Or wait for the perfect time.

I built WhyHi to make "just checking in" calls feel normal again: before calling, you set duration + intention. They see "10 min · Connection."

Now it's not a big commitment. It's 10 minutes between dinner and bedtime. Doable.

I've stayed closer to people this year than I have in the last five years combined.

Not saying it's magic—you still have to actually call. But it removed the friction that was stopping me.

Anyone else struggling with this? What's working for you?

(I made this because I needed it. Sharing in case others do too.)
```

---

#### r/LongDistance
**Lead:** "We kept trying to do regular calls. It never stuck. Then we tried this..."

**Frame:** Makes recurring connection easier, predictable routines

**Avoid:** Promising it solves relationship issues

**Example Post:**
```
Title: How we actually stuck to our daily call routine (after failing for months)

My partner and I tried doing daily calls. It lasted about a week before life got in the way.

The problem: one of us would call at a "bad time," the other felt guilty, we'd reschedule, then forget, then feel bad about forgetting...

Started using WhyHi: we both set "20 min · Connection" as our nightly routine. If one of us can't talk, they hit "call back in 1 hour" and we both get reminded.

It's been 6 weeks and we've only missed 3 calls (vs missing 5+ a week before).

The structure makes it feel like less pressure? Like we're both opting in, not one person imposing on the other.

Has anyone else struggled with this? What's worked for you?

(Made this app, but genuinely asking—what helps you stay connected?)
```

---

### ORGANIZATION PARTNERSHIP OUTREACH

**Target Organizations (Aligned Missions):**

**Neurodiversity & Accessibility:**
- Autistic Self Advocacy Network (ASAN)
- Autism Women & Nonbinary Network (AWN)
- CHADD (ADHD advocacy)
- ADDitude Magazine
- Neurodiversity Hub
- Different Brains

**Mental Health & Wellness:**
- ADAA (Anxiety & Depression Association)
- 7 Cups (peer support platform)
- The Mighty (storytelling platform)
- NAMI local chapters

**Loneliness & Connection Initiatives:**
- Campaign to End Loneliness (UK)
- Foundation for Social Connection (US)
- Together All (online support groups)
- Modern Elder Academy (connection for 50+)

**Parent & Family Communities:**
- Scary Mommy community
- Cup of Jo readers
- Motherly community
- Special needs parenting groups

**College/Young Adult Mental Health:**
- Active Minds chapters
- JED Foundation campus programs
- Student support services at universities

---

### Partnership Email Template

**Subject:** Partnership Opportunity: WhyHi + [Organization Name]

**Body:**
```
Hi [Name],

I'm Tom, founder of WhyHi—a calling app designed to make phone calls less anxiety-inducing and more accessible.

I'm reaching out because [Organization] and WhyHi share a mission: [specific alignment, e.g., "supporting the neurodivergent community" or "addressing the loneliness epidemic"].

What WhyHi Does:
WhyHi shows people *why* you're calling and *how long* you need before they answer. This simple change makes calls predictable, reduces overwhelm, and helps people stay connected.

Why This Matters for [Audience]:
[Specific pain point for their community, e.g., "Many autistic adults avoid calls because of the unpredictability. WhyHi removes that barrier by adding structure and boundaries to calling."]

Partnership Ideas:
- Beta access for your community
- Co-branded content (e.g., blog post or video about accessible communication)
- Feedback session to improve WhyHi for [specific needs]
- Webinar or workshop on intentional communication

Would you be open to a brief call to explore this? I'd love to learn how WhyHi could serve your community better.

Best,
Tom
Founder, WhyHi
[Email] | [WhyHi Website]
```

---

### LinkedIn Enterprise Outreach (WhyHi Pro)

**Target Roles:**
- Sales leaders, customer success directors
- Service business owners (plumbers, HVAC, real estate agents)
- Insurance agency owners
- Recruiting firm managers
- Healthcare practice managers

**LinkedIn DM Template:**
```
Hi [Name],

Saw your post about [pain point related to customer communication / pickup rates / relationship building].

Quick question: How often do your [sales reps / field techs / agents] leave voicemails that never get returned?

I built WhyHi Pro to solve this. It adds context to outbound calls—shows customers *why* you're calling and *how long* it'll take before they pick up.

Early customers are seeing 30-40% higher pickup rates.

Would it make sense to show you a quick demo?

Best,
Tom
```

---

## SECTION G: CONTENT CADENCE & SCHEDULING

**Purpose:** Define posting frequency, content mix, and pre-launch strategy.

---

### Posting Frequency

**Social Posts:** 3-4x per week (across LinkedIn, Facebook, Instagram)
**Social Videos:** 1-2x per week (30-90 seconds, short-form)
**Instructional Videos:** One-time creation (7 videos for onboarding drip campaign)

---

### Pre-Launch Strategy

**Goal:** Build content library of 30 posts + 15 videos BEFORE mid-March launch

**Why:** 
- Content calendar populated through April
- Posting runs on autopilot post-launch
- Tom's time post-launch focused on users, not content creation

**Timeline:** 4-6 weeks before launch (start early February)

---

### Content Mix Guidelines

**Social Posts (30 total):**
- **40% (12 posts):** Use Case Spotlights (relatable scenarios from Use Case Library)
- **30% (9 posts):** Hidden Cost / Moment of Clarity (problem awareness)
- **20% (6 posts):** Educational (how WhyHi works, features)
- **10% (3 posts):** Personal / Founder Story (authentic, vulnerable)

**Social Videos (15 total):**
- **50% (7-8 videos):** Use case reenactments (show problem + WhyHi solution)
- **30% (4-5 videos):** Talking head (observational insights, "moment of clarity" style)
- **20% (2-3 videos):** Educational (how to use WhyHi, screen recording demos)

---

### Platform Distribution

**LinkedIn:** 
- **Frequency:** 2x/week (Tuesday morning 9-10am, Thursday afternoon 2-3pm)
- **Content Focus:** 70% WhyHi Pro / B2B messaging, 30% personal use cases
- **Tone:** Professional but conversational

**Facebook:**
- **Frequency:** 1-2x/week (Weekday evenings 7-9pm)
- **Content Focus:** Parent scenarios, friendship maintenance, life logistics
- **Tone:** Warm, community-focused

**Instagram:**
- **Frequency:** 2x/week (mix of feed posts and Reels)
- **Content Focus:** Visual use case scenarios, emotional connection, spontaneous moments
- **Tone:** Personal, relatable, punchy

---

### Scheduling Strategy

**Use Buffer for Automated Posting:**
- All approved posts scheduled in advance
- Mix of platforms and themes to avoid repetition
- Stagger posting times based on platform best practices
- Tom reviews calendar weekly but doesn't manually post

**Content Calendar Structure:**
- Week 1: Introduce problem (loneliness paradox, texting vs calling)
- Week 2: Show use cases (everyday logistics, quick questions)
- Week 3: Deepen problem awareness (hidden cost, call anxiety)
- Week 4: Demonstrate solution (how WhyHi works)
- Week 5+: Rotate through use case clusters, maintain variety

---

### Engagement Strategy

**Responding to Comments:**
- Tom responds to meaningful comments/questions within 24 hours
- COS does NOT auto-respond (keep human touch)
- Use comments to identify potential creator partnerships

**Tracking Performance:**
- COS pulls engagement metrics automatically (via engagement_tracking workflow)
- Weekly review: which themes/formats are resonating?
- Adjust future content mix based on data

---

### Content Refresh Cycle

**Monthly Review:**
- Which posts got highest engagement?
- Which use case clusters resonate most?
- Are we seeing fatigue with certain themes?

**Quarterly Update:**
- Refresh Use Case Library with new scenarios
- Update messaging based on user feedback
- Add new video scripts for emerging use cases

---

**END OF COS CONTENT PLAYBOOK**

Document 3: Founder Voice Profile (Placeholder)
File Path: /canon/founder_voice_profile.md
Content:
markdown# Founder Voice Profile: Tom

**Purpose:** Help Content Drafter match Tom's natural voice, style, and energy when generating content.

**Status:** Partial - to be completed by Tom over time

---

## Tone & Style

**How I naturally speak:**
- Casual, engaging, warm, conversational
- Not formal, not corporate
- Fast-paced, energetic
- Direct and honest

**Humor:**
- High sense of humor
- Self-deprecating
- Intellectual humor (smart but accessible)

---

## On-Camera Persona

**Pace:** Fast talker

**Energy Level:** High energy, charismatic

**Gestures:** Yes, I use hand gestures frequently to emphasize points

**Props:** No props unless holding phone to reference app

**Style:** Direct to camera yet conversational and inviting

---

## Words/Phrases I Use Often

**[TO BE FILLED IN BY TOM]**

*Examples to add:*
- Common expressions
- Favorite analogies
- Go-to transitions
- Signature phrases

---

## Words/Phrases I'd NEVER Say

**[TO BE FILLED IN BY TOM]**

*Examples to add:*
- Business jargon you hate
- Phrases that feel inauthentic
- Overused tech buzzwords
- Anything that sounds "salesy"

---

## Content Preferences

### Topics I'm Passionate About:
**[TO BE FILLED IN BY TOM]**

*Guidance:* What gets you fired up? What could you talk about for hours?

### Topics I'd Rather Avoid:
- Politics (generally avoid unless directly relevant to product/mission)

**[TO BE FILLED IN BY TOM - Add more]**

### How Vulnerable/Personal I'm Willing to Get:
- 1-2 personal posts about my journey (friends slipping away, building WhyHi to solve my own problem)
- Most content should stay observational and universal, not personal
- Willing to share founder story when it adds credibility or connection
- Not interested in making myself the hero of every story

### Strong Opinions I Want to Express:
**[TO BE FILLED IN BY TOM]**

*Examples:*
- Messaging is killing real connection
- Phone calls aren't broken, the design is
- [Add more]

### Positions I Want to Stay Neutral On:
**[TO BE FILLED IN BY TOM]**

---

## Examples of My Style

### People Whose Style I Admire:
**[TO BE FILLED IN BY TOM]**

*Add:*
- Links to videos/creators whose tone you want to match
- "I want to sound like [person] when explaining [topic]"

### Content I Hate (What NOT to Sound Like):
**[TO BE FILLED IN BY TOM]**

*Add:*
- Examples of content that feels off-brand
- "Never make me sound like this..."

---

## Notes for Content Drafter Agent

When generating content in Tom's voice:
- Match his fast-talking, energetic pace
- Use conversational language, avoid corporate speak
- Self-deprecating humor when appropriate
- Direct and honest, no sugar-coating
- Casual but intelligent tone
- Hand gestures when on camera (note in storyboards)

**This profile will evolve.** Tom can tell WOS: "Add [phrase] to things I say often" or "Remove [topic] from content preferences" and this document will be updated.

---

**END OF FOUNDER VOICE PROFILE**

TECHNICAL SPECIFICATIONS
Audience: Claude Code
Purpose: Exact implementation requirements for databases, workflows, and agents.

NOTION DATABASE ARCHITECTURE
DATABASE 1: Content & Creator Capture (Unified)
Purpose: Single repository for all captured content (creator profiles, posts, articles). Supports both outreach pipeline AND content ideation.
Status: ✅ Exists (formerly "Creator CRM")
Database ID: 23d632f5307e8001a1d6fb31be92d59e
Action Required: ⚠️ Add new fields (amendments specified below)

EXISTING PROPERTIES (Keep As-Is):

Source URL (URL)

The original URL of the profile, post, or article


Platform (Select)

Options: Twitter/X, Instagram, YouTube, TikTok, LinkedIn, Facebook, Article/Blog, Other
Auto-detected from URL pattern


Creator/Author (Text)

Extracted handle (e.g., @username) or author name


Contact Method (Select)

Options: Twitter DM, Instagram DM, LinkedIn Message, YouTube Comment/Email, TikTok DM, Facebook Messenger, Email, Other
Auto-suggested based on platform


Outreach Status (Select)

Options: New Lead, Researched, Draft Ready, Outreach Sent, Responded, Not Interested, Archived


Date Captured (Created Time)

Auto-generated timestamp




NEW PROPERTIES (Add These):

Action Type (Multi-select) [NEW]

Options:

🎯 Outreach Target
💡 Content Ideation
📌 Reference Only


User can select multiple (e.g., both Outreach AND Ideation)
Default: Empty (user must triage after capture)
Purpose: Determines which downstream workflows trigger


Topic Tags (Multi-select) [NEW]

Options:

Loneliness
Call Anxiety
Telephobia
Connection
Texting vs Calling
Productivity
Neurodiversity
Parenting
Professional Relationships
Friendship
Mental Health
WhyHi Pro / B2B
Other


User manually selects relevant themes
Visible/Relevant when: Action Type includes "💡 Content Ideation"


Relevance Score (Select) [NEW]

Options: 1 (Low), 2, 3 (Medium), 4, 5 (High)
User rates how relevant/inspiring this content is for ideation
Visible/Relevant when: Action Type includes "💡 Content Ideation"


Content Notes (Text - Long) [NEW]

User's notes on what angle/idea caught their attention
What's interesting about this content?
What could we riff on?
Visible/Relevant when: Action Type includes "💡 Content Ideation"


Ideation Status (Select) [NEW]

Options: New, Reviewed, Sent to COS, Ideas Generated, Used, Archived
Default: New
Visible/Relevant when: Action Type includes "💡 Content Ideation"
TRIGGER: When set to "Sent to COS" → triggers ideation_trigger workflow




RELATIONS (Add These):

Generated Ideas (Relation to "Content Ideas Queue") [NEW]

Links to content ideas that were inspired by this captured item
Auto-populated when Content Idea Miner creates ideas
Allows tracking: "Which ideas came from this source?"


Related Drafts (Relation to "Drafts for Review") [NEW]

Links to drafts that reference this source content
Helps track content lineage




WORKFLOW INTEGRATION NOTES:
Triggers:

Outreach Trigger: Activated when Action Type contains "🎯 Outreach Target" AND Outreach Status = "Draft Ready"
Ideation Trigger: Activated when Action Type contains "💡 Content Ideation" AND Ideation Status = "Sent to COS"

Capture Workflow Changes:

content_capture workflow will create entries with all core fields populated
Action Type field left empty (user decides later)
Outreach Status defaults to empty or "New Lead" only if historically used for outreach


DATABASE 2: Content Ideas Queue
Purpose: Stores content ideas generated by Content Idea Miner agent, awaiting user approval.
Status: ⚠️ New database (needs creation)
Suggested Notion Database Name: Content Ideas Queue

PROPERTIES (All New):

Idea Title (Title - Text)

Short description of the content idea
Example: "Video: Locked out scenario (5 min Question call)"
Auto-populated by Content Idea Miner agent


Source Content (Relation to "Content & Creator Capture")

Links back to the captured item that inspired this idea
Allows tracing: "Where did this idea come from?"


Content Type (Select)

Options: Social Post, Video, Thread, Article, Email, Other
Specifies output format
Helps Content Drafter know what to generate


Platform Target (Multi-select)

Options: LinkedIn, Facebook, Instagram, All Platforms, YouTube, Twitter/X
Where should this content be posted?
Can select multiple if cross-platform post


**Use Case
Continue4:38 PMCluster** (Select)

Options:

Logistics & Quick Questions
Connection & Maintenance
Emotional Support
News & Updates
Planning & Coordination
Emergencies
General/Other


Which theme does this idea fit?
Helps organize content library


Idea Description (Text - Long)

Generated by Content Idea Miner
Explains the angle, hook, and why it's relevant
Example: "Post about locked-out scenario. Lead with frustration of texting vs needing immediate answer. Show WhyHi's 5-min Question call as natural solution. Use Case Spotlight formula."


Status (Select)

Options: Proposed, Approved, Rejected, Drafting, Done, Archived
Default: Proposed
TRIGGER: When set to "Approved" → triggers drafting_trigger workflow


Your Notes (Text)

User's feedback/edits on the idea
Example: "Like this but change to parent scenario instead of locked-out"
Content Drafter can reference these notes when generating


Date Generated (Created Time)

Auto-generated timestamp


Priority (Select)

Options: High, Medium, Low
User can prioritize which ideas to draft first
Helps manage queue when many ideas generated




RELATIONS:

Related Drafts (Relation to "Drafts for Review")

Links to drafts created from this idea
Allows tracking: "What drafts came from this idea?"
Auto-populated when Content Drafter creates draft




DATABASE 3: Drafts for Review
Purpose: Stores drafted content (posts, video scripts) generated by Content Drafter agent, awaiting user approval.
Status: ⚠️ New database (needs creation)
Suggested Notion Database Name: Drafts for Review

PROPERTIES (All New):

Draft Title (Title - Text)

Inherits from linked Content Idea
Example: "LinkedIn Post: Locked out scenario"


Linked Idea (Relation to "Content Ideas Queue")

Links to the approved idea this draft came from
Shows origin of content


Content Type (Select - Auto-populated from Idea)

Options: Social Post, Video Script, Thread, Article
Determines which draft fields are relevant


Platform (Multi-select - Auto-populated from Idea)

Options: LinkedIn, Facebook, Instagram, YouTube, Twitter/X, All
Where this will be posted




FOR SOCIAL POSTS (Conditional fields based on Content Type = "Social Post"):

LinkedIn Draft (Text - Long)

Platform-specific post copy (150-250 words)
Generated by Content Drafter following LinkedIn tone guidelines


Facebook Draft (Text - Long)

Platform-specific post copy (100-200 words)
Generated by Content Drafter following Facebook tone guidelines


Instagram Caption (Text - Long)

Platform-specific caption (80-150 words)
Generated by Content Drafter following Instagram tone guidelines


Suggested Images (Text)

Links or keywords for royalty-free images
Generated by Content Drafter
Example: "Unsplash search: 'phone call anxiety' OR direct link: https://unsplash.com/photos/..."




FOR VIDEO SCRIPTS (Conditional fields based on Content Type = "Video Script"):

Video Script (Text - Long)

Full script with timestamps/structure
Example: "[0-3s] Hook... [4-15s] Setup... [16-40s] WhyHi reveal..."
Generated by Content Drafter following video frameworks


Storyboard Notes (Text)

Shot suggestions, visual elements, text overlays
Generated by Content Drafter
Example: "Shot 1: Talking head. Shot 2: Show phone screen with '5 min Question'. Overlay text at 15s."


Video Format (Select)

Options: Talking Head, Scenario Reenactment, Screen Recording, Educational/Explainer
Helps user understand production needs




APPROVAL & SCHEDULING (For All Content Types):

Status (Select)

Options: Draft, Approved, Needs Revision, Scheduled, Posted, Archived
Default: Draft
TRIGGER: When set to "Approved" AND Content Type = "Social Post" → triggers buffer_scheduling workflow


Your Edits/Notes (Text)

User's feedback on the draft
Example: "Change opening hook to be more direct"
Used for iteration if status set to "Needs Revision"


Scheduled Date (Date with Time)

When this should be posted (if approved)
User sets this before approving
Used for Buffer scheduling


Buffer Link (URL)

Link to scheduled post in Buffer dashboard
Auto-populated after buffer_scheduling workflow runs


Date Created (Created Time)


RELATIONS:

Calendar Entries (Relation to "Content Calendar")

Links to Content Calendar entries created from this draft
Allows tracking where/when draft was posted




DATABASE 4: Content Calendar
Purpose: Master calendar of all scheduled and posted content. Syncs with Buffer for automated posting. Tracks engagement metrics.
Status: ⚠️ New database (needs creation)
Suggested Notion Database Name: Content Calendar

PROPERTIES (All New):

Post Title (Title - Text)

Inherits from approved draft
Example: "LinkedIn: Locked out scenario - Use Case Post"


Linked Draft (Relation to "Drafts for Review")

Links to the draft this calendar entry came from
Shows content origin


Content Type (Select - Auto-populated from draft)

Options: Social Post, Video, Thread
Rolled up from linked draft


Platform (Multi-select - Auto-populated from draft)

Options: LinkedIn, Facebook, Instagram, YouTube
Where this is being posted
Can be multiple if same content goes to multiple platforms


Post Copy (Text - Long)

Final approved text (platform-specific)
Copied from approved draft
This is what gets sent to Buffer


Image/Video URL (URL or File)

Link to visual asset
For posts: Unsplash/Pexels link or uploaded image
For videos: Link to uploaded video file (DropBox, Google Drive, etc.)


Scheduled Date/Time (Date with Time)

When Buffer should post this
Set by user or suggested by COS based on platform best practices
Example: "March 15, 2026 9:00 AM PST"


Status (Select)

Options: Scheduled, Posted, Failed, Cancelled
Default: Scheduled
Auto-updated by buffer_scheduling workflow after posting


Buffer Post ID (Text)

Unique ID from Buffer API
Used to pull engagement metrics
Auto-populated when post is scheduled


Buffer Queue Link (URL)

Direct link to view in Buffer dashboard
Auto-populated when post is scheduled




ENGAGEMENT METRICS (Auto-populated post-publish by engagement_tracking workflow):

Likes/Reactions (Number)

Pulled from Buffer API after posting
Updated daily for first week, then weekly


Comments (Number)

Pulled from Buffer API
Helps identify posts worth engaging with


Shares (Number)

Pulled from Buffer API
Indicator of viral potential


Reach/Impressions (Number)

Pulled from Buffer API (if available, platform-dependent)
Total people who saw the post


Date Posted (Date)

Actual post date (vs scheduled date)
Auto-populated when status changes to "Posted"


Performance Notes (Text)

User or agent notes on what worked/didn't work
Example: "High engagement—use case scenarios perform well on LinkedIn"
Can be manual or auto-generated summary




VIEWS (Suggested):
View 1: Calendar View

Group by: Week
Filter: Status = Scheduled or Posted
Sort: Scheduled Date/Time ascending

View 2: Platform Performance

Group by: Platform
Filter: Status = Posted
Sort: Likes/Reactions descending

View 3: This Week's Posts

Filter: Scheduled Date within next 7 days
Sort: Scheduled Date/Time ascending


N8N WORKFLOW SPECIFICATIONS
WORKFLOW 1: content_capture (Existing - Needs Amendment)
Purpose: Unified capture of creator profiles, posts, articles via iOS share sheet. Populates Notion database.
Status: ✅ Exists (creator_capture_v0)
Webhook URL: https://n8n.whyhi.app/webhook/wos/intent/creator_capture_v0
Action Required: ⚠️ Amend to support new Notion fields

CURRENT BEHAVIOR:

Webhook receives URL from iOS shortcut
JavaScript extracts:

Platform (Twitter, Instagram, YouTube, etc.)
Creator handle/name
Contact method (platform-specific)


Creates Notion entry in Creator CRM
Sets Outreach Status to "New Lead"
Returns confirmation message


REQUIRED CHANGES:
1. Update JavaScript Extraction Node:

Keep existing logic for platform, handle, contact method
No changes needed here

2. Modify Notion API "Create Entry" Node:
Add new fields to Notion creation:
json{
  "Source URL": "[extracted URL]",
  "Platform": "[extracted platform]",
  "Creator/Author": "[extracted handle]",
  "Contact Method": "[suggested method]",
  "Action Type": [], // Empty multi-select - user will triage
  "Outreach Status": "", // Empty - no longer auto-set to "New Lead"
  "Topic Tags": [], // Empty multi-select
  "Relevance Score": null, // Empty
  "Content Notes": "", // Empty text field
  "Ideation Status": "New" // Default to "New" but hidden unless Action Type includes "Content Ideation"
}
```

**3. Update Response Message:**

Change confirmation from:
```
"✅ Captured! Added to outreach pipeline."
```

To:
```
"✅ Captured! Review in Notion to triage (Outreach, Ideation, or Both)."
```

**4. Keep Existing Smart Notes Logic:**
- If URL is video/post (not profile): Add note "Open post → tap username → share profile URL"
- If URL is article/blog: Extract domain, note to manually find author

---

#### UPDATED WORKFLOW STRUCTURE:
```
[Webhook Trigger]
    ↓
[JavaScript: Extract URL Data]
    - Platform detection
    - Creator/Handle extraction
    - Contact Method suggestion
    ↓
[Notion API: Create Entry]
    - Populate core fields (URL, platform, creator, contact method)
    - Leave Action Type empty (user triages)
    - Leave ideation fields empty
    - Set Ideation Status to "New" (conditional visibility)
    ↓
[HTTP Response]
    - Confirmation: "✅ Captured! Review in Notion to triage."

TESTING CHECKLIST:

 Share profile URL via iOS → Verify entry created with empty Action Type
 Share post URL via iOS → Verify smart notes added
 Share article URL via iOS → Verify domain extracted
 Verify all new fields present in Notion entry
 Verify no errors in n8n execution log


WORKFLOW 2: ideation_trigger (New - Needs Creation)
Purpose: Monitors Notion for items marked "Sent to COS" and triggers Content Idea Miner agent.
Status: ⚠️ New workflow (to be built)
Suggested Workflow Name: cos_ideation_trigger

TRIGGER:
Method: Notion database poll
Frequency: Every 5 minutes
Database: Content & Creator Capture (23d632f5307e8001a1d6fb31be92d59e)
Filter Conditions:

Action Type contains "💡 Content Ideation"
AND Ideation Status = "Sent to COS"


WORKFLOW STEPS:
1. Query Notion (Trigger)

Get all entries matching filter
For each entry, extract:

Source URL
Platform
Creator/Author
Topic Tags
Relevance Score
Content Notes (user's observations)



2. Retrieve Context

Read Brand Foundation from Canon (/canon/brand_foundation.md)
Read Content Playbook from Canon (/canon/cos_content_playbook.md)
Read Use Case Library (within Content Playbook)

3. Call Content Idea Miner Agent (via MCP)
Input to Agent:
json{
  "source_url": "[captured URL]",
  "platform": "[platform]",
  "creator": "[creator name]",
  "topic_tags": ["Loneliness", "Call Anxiety"],
  "relevance_score": 4,
  "user_notes": "[Tom's notes on what caught his attention]",
  "brand_foundation": "[full Brand Foundation content]",
  "content_playbook": "[full Content Playbook content]",
  "use_case_library": "[extracted use case clusters]"
}
Expected Output from Agent:
json{
  "ideas": [
    {
      "title": "LinkedIn Post: Professional Phone Tag Problem",
      "content_type": "Social Post",
      "platform_target": ["LinkedIn"],
      "use_case_cluster": "Logistics & Quick Questions",
      "description": "Use Hidden Cost formula. Lead with stat about time wasted in phone tag. Contrast with 5-minute call efficiency. WhyHi Pro angle for B2B audience."
    },
    {
      "title": "Instagram Video: Why We Don't Call Anymore",
      "content_type": "Video",
      "platform_target": ["Instagram"],
      "use_case_cluster": "Connection & Maintenance",
      "description": "Talking head, Moment of Clarity formula. Ask 'When's the last time you called a friend?' Reveal design problem. Show WhyHi as simple fix."
    }
    // Agent generates 2-5 ideas total
  ]
}
4. Create Entries in Content Ideas Queue
For each generated idea:
json{
  "Idea Title": "[idea.title]",
  "Source Content": "[relation to original captured item]",
  "Content Type": "[idea.content_type]",
  "Platform Target": ["[idea.platform_target]"],
  "Use Case Cluster": "[idea.use_case_cluster]",
  "Idea Description": "[idea.description]",
  "Status": "Proposed",
  "Date Generated": "[current timestamp]"
}
```

**5. Update Source Entry in Notion**

Update original captured item:
- `Ideation Status`: "New" → "Ideas Generated"
- `Generated Ideas`: [add relations to newly created idea entries]

**6. Optional: Notify User**

Send notification (email, Slack, or skip for now):
- "✅ 3 content ideas generated from [source]. Review in Notion to approve."

---

#### ERROR HANDLING:

- If Content Idea Miner agent fails: Log error, set Ideation Status to "Error - Retry"
- If Notion API fails: Retry 3 times with exponential backoff
- If 0 ideas generated: Update status to "No Ideas Generated" with note

---

#### WORKFLOW STRUCTURE DIAGRAM:
```
[Notion Trigger: Poll Every 5 Min]
    Filter: Action Type contains "Ideation" AND Ideation Status = "Sent to COS"
    ↓
[For Each Matching Entry]
    ↓
    [Extract Entry Data]
        - URL, platform, creator, tags, score, notes
    ↓
    [Read Canon Documents]
        - Brand Foundation
        - Content Playbook
        - Use Case Library
    ↓
    [Call Content Idea Miner Agent via MCP]
        Input: Source data + Canon context
        Output: Array of 2-5 content ideas
    ↓
    [For Each Generated Idea]
        ↓
        [Create Entry in Content Ideas Queue]
            - Idea Title, Type, Platform, Description
            - Link to source content
            - Status: "Proposed"
    ↓
    [Update Source Entry]
        - Ideation Status: "Ideas Generated"
        - Generated Ideas: [link relations]
    ↓
    [Optional: Send Notification]

TESTING CHECKLIST:

 Mark test entry as "Sent to COS" → Verify workflow triggers within 5 min
 Verify Content Idea Miner agent called with correct context
 Verify 2-5 ideas created in Content Ideas Queue
 Verify source entry updated with "Ideas Generated" status
 Verify relations correctly linked
 Test error handling: invalid URL, agent timeout, Notion API failure


WORKFLOW 3: drafting_trigger (New - Needs Creation)
Purpose: Monitors Content Ideas Queue for approved ideas and triggers Content Drafter agent.
Status: ⚠️ New workflow (to be built)
Suggested Workflow Name: cos_drafting_trigger

TRIGGER:
Method: Notion database poll
Frequency: Every 5 minutes
Database: Content Ideas Queue
Filter Conditions:

Status = "Approved"


WORKFLOW STEPS:
1. Query Notion (Trigger)

Get all approved ideas
For each idea, extract:

Idea Title
Idea Description
Content Type (Social Post vs Video Script)
Platform Target
Use Case Cluster
Source Content (relation - fetch source URL if needed)



2. Retrieve Context

Read Brand Foundation from Canon
Read Content Playbook from Canon
Read Founder Voice Profile from Canon
Fetch source content (if linked) from Content & Creator Capture

3. Call Content Drafter Agent (via MCP)
Input to Agent:
json{
  "idea_title": "[Idea Title]",
  "idea_description": "[Full description from Content Idea Miner]",
  "content_type": "Social Post" or "Video Script",
  "platform_target": ["LinkedIn", "Facebook", "Instagram"],
  "use_case_cluster": "[cluster name]",
  "source_content": {
    "url": "[if available]",
    "platform": "[if available]",
    "notes": "[user notes if available]"
  },
  "brand_foundation": "[full content]",
  "content_playbook": "[full content with formulas + examples]",
  "founder_voice_profile": "[full content]"
}
Expected Output from Agent (Social Post):
json{
  "linkedin_draft": "[150-250 word post following LinkedIn guidelines]",
  "facebook_draft": "[100-200 word post following Facebook guidelines]",
  "instagram_caption": "[80-150 word caption following Instagram guidelines]",
  "suggested_images": [
    "Unsplash search: 'phone call anxiety'",
    "https://unsplash.com/photos/abc123"
  ]
}
Expected Output from Agent (Video Script):
json{
  "video_script": "[Full script with timestamps, following video framework]",
  "storyboard_notes": "[Shot descriptions, text overlays, visual elements]",
  "video_format": "Talking Head" or "Scenario Reenactment" or "Educational"
}
4. Create Entry in Drafts for Review
For Social Post:
json{
  "Draft Title": "[Idea Title]",
  "Linked Idea": "[relation to approved idea]",
  "Content Type": "Social Post",
  "Platform": ["LinkedIn", "Facebook", "Instagram"],
  "LinkedIn Draft": "[agent output]",
  "Facebook Draft": "[agent output]",
  "Instagram Caption": "[agent output]",
  "Suggested Images": "[agent output]",
  "Status": "Draft",
  "Date Created": "[timestamp]"
}
For Video Script:
json{
  "Draft Title": "[Idea Title]",
  "Linked Idea": "[relation to approved idea]",
  "Content Type": "Video Script",
  "Platform": ["[target platform]"],
  "Video Script": "[agent output]",
  "Storyboard Notes": "[agent output]",
  "Video Format": "[agent output]",
  "Status": "Draft",
  "Date Created": "[timestamp]"
}
```

**5. Update Content Ideas Queue**

Update original idea:
- `Status`: "Approved" → "Done"
- Add relation to created draft (via "Related Drafts" field)

**6. Optional: Notify User**

Send notification:
- "✅ Draft ready for review: [Draft Title]. Check Notion to approve."

---

#### ERROR HANDLING:

- If Content Drafter agent fails: Log error, set idea status to "Error - Retry"
- If agent output is incomplete: Flag draft as "Needs Revision" with error note
- If Notion API fails: Retry 3 times

---

#### WORKFLOW STRUCTURE DIAGRAM:
```
[Notion Trigger: Poll Content Ideas Queue]
    Filter: Status = "Approved"
    ↓
[For Each Approved Idea]
    ↓
    [Extract Idea Data]
        - Title, description, type, platform, cluster
    ↓
    [Retrieve Canon Context]
        - Brand Foundation
        - Content Playbook
        - Founder Voice Profile
        - Source content (if linked)
    ↓
    [Call Content Drafter Agent via MCP]
        Input: Idea + Canon context
        Output: Platform-specific drafts OR video script + storyboard
    ↓
    [Create Entry in Drafts for Review]
        IF Social Post:
            - Populate LinkedIn/FB/IG drafts
            - Add suggested images
        IF Video:
            - Populate script + storyboard
            - Add format specification
        Status: "Draft"
    ↓
    [Update Content Ideas Queue]
        - Status: "Done"
        - Link to created draft
    ↓
    [Optional: Notify User]
```

---

#### TESTING CHECKLIST:

- [ ] Approve test idea → Verify workflow triggers within 5 min
- [ ] Verify Content Drafter called with correct context
- [ ] Verify draft created with platform-specific content
- [ ] For Social Post: Verify LN/FB/IG variants present
- [ ] For Video: Verify script + storyboard present
- [ ] Verify idea status updated to "Done"
- [ ] Verify relations correctly linked

---

### WORKFLOW 4: buffer_scheduling (New - Needs Creation)

**Purpose:** Monitors Drafts for Review for approved posts, schedules them in Buffer, and updates Content Calendar.

**Status:** ⚠️ New workflow (to be built)  
**Suggested Workflow Name:** `cos_buffer_scheduling`

---

#### PREREQUISITES:

**Buffer Setup (Tom's Action):**
1. Create Buffer account (free tier supports 3 channels)
2. Connect LinkedIn, Facebook, Instagram accounts
3. Generate API access token from Buffer settings
4. Provide token to CC for n8n integration

---

#### TRIGGER:

**Method:** Notion database poll  
**Frequency:** Every 5 minutes  
**Database:** Drafts for Review

**Filter Conditions:**
- `Status` = "Approved"
- AND `Content Type` = "Social Post"

---

#### WORKFLOW STEPS:

**1. Query Notion (Trigger)**
- Get approved post drafts
- Extract for each:
  - Draft Title
  - Platform (LinkedIn, Facebook, Instagram)
  - LinkedIn Draft text
  - Facebook Draft text
  - Instagram Caption text
  - Suggested Images (URLs)
  - Scheduled Date/Time

**2. For Each Platform in Platform List:**

**LinkedIn Posting:**
```
IF Platform includes "LinkedIn":
  [Buffer API: Create Scheduled Post]
    - Profile ID: [LinkedIn profile from Buffer]
    - Text: [LinkedIn Draft text]
    - Media: [Image URL if provided]
    - Scheduled time: [Scheduled Date/Time]
  
  [Receive Buffer Response]
    - Buffer Post ID
    - Buffer Queue Link
```

**Facebook Posting:**
```
IF Platform includes "Facebook":
  [Buffer API: Create Scheduled Post]
    - Profile ID: [Facebook profile from Buffer]
    - Text: [Facebook Draft text]
    - Media: [Image URL if provided]
    - Scheduled time: [Scheduled Date/Time]
  
  [Receive Buffer Response]
    - Buffer Post ID
    - Buffer Queue Link
```

**Instagram Posting:**
```
IF Platform includes "Instagram":
  [Buffer API: Create Scheduled Post]
    - Profile ID: [Instagram profile from Buffer]
    - Text: [Instagram Caption text]
    - Media: [Image URL - REQUIRED for Instagram]
    - Scheduled time: [Scheduled Date/Time]
  
  [Receive Buffer Response]
    - Buffer Post ID
    - Buffer Queue Link
3. Create Entry in Content Calendar (For Each Platform)
For each platform posted to:
json{
  "Post Title": "[Draft Title] - [Platform]",
  "Linked Draft": "[relation to draft]",
  "Content Type": "Social Post",
  "Platform": ["[specific platform]"],
  "Post Copy": "[platform-specific draft text]",
  "Image/Video URL": "[image URL if used]",
  "Scheduled Date/Time": "[scheduled datetime]",
  "Status": "Scheduled",
  "Buffer Post ID": "[from Buffer API response]",
  "Buffer Queue Link": "[from Buffer API response]",
  "Date Created": "[timestamp]"
}
4. Update Drafts for Review
Update original draft:

Status: "Approved" → "Scheduled"
Buffer Link: [URL to Buffer queue]
Add relation to created calendar entries


ERROR HANDLING:

If Buffer API fails: Log error, set draft status to "Scheduling Error"
If image URL invalid for Instagram: Flag error, require user to fix
If scheduled time in the past: Reject with error message
Retry Buffer API calls 3 times with exponential backoff


BUFFER API NOTES:
Endpoint: https://api.bufferapp.com/1/updates/create.json
Required Parameters:

access_token: [from Tom's Buffer account]
profile_ids[]: [platform-specific profile ID]
text: [post copy]
scheduled_at: [Unix timestamp]
media[photo]: [image URL - optional for LN/FB, required for IG]

Response:
json{
  "success": true,
  "buffer_count": 1,
  "buffer_percentage": 10,
  "updates": [
    {
      "id": "abc123def456",
      "status": "buffer",
      "text": "[post copy]",
      "due_at": 1234567890,
      "profile_id": "xyz789",
      "profile_service": "linkedin"
    }
  ]
}
```

---

#### WORKFLOW STRUCTURE DIAGRAM:
```
[Notion Trigger: Poll Drafts for Review]
    Filter: Status = "Approved" AND Content Type = "Social Post"
    ↓
[For Each Approved Draft]
    ↓
    [Extract Draft Data]
        - Platform-specific text (LN/FB/IG)
        - Images, scheduled datetime
    ↓
    [For Each Platform in Draft]
        ↓
        [Buffer API: Create Scheduled Post]
            - Profile ID (platform-specific)
            - Text (platform-specific draft)
            - Media (image URL)
            - Scheduled time
        ↓
        [Receive Buffer Response]
            - Post ID, Queue link
        ↓
        [Create Entry in Content Calendar]
            - Post title, platform, copy
            - Scheduled datetime
            - Buffer ID, Buffer link
            - Status: "Scheduled"
    ↓
    [Update Draft Status]
        - Status: "Scheduled"
        - Buffer Link: [URL]
        - Link to calendar entries

TESTING CHECKLIST:

 Approve test draft with scheduled datetime → Verify Buffer post created
 Check Buffer dashboard to confirm post in queue
 Verify Content Calendar entry created
 Verify multiple platforms (LN + FB + IG) all scheduled correctly
 Test with image URL → Verify image attached in Buffer
 Test error handling: invalid datetime, missing image for IG, API failure


WORKFLOW 5: engagement_tracking (New - Needs Creation)
Purpose: Pulls engagement metrics from Buffer after posts go live and updates Content Calendar.
Status: ⚠️ New workflow (to be built)
Suggested Workflow Name: cos_engagement_tracking

TRIGGER:
Method: Scheduled cron job
Frequency: Daily at 9:00 AM PST
OR: Manual trigger (for testing or immediate updates)

WORKFLOW STEPS:
1. Query Notion Content Calendar
Filter:

Status = "Posted"
AND Date Posted is within last 7 days

Extract for each:

Post Title
Platform
Buffer Post ID
Date Posted

2. For Each Post:
Call Buffer API to Get Analytics:
Endpoint: https://api.bufferapp.com/1/updates/[buffer_post_id].json
Parameters:

access_token: [Buffer token]

Response:
json{
  "id": "abc123",
  "statistics": {
    "reach": 1234,
    "clicks": 56,
    "shares": 12,
    "comments": 8,
    "likes": 89
  },
  "sent_at": 1234567890
}
Note: Available metrics vary by platform:

LinkedIn: likes, comments, shares, impressions
Facebook: likes, comments, shares, reach
Instagram: likes, comments (shares not always available)

3. Update Notion Content Calendar Entry:
json{
  "Likes/Reactions": [from API statistics.likes],
  "Comments": [from API statistics.comments],
  "Shares": [from API statistics.shares],
  "Reach/Impressions": [from API statistics.reach or impressions],
  "Performance Notes": "[optional auto-generated note]"
}
```

**Optional Auto-Generated Performance Notes:**
```
IF Likes > 50:
  "High engagement - strong post"
IF Comments > 10:
  "Active discussion - consider engaging in comments"
IF Shares > 5:
  "Viral potential - similar content performs well"
```

**4. Weekly Digest (Optional - Future Enhancement):**

After all posts updated:
- Aggregate metrics by platform, use case cluster, content type
- Identify top 3 performing posts
- Generate summary report
- Send to Tom via email or create Notion page

---

#### ERROR HANDLING:

- If Buffer API fails: Log error, retry next day
- If Buffer Post ID missing: Skip entry, flag for manual review
- If metrics not yet available (post too recent): Skip, will retry tomorrow

---

#### WORKFLOW STRUCTURE DIAGRAM:
```
[Cron Trigger: Daily at 9 AM]
    ↓
[Query Notion Content Calendar]
    Filter: Status = "Posted" AND Date Posted within last 7 days
    ↓
[For Each Posted Entry]
    ↓
    [Buffer API: Get Analytics]
        Endpoint: /updates/[buffer_post_id].json
        Extract: likes, comments, shares, reach
    ↓
    [Update Notion Content Calendar]
        - Likes/Reactions: [number]
        - Comments: [number]
        - Shares: [number]
        - Reach/Impressions: [number]
        - Performance Notes: [optional]
    ↓
[Optional: Generate Weekly Digest]
    - Aggregate metrics
    - Top performers
    - Insights for future content

TESTING CHECKLIST:

 Run workflow manually after test post published
 Verify metrics pulled from Buffer API
 Verify Notion updated with correct numbers
 Test with posts from different platforms (LN, FB, IG)
 Test error handling: missing Buffer ID, API failure
 Verify cron schedule triggers at correct time


WORKFLOW 6: outreach_trigger (New - Optional Phase 5)
Purpose: Monitors Notion for items marked "Ready for Outreach" and triggers Creator Outreach agent.
Status: ⚠️ New workflow (to be built in Phase 5 if time permits)
Priority: Lower than ideation/drafting workflows
Suggested Workflow Name: cos_outreach_trigger

TRIGGER:
Method: Notion database poll
Frequency: Every 15 minutes (less frequent than ideation)
Database: Content & Creator Capture
Filter Conditions:

Action Type contains "🎯 Outreach Target"
AND Outreach Status = "Draft Ready"


WORKFLOW STEPS:
1. Query Notion (Trigger)

Get entries marked for outreach
Extract:

Creator/Author
Platform
Source URL
Contact Method
Any notes/context Tom added



2. Call Creator Outreach Agent (Existing - May Need Update)
Input to Agent:
json{
  "creator_name": "[extracted]",
  "creator_handle": "[extracted]",
  "platform": "[platform]",
  "source_url": "[URL of their content]",
  "contact_method": "Twitter DM" or "Email" etc,
  "user_notes": "[any context Tom provided]",
  "whyhi_context": {
    "product": "[brief WhyHi description]",
    "why_reaching_out": "[alignment with creator's content]"
  }
}
Expected Output:
json{
  "outreach_message": "[Personalized message draft]",
  "subject_line": "[If email]",
  "platform_specific_notes": "[Tone adjustments for platform]"
}
3. Store Draft in Notion
Create "Outreach Messages" entry (new database or field in Content & Creator Capture):
json{
  "Creator": "[name]",
  "Platform": "[platform]",
  "Draft Message": "[agent output]",
  "Status": "Awaiting Approval",
  "Date Generated": "[timestamp]"
}
4. Update Content & Creator Capture
Update original entry:

Outreach Status: "Draft Ready" → "Awaiting Approval"

5. Tom Reviews & Approves
(Manual step - Tom reviews message in Notion)
6. After Approval:
IF Status = "Approved to Send":

Send message via platform API (Twitter DM, email, LinkedIn)
Update status to "Outreach Sent"
Log date sent


NOTE:
This workflow is lower priority than content creation workflows. Build only if time permits in Phase 5.
Tom can also handle outreach manually using the drafted messages—automation is nice-to-have, not required.

AGENT SPECIFICATIONS
AGENT 1: Content Idea Miner (New - Needs Creation)
Purpose: Analyzes captured content and generates 2-5 content ideas for WhyHi.
Status: ⚠️ New agent (to be built)
Access Method: MCP (callable via n8n workflow)
Suggested Agent Name: cos_content_idea_miner

INPUT SCHEMA:
json{
  "source_url": "string (URL of captured content)",
  "platform": "string (Twitter, Instagram, Article, etc.)",
  "creator": "string (author or creator name)",
  "topic_tags": ["array of strings (user-selected themes)"],
  "relevance_score": "number 1-5",
  "user_notes": "string (Tom's observations about this content)",
  "brand_foundation": "string (full Brand Foundation markdown)",
  "content_playbook": "string (full Content Playbook markdown)",
  "use_case_library": "string (extracted use cases from playbook)"
}

PROCESSING LOGIC:
Step 1: Analyze Source Content

Identify key themes, angles, insights in the captured content
Note how it relates to WhyHi's mission (loneliness, call anxiety, connection, etc.)
Extract quotable moments or statistics (if applicable)

Step 2: Cross-Reference with Canon

Check Brand Foundation for:

Approved messaging themes
Voice guidelines
Anti-patterns to avoid


Check Content Playbook for:

Which writing formulas apply?
Which use case clusters are relevant?
Platform-specific tone adaptations



Step 3: Cross-Reference with Use Case Library

Which specific scenarios (locked out, mom calling kid, etc.) could this inspire?
Are there multiple use cases this content could illustrate?

Step 4: Generate 2-5 Content Ideas
For each idea, determine:

Title: Short, descriptive (e.g., "LinkedIn Post: Phone Tag Problem")
Content Type: Social Post or Video
Platform Target: LinkedIn, Facebook, Instagram, or combination
Use Case Cluster: Which theme this fits
Description: Full explanation of:

Which writing formula to use (Use Case Spotlight, Hidden Cost, etc.)
Hook/opening line
Key points to cover
WhyHi angle (how to reveal solution)
Platform-specific notes



Step 5: Quality Checks

Does this align with Brand Foundation voice?
Does it avoid anti-patterns?
Is it specific enough for Content Drafter to execute?
Does it feel authentic to Tom's style?


OUTPUT SCHEMA:
json{
  "ideas": [
    {
      "title": "string (descriptive title)",
      "content_type": "Social Post" or "Video",
      "platform_target": ["LinkedIn"] or ["Facebook", "Instagram"] etc,
      "use_case_cluster": "string (cluster name from playbook)",
      "description": "string (detailed instructions for Content Drafter)"
    }
    // 2-5 ideas total
  ]
}

EXAMPLE INPUT/OUTPUT:
Input:
json{
  "source_url": "https://twitter.com/creator/status/123",
  "platform": "Twitter",
  "creator": "@sherry_turkle",
  "topic_tags": ["Loneliness", "Texting vs Calling"],
  "relevance_score": 5,
  "user_notes": "Great point about texting reducing empathy. Could tie to WhyHi's mission.",
  "brand_foundation": "[full content]",
  "content_playbook": "[full content]",
  "use_case_library": "[use cases]"
}
Output:
json{
  "ideas": [
    {
      "title": "LinkedIn Post: The Empathy Gap in Digital Communication",
      "content_type": "Social Post",
      "platform_target": ["LinkedIn"],
      "use_case_cluster": "General",
      "description": "Use The Hidden Cost formula. Lead with Turkle's observation about texting reducing empathy (paraphrase, don't quote directly). Contrast with how hearing someone's voice creates understanding. Tie to professional relationships: 'How many misunderstandings could be avoided with a 5-minute call?' WhyHi reveal: context makes calling feel possible again. Soft CTA."
    },
    {
      "title": "Instagram Video: Why Texting Doesn't Make Us Feel Close",
      "content_type": "Video",
      "platform_target": ["Instagram"],
      "use_case_cluster": "Connection & Maintenance",
      "description": "Talking head format, Moment of Clarity formula. Open with question: 'Why do we text our best friend 50 times a day but never call?' Reference Turkle's insight (reworded). Reveal: texting is transactional, voice is social. WhyHi makes calling easy: '10 min Connection' removes the barrier. Keep under 60 seconds."
    },
    {
      "title": "Facebook Post: Missing Your Friend's Voice",
      "content_type": "Social Post",
      "platform_target": ["Facebook"],
      "use_case_cluster": "Connection & Maintenance",
      "description": "Emotional angle. Lead with relatable scenario: 'When's the last time you heard your best friend laugh?' Build on Turkle's empathy point—we miss the nuance of voice. Use case: 10-minute catch-up that actually happens vs 100 texts that don't connect. WhyHi as enabler, not pushy pitch."
    }
  ]
}
```

---

#### PROMPT GUIDANCE FOR AGENT:
```
You are the Content Idea Miner for WhyHi's Content Operating System.

Your job: Analyze captured content (articles, social posts, videos) and generate 2-5 specific, actionable content ideas that align with WhyHi's brand voice and mission.

INPUTS YOU RECEIVE:
- Source content (URL, platform, creator, user notes)
- Brand Foundation (positioning, voice, themes)
- Content Playbook (writing formulas, use cases, examples)

YOUR PROCESS:
1. Identify key themes/insights in the source content
2. Connect to WhyHi's mission (loneliness, call anxiety, connection)
3. Reference Brand Foundation for approved messaging
4. Reference Content Playbook for formulas and use case clusters
5. Generate 2-5 ideas with detailed descriptions

EACH IDEA MUST INCLUDE:
- Title (descriptive, platform-specific)
- Content Type (Social Post or Video)
- Platform Target (LinkedIn, Facebook, Instagram, or mix)
- Use Case Cluster (from playbook)
- Description (which formula to use, hook, key points, WhyHi angle)

QUALITY STANDARDS:
- Align with Tom's voice (casual, fast-paced, self-deprecating humor)
- Avoid anti-patterns (no clinical claims, no competitor names, no hard sell)
- Be specific enough for Content Drafter to execute
- Vary platforms and formats (don't generate 5 LinkedIn posts)

OUTPUT FORMAT:
JSON array of ideas, each with title, content_type, platform_target, use_case_cluster, description.

Remember: You're helping Tom create authentic, engaging content that drives WhyHi's mission forward. Be creative, be strategic, be specific.

AGENT 2: Content Drafter (New - Needs Creation)
Purpose: Takes approved content ideas and generates platform-specific drafts (posts, video scripts, storyboards).
Status: ⚠️ New agent (to be built)
Access Method: MCP (callable via n8n workflow)
Suggested Agent Name: cos_content_drafter

INPUT SCHEMA:
json{
  "idea_title": "string (from approved idea)",
  "idea_description": "string (detailed instructions from Content Idea Miner)",
  "content_type": "Social Post" or "Video Script",
  "platform_target": ["LinkedIn"] or ["Facebook", "Instagram"] etc,
  "use_case_cluster": "string (cluster name)",
  "source_content": {
    "url": "string (optional)",
    "platform": "string (optional)",
    "notes": "string (optional)"
  },
  "brand_foundation": "string (full markdown)",
  "content_playbook": "string (full markdown with formulas + examples)",
  "founder_voice_profile": "string (full markdown)"
}

PROCESSING LOGIC:
FOR SOCIAL POSTS:
Step 1: Identify Formula

Parse idea_description to determine which writing formula to use
Example: "Use Hidden Cost formula" → reference that section in Content Playbook

Step 2: Reference Examples

Look at "Voice in Action" example posts in Content Playbook
Match tone, structure, pacing to examples

Step 3: Apply Founder Voice

Reference Founder Voice Profile for:

Tone (casual, fast-paced)
Humor style (self-deprecating, intellectual)
Words/phrases to use or avoid
Energy level (high, charismatic)



Step 4: Generate Platform-Specific Drafts
LinkedIn (150-250 words):

Professional angle (if applicable, WhyHi Pro)
Conversational but polished
Lead with business pain point or observation
Soft CTA

Facebook (100-200 words):

Personal, relatable angle
Parent or friendship scenario
Warm, community tone
Invite engagement (tag a friend, share if relate)

Instagram (80-150 words):

Short, punchy
Visual storytelling
Emotional or aspirational
Question to audience

Step 5: Suggest Images

Query Unsplash/Pexels API with relevant keywords
OR provide search keywords for Tom to use
Ensure images align with post theme


FOR VIDEO SCRIPTS:
Step 1: Identify Framework

Talking Head, Scenario Reenactment, or Educational/Explainer
Based on idea_description instructions

Step 2: Write Script with Timestamps

Follow framework structure from Content Playbook
Include:

[0-3s] Hook
[4-15s] Setup
[16-40s] WhyHi reveal
[41-60s] Closer


Use natural language (how Tom would actually speak)
Fast-paced, energetic delivery

Step 3: Storyboard Notes

Shot suggestions (talking head, B-roll, screen recording)
Visual elements (text overlays, graphics)
Props or actions (hold up phone, show app interface)
Transitions or cuts

Step 4: Specify Format

Talking Head, Scenario Reenactment, Screen Recording, or Educational


OUTPUT SCHEMA:
For Social Post:
json{
  "linkedin_draft": "string (150-250 words)",
  "facebook_draft": "string (100-200 words)",
  "instagram_caption": "string (80-150 words)",
  "suggested_images": [
    "Unsplash search: 'keyword'",
    "Direct URL: https://unsplash.com/photos/abc"
  ]
}
For Video Script:
json{
  "video_script": "string (full script with timestamps)",
  "storyboard_notes": "string (shot descriptions, visual elements)",
  "video_format": "Talking Head" or "Scenario Reenactment" or "Educational"
}

EXAMPLE INPUT/OUTPUT:
Input (Social Post):
json{
  "idea_title": "LinkedIn Post: Phone Tag Problem",
  "idea_description": "Use Hidden Cost formula. Lead with time wasted in phone tag. Contrast with 5-minute call efficiency. WhyHi Pro angle for B2B audience.",
  "content_type": "Social Post",
  "platform_target": ["LinkedIn", "Facebook"],
  "use_case_cluster": "Logistics & Quick Questions",
  "brand_foundation": "[full content]",
  "content_playbook": "[full content]",
  "founder_voice_profile": "[full content]"
}
Output:
json{
  "linkedin_draft": "Your field tech needs to update a customer about a delayed appointment.\n\nThey call. Customer doesn't pick up (unknown number, might be spam). Tech leaves voicemail. Customer calls back two hours later when tech is at another job site. Voicemail again. Phone tag begins.\n\nHow much time just got wasted? How much frustration for both sides?\n\nNow imagine: the customer sees 'ABC Plumbing: 5 min · Appointment Update' before their phone even rings. They know exactly what it is. They pick up. Issue resolved in 2 minutes.\n\nThat's how WhyHi Pro turns missed calls into completed conversations.\n\nCalling works—when people actually pick up.",
  
  "facebook_draft": "Ever play phone tag for three days just to schedule one appointment?\n\n'When are you free?'\n'Tuesday?'\n'Morning or afternoon?'\n'10am?'\n'Can we do 11?'\n\nEight texts later, you still haven't confirmed the time. A 5-minute call would've handled it instantly.\n\nThis is why WhyHi shows people WHY you're calling and HOW LONG you need before they answer. Suddenly, picking up feels reasonable.\n\nThere's a better way to coordinate.",
  
  "instagram_caption": "Phone tag: the worst game ever invented.\n\nYou call. They miss it. They call back. You miss it. Repeat for 3 days.\n\nOr... you send a '5 min · Question' call and they know exactly what you need.\n\nPick up rate: 📈\nFrustration: 📉\n\nTag someone who never picks up the phone 😅",
  
  "suggested_images": [
    "Unsplash search: 'phone call business'",
    "https://unsplash.com/photos/person-holding-phone"
  ]
}
```

---

#### PROMPT GUIDANCE FOR AGENT:
```
You are the Content Drafter for WhyHi's Content Operating System.

Your job: Take approved content ideas and transform them into platform-specific drafts (posts or video scripts) that match Tom's voice and WhyHi's brand.

INPUTS YOU RECEIVE:
- Approved content idea (title, description, platform, cluster)
- Brand Foundation (positioning, voice, anti-patterns)
- Content Playbook (formulas, examples, video frameworks)
- Founder Voice Profile (Tom's tone, style, energy)

YOUR PROCESS FOR SOCIAL POSTS:
1. Identify which writing formula to use (from idea description)
2. Reference example posts in Content Playbook (match that style)
3. Apply Tom's voice (casual, fast-paced, self-deprecating humor)
4. Generate platform-specific variants:
   - LinkedIn: 150-250 words, professional angle
   - Facebook: 100-200 words, relatable/personal
   - Instagram: 80-150 words, short/punchy
5. Suggest images (Unsplash keywords or direct URLs)

YOUR PROCESS FOR VIDEO SCRIPTS:
1. Identify which framework to use (Talking Head, Reenactment, Educational)
2. Write script with timestamps following framework structure
3. Use natural, conversational language (how Tom actually talks)
4. Create storyboard notes (shots, visuals, text overlays)
5. Specify video format

QUALITY STANDARDS:
- Match Tom's voice (reference Founder Voice Profile)
- Follow formulas precisely (they're proven to work)
- Avoid anti-patterns (no clinical claims, no hard sell, no competitor names)
- Platform-appropriate tone and length
- Soft CTAs only (invite, don't demand)

CRITICAL RULES:
- NEVER reproduce copyrighted quotes (paraphrase/reference instead)
- Maximum ONE short quote (<15 words) from source content if needed
- All content must be original, not regurgitated from sources
- If idea references a creator's work, discuss the concept, don't copy their words

OUTPUT FORMAT:
For Social Post: JSON with linkedin_draft, facebook_draft, instagram_caption, suggested_images
For Video: JSON with video_script, storyboard_notes, video_format

Remember: You're writing AS Tom, not FOR Tom. It should sound like he wrote it himself.

AGENT 3: Creator Outreach (Existing - May Need Update)
Purpose: Generates personalized outreach messages to creators/journalists.
Status: ✅ Already built (part of WOS)
Action Required: ⚠️ May need updates to integrate with unified Notion database

CURRENT BEHAVIOR (Assumed):

Takes creator info (name, handle, platform, source content)
Analyzes creator's content/profile
Drafts personalized outreach message
Platform-appropriate tone


INTEGRATION WITH COS:
Input from outreach_trigger workflow:
json{
  "creator_name": "string",
  "creator_handle": "string",
  "platform": "string",
  "source_url": "string (the post/profile captured)",
  "contact_method": "Twitter DM" or "Email" etc,
  "user_notes": "string (Tom's context)",
  "whyhi_context": {
    "product_description": "brief WhyHi overview",
    "why_reaching_out": "alignment reason"
  }
}
Expected Output:
json{
  "outreach_message": "string (personalized message draft)",
  "subject_line": "string (if email)",
  "platform_notes": "string (tone adjustments for platform)"
}

UPDATE REQUIREMENTS (If Needed):

Align with Brand Foundation

Reference Brand Foundation for WhyHi positioning
Use approved language (not clinical, not sales-y)


Platform-Specific Tone

Twitter DM: Casual, short, direct
LinkedIn Message: Professional but warm
Email: More formal, include subject line


Personalization Based on Source

Reference the specific post/content that was captured
Connect to WhyHi mission authentically
Avoid generic templates




TESTING AFTER INTEGRATION:

 Pass creator info from unified Notion database
 Verify outreach message references Brand Foundation
 Test with different platforms (Twitter, LinkedIn, Email)
 Verify personalization quality (not generic)


BUILD ORDER & TIMELINE
Total Duration: 2 weeks (10 working days)
Approach: Phased implementation with testing at each stage

PHASE 1: Foundation (Week 1, Days 1-2)
Goal: Set up Canon documents and Notion databases

Day 1: Canon Setup
Tasks:

Extract and save Brand Foundation

Read content from this brief
Create file: /canon/brand_foundation.md
Commit to git with message: "Add Brand Foundation to Canon"


Extract and save Content Playbook

Read content from this brief
Create file: /canon/cos_content_playbook.md
Commit to git with message: "Add COS Content Playbook to Canon"


Create Founder Voice Profile placeholder

Create file: /canon/founder_voice_profile.md
Add placeholder structure (provided in this brief)
Note for Tom to complete over time
Commit to git



Deliverables:

 /canon/brand_foundation.md created and committed
 /canon/cos_content_playbook.md created and committed
 /canon/founder_voice_profile.md placeholder created


Day 2: Notion Database Updates
Tasks:

Update Content & Creator Capture database

Add new properties (Action Type, Topic Tags, Relevance Score, Content Notes, Ideation Status, Generated Ideas relation, Related Drafts relation)
Test with sample entry
Document database ID and field IDs


Create Content Ideas Queue database

Create new database with all specified properties
Create relations to Content & Creator Capture and Drafts for Review
Set up suggested views (Proposed, Approved, Done)
Test with sample entry


Create Drafts for Review database

Create new database with all specified properties
Create relations to Content Ideas Queue and Content Calendar
Set up views (by status, by platform)
Test with sample entry


Create Content Calendar database

Create new database with all specified properties
Create relation to Drafts for Review
Set up suggested views (Calendar view, Platform performance, This week)
Test with sample entry


Documentation

Create COS_SETUP.md file documenting:

All database IDs
Field names and types
Relation structures
Webhook URLs


Commit to repo



Deliverables:

 Content & Creator Capture updated with new fields
 Content Ideas Queue database created
 Drafts for Review database created
 Content Calendar database created
 All relations properly configured
 Sample entries tested in each database
 COS_SETUP.md documentation created

Ask Tom Before Day 2:

Do you want me to create a backup of existing Content & Creator Capture before modifications?
Confirm database modifications look correct before proceeding


Day 2 (Continued): Amend content_capture Workflow
Tasks:

Update content_capture workflow

Modify Notion API node to include new fields
Update response message
Keep existing URL extraction logic
Test with iOS share (Tom will test)


Test workflow

Share test URL via iOS shortcut
Verify Notion entry created with new fields
Verify Action Type left empty (user triages)
Verify no errors in n8n execution log



Deliverables:

 content_capture workflow updated
 Test successful (entry created with new fields)
 No breaking changes to existing functionality


PHASE 2: Ideation Flow (Week 1, Days 3-4)
Goal: Enable content ideation pipeline (capture → ideas)

Day 3: Build Content Idea Miner Agent
Tasks:

Create Content Idea Miner agent

Implement MCP-accessible agent
Integrate with Canon (read Brand Foundation, Content Playbook)
Implement processing logic (analyze content, generate 2-5 ideas)
Test with sample captured content


Test agent in isolation

Pass sample input (article URL, user notes)
Verify 2-5 ideas generated
Check idea quality (specific, actionable, matches brand voice)
Verify ideas reference appropriate formulas and use cases



Deliverables:

 Content Idea Miner agent created and accessible via MCP
 Agent tested with sample inputs
 Quality checks passed (ideas are specific and on-brand)


Day 4: Build ideation_trigger Workflow
Tasks:

Create ideation_trigger workflow

Set up Notion poll trigger (every 5 min)
Filter: Action Type contains "Ideation" AND Ideation Status = "Sent to COS"
For each entry: extract data, read Canon, call Content Idea Miner agent
Create entries in Content Ideas Queue
Update source entry with "Ideas Generated" status


Test workflow end-to-end

Mark test entry as "Sent to COS"
Wait for workflow to trigger (within 5 min)
Verify ideas created in Content Ideas Queue
Verify source entry updated
Verify relations linked correctly



Deliverables:

 ideation_trigger workflow created
 End-to-end test successful (capture → ideas)
 Error handling implemented
 Documentation updated in COS_SETUP.md

Milestone: Tom can now capture content, send to COS, and receive AI-generated content ideas

PHASE 3: Drafting Flow (Week 1-2, Days 5-7)
Goal: Enable content drafting pipeline (approved ideas → drafts)

Day 5: Build Content Drafter Agent
Tasks:

Create Content Drafter agent

Implement MCP-accessible agent
Integrate with Canon (Brand Foundation, Content Playbook, Founder Voice Profile)
Implement post generation (LinkedIn/Facebook/Instagram variants)
Implement video script generation (with storyboards)


Test agent in isolation

Pass sample approved idea (social post)
Verify platform-specific drafts generated
Check voice match (does it sound like Tom?)
Verify formula adherence
Test video script generation
Check storyboard quality



Deliverables:

 Content Drafter agent created and accessible via MCP
 Social post drafts tested (LN/FB/IG)
 Video script drafts tested
 Quality checks passed (voice match, formula adherence)


Day 6-7: Build drafting_trigger Workflow
Tasks:

Create drafting_trigger workflow

Set up Notion poll trigger (Content Ideas Queue, every 5 min)
Filter: Status = "Approved"
For each approved idea: extract data, read Canon, call Content Drafter agent
Create entry in Drafts for Review (with platform-specific content)
Update idea status to "Done"


Test workflow end-to-end

Approve test idea in Notion
Wait for workflow to trigger
Verify draft created in Drafts for Review
Verify all platform variants present (or video script if applicable)
Verify idea updated to "Done"
Verify relations linked


Refinement

Tom reviews draft quality
Iterate on Content Drafter prompts if needed
Adjust formulas or voice guidance based on feedback



Deliverables:

 drafting_trigger workflow created
 End-to-end test successful (idea → draft)
 Draft quality approved by Tom
 Documentation updated

Milestone: Tom can now approve ideas and receive platform-specific drafts automatically

PHASE 4: Scheduling (Week 2, Days 8-9)
Goal: Enable automated posting via Buffer

Day 8: Set Up Buffer Integration
Tom's Tasks (Before Day 8):

 Create Buffer account (free tier)
 Connect LinkedIn, Facebook, Instagram accounts
 Generate API access token
 Provide token to CC

CC Tasks:

Configure Buffer integration in n8n

Add Buffer credentials to n8n
Test Buffer API connection
Verify profiles (LinkedIn, Facebook, Instagram) accessible


Test Buffer API manually

Create test scheduled post via API
Verify it appears in Buffer queue
Verify post publishes at scheduled time (or cancel before publish)



Deliverables:

 Buffer credentials configured in n8n
 API connection tested successfully
 Platform profiles verified


Day 8 (Continued): Build buffer_scheduling Workflow
Tasks:

Create buffer_scheduling workflow

Set up Notion poll trigger (Drafts for Review, every 5 min)
Filter: Status = "Approved" AND Content Type = "Social Post"
For each approved draft:

For each platform: call Buffer API to schedule post
Create entry in Content Calendar
Update draft status to "Scheduled"




Test workflow end-to-end

Approve test draft with scheduled datetime
Wait for workflow to trigger
Verify post scheduled in Buffer (check Buffer dashboard)
Verify Content Calendar entry created
Verify draft updated to "Scheduled"



Deliverables:

 buffer_scheduling workflow created
 End-to-end test successful (draft → Buffer → calendar)
 Buffer dashboard shows scheduled post
 Documentation updated


Day 9: Build engagement_tracking Workflow
Tasks:

Create engagement_tracking workflow

Set up cron trigger (daily at 9:00 AM PST)
Query Content Calendar for posted items (last 7 days)
For each post: call Buffer API to get analytics
Update Content Calendar with metrics (likes, comments, shares, reach)


Test workflow

Run manually (don't wait for cron)
If test post available: verify metrics pulled
If no test post: create mock data to verify Notion updates work


Optional: Weekly Digest

If time permits, add aggregation logic
Generate summary of top performers
Send to Tom via email or create Notion page



Deliverables:

 engagement_tracking workflow created
 Cron schedule configured
 Test run successful
 Metrics update in Notion verified
 Documentation updated

Milestone: Tom can now schedule posts to Buffer automatically and track engagement metrics

PHASE 5: Outreach Flow (Week 2, Day 10, Optional)
Goal: Enable creator outreach pipeline (if time permits)
Priority: Lower than content creation workflows

Day 10: Build outreach_trigger Workflow (If Time Permits)
Tasks:

Review existing Creator Outreach agent

Verify it works with unified Notion database
Update if needed to reference Brand Foundation


Create outreach_trigger workflow

Set up Notion poll trigger (every 15 min)
Filter: Action Type contains "Outreach" AND Outreach Status = "Draft Ready"
Call Creator Outreach agent
Store draft message in Notion
Update status to "Awaiting Approval"


Test workflow

Mark test entry as "Draft Ready"
Verify workflow triggers
Verify message drafted
Tom reviews message quality



Deliverables:

 outreach_trigger workflow created (if time permits)
 Message quality approved by Tom
 Documentation updated

Alternative: If Phase 5 not completed, Tom can handle outreach manually. Add to BACKLOG.md as future enhancement.

PHASE 6: Testing & Refinement (Ongoing)
Goal: Validate system works end-to-end, iterate based on feedback

Testing Checklist
End-to-End Ideation Flow:

 Capture content via iOS → Triage as "Ideation" → Send to COS → Ideas generated → Approve idea → Draft created → Approve draft → Scheduled in Buffer → Posted → Metrics tracked

End-to-End Outreach Flow (If Built):

 Capture content via iOS → Triage as "Outreach" → Mark as "Draft Ready" → Message drafted → Approve → Send → Status updated

Dual-Purpose Capture:

 Mark entry as BOTH "Outreach" AND "Ideation" → Verify both workflows trigger correctly

Error Scenarios:

 Invalid URL → Verify workflow handles gracefully
 Agent timeout → Verify retry logic works
 Notion API failure → Verify error logging
 Buffer API failure → Verify draft marked as "Scheduling Error"


Iteration & Tuning
Week 2+:

Tom uses system for real content creation
Provides feedback on:

Idea quality (are they useful?)
Draft quality (does it sound like Tom?)
Workflow efficiency (any bottlenecks?)



CC adjusts:

Content Idea Miner prompts (if ideas too generic)
Content Drafter prompts (if voice doesn't match)
Workflow polling frequency (if too noisy or too slow)


POST-BUILD: Phase Completion Checklist
After completing Phases 1-5, Claude Code should:

Create COS_STATUS.md file

Document what's built, what's tested, what's working
Note any issues or limitations
List items deferred to BACKLOG.md


Update WOS_SETUP.md

Add all COS-related configuration details
Webhook URLs, database IDs, API tokens
Workflow names and purposes


Provide Tom with handoff document

How to use the COS
How to capture content
How to triage, approve ideas, approve drafts
How to schedule posts
How to review metrics


Recommend items for BACKLOG.md

Email/Slack notifications
Auto-suggested posting times
Advanced analytics dashboard
A/B testing framework
(See "Items for BACKLOG.md" section below)




PRE-LAUNCH CONTENT SPRINT PLAN
Goal: Build library of 30 posts + 15 videos before mid-March launch
Timeline: 4-6 weeks before launch (start early February)
Deliverable: Fully populated content calendar through April, posting runs on autopilot

Week 1: Capture (Ideally 40-50 pieces)
Target: Capture 40-50 pieces of source content

Sources to Capture:
Articles:

Loneliness epidemic (scholarly articles, news pieces)
Phone call anxiety / telephobia
Digital communication trends
Neurodiversity and communication
Professional relationship building

Social Media:

Posts from thought leaders (Sherry Turkle, Scott Galloway, Simon Sinek, Jonathan Haidt, Freya India, Sam Harris, Jay Shetty)
Threads from Reddit (r/Telephobia, r/autism, r/ADHD, r/socialanxiety)
LinkedIn posts about professional communication
Instagram posts about friendship maintenance

Existing Resources:

Tom's list of 50-100 creator posts (telephobia, online loneliness)
Podcast episodes or clips (Dayal McCluskey, Yakov Danishefsky, Dr. Jerome Adams)


Process:
Daily (Mon-Fri):

Browse source platforms (Twitter, LinkedIn, Instagram, Reddit, articles)
Capture 8-10 pieces per day via iOS share → content_capture
End of day: Quick triage in Notion

Mark all as "💡 Content Ideation"
Add relevance scores (4-5 for best content)
Add brief notes on what caught your attention



Weekend:

Review week's captures
Set all high-quality items to "Sent to COS"


Week 2: Ideation (Generate 40-50 ideas, approve 40-50)
Target: Generate 80-150 ideas (2-3 per source), approve top 40-50

Process:
Monday:

Batch send all captured content to COS (set Ideation Status = "Sent to COS")
Wait for Content Idea Miner to generate ideas (should complete within hours)

Tuesday-Friday:

Review generated ideas in Content Ideas Queue (sorted by "Proposed")
Approve top ideas targeting:

30 ideas for social posts (mix of LinkedIn, Facebook, Instagram)
15 ideas for social videos (use case scenarios, talking heads)
5 bonus (buffer for testing or rejections)



Prioritize:

Mix of use case clusters (avoid 20 "Logistics" posts in a row)
Mix of platforms (don't approve 25 LinkedIn posts, 5 Facebook)
Mix of formats (Use Case Spotlight, Hidden Cost, Moment of Clarity, etc.)


Approval Strategy:
Social Posts (30):

12 Use Case Spotlights (various scenarios)
9 Hidden Cost / Moment of Clarity (problem awareness)
6 Educational (how WhyHi works)
3 Personal / Founder Story

Platform Distribution:

12 LinkedIn (focus on WhyHi Pro, professional relationships)
10 Facebook (parenting, friendship, logistics)
8 Instagram (emotional connection, use case visuals)

Social Videos (15):

7-8 Use case reenactments (locked out, phone tag, busy parent)
4-5 Talking head (Moment of Clarity, Hidden Cost themes)
2-3 Educational (how to use WhyHi, screen recording)


Week 3: Drafting (Get drafts for all 40-50 approved ideas)
Target: 30 approved post drafts + 15 approved video scripts

Process:
Monday:

Approve ideas in batches of 10
Content Drafter generates drafts (should complete within hours)

Tuesday-Friday:

Review drafts in "Drafts for Review" (sorted by "Draft" status)
For each draft:

Read platform-specific versions (LinkedIn, Facebook, Instagram)
Edit if needed (adjust tone, change hook, tweak CTA)
Approve if good (or mark "Needs Revision" with notes)


Select/approve images from Unsplash/Pexels suggestions

Weekend:

Review all approved drafts
Ensure variety in themes and formats
Identify any gaps (need more Facebook posts? More videos on specific topic?)


Quality Check:
For Posts:

Does it sound like Tom? (voice match)
Does it follow the formula correctly?
Is the platform adaptation appropriate?
Does it avoid anti-patterns (no hard sell, no clinical language)?

For Videos:

Is the script natural (would Tom actually say this)?
Is the storyboard clear and actionable?
Is the format appropriate (Talking Head vs Reenactment)?
Is it under 60 seconds for social platforms?


Week 4-5: Production (Record and edit 15 videos)
Target: 15 finished videos, ready to upload

Process:
Week 4 (Recording):
Monday-Wednesday:

Set up recording space (clean background, good lighting, phone on tripod)
Review all 15 video scripts
Group scripts by format:

Talking Head (can batch record in one session)
Scenario Reenactment (may need props or location changes)
Educational/Screen Recording (need to record screen + voiceover)



Batch Recording Sessions:

Session 1 (Talking Head): Record all 7-8 talking head videos in one sitting

Use teleprompter or memorize key points from script
Do 2-3 takes per video
Keep energy high, match Tom's fast-paced style


Session 2 (Reenactment): Record scenario-based videos

Follow storyboard notes
May need to record B-roll (texting footage, frustrated expressions, etc.)


Session 3 (Educational): Screen recordings + voiceover

Record app screen while demonstrating features
Record voiceover separately (cleaner audio)



Thursday-Friday:

Review all raw footage
Select best takes
Organize files for editing


Week 5 (Editing):
Monday-Friday:

Edit videos in CapCut (basic cuts, text overlays, transitions)
For Talking Head:

Cut out pauses, filler words ("um," "uh")
Add text overlays at key moments (e.g., "5 min · Question" graphic)
Add WhyHi logo end screen


For Reenactment:

Cut between scenes (texting → frustrated → WhyHi solution)
Add text bubbles or graphics to show messaging vs calling
Add music (if appropriate, keep subtle)


For Educational:

Sync screen recording with voiceover
Add arrows or highlights to UI elements
Add captions for key steps



Weekend:

Review all 15 edited videos
Export finals (1080p, MP4)
Upload to cloud storage (Google Drive, Dropbox)
Note video URLs in Notion (for easy access during scheduling)


Video Editing Checklist (Per Video):

 Intro hook under 3 seconds
 Captions/text overlays at key moments
 WhyHi logo or branding visible (end screen)
 Length under 60 seconds (for Instagram/TikTok) or 90 seconds max (for LinkedIn/YouTube)
 Audio clear (no background noise, consistent volume)
 Exported and uploaded to cloud
 Video URL added to Notion draft


Week 6: Scheduling (Schedule all 30 posts + 15 videos)
Target: Fully populated content calendar through April

Process:
Monday:

Review content calendar strategy
Decide posting frequency:

3-4 posts per week (across all platforms)
1-2 videos per week


Calculate: 30 posts + 15 videos = ~10 weeks of content (March-April coverage)

Tuesday-Thursday:

Schedule all 30 social posts in Buffer

LinkedIn: Tuesday 9am, Thursday 2pm
Facebook: Wednesday 7pm, Friday 6pm
Instagram: Monday 8pm, Thursday 8pm


Ensure mix of themes and formats (don't post 3 "phone tag" posts in a row)
Stagger use case clusters across weeks

Thursday-Friday:

Schedule all 15 videos in Buffer

LinkedIn: Wednesday mornings (professional audience awake and active)
Instagram: Weekend evenings (higher engagement for video content)


Alternate video formats (Talking Head → Reenactment → Educational)

Weekend:

Review entire content calendar (March 15 - April 30)
Verify balanced distribution:

Each platform has regular cadence
Use case clusters rotate
Video + post mix feels natural


Make final adjustments to scheduling


Scheduling Best Practices:
Time Slots:

LinkedIn: Weekday mornings (9-10am) or early afternoons (2-3pm)
Facebook: Weekday evenings (6-9pm)
Instagram: Evenings (7-9pm) or weekends

Frequency:

Avoid posting to same platform twice in one day
Space posts at least 48 hours apart on same platform
Ensure content variety (don't post 3 "busy parent" scenarios in one week)

Buffer Queue Review:

Double-check all posts have images (especially Instagram - required)
Verify scheduled times are correct (timezone set to PST)
Confirm all platforms selected correctly


Sprint Completion Checklist
By End of Week 6 (Early March):

 40-50 pieces of source content captured
 40-50 content ideas generated and approved
 30 social post drafts approved (LinkedIn, Facebook, Instagram)
 15 video scripts approved
 15 videos recorded, edited, and uploaded
 All 30 posts scheduled in Buffer (March 15 - April 30)
 All 15 videos scheduled in Buffer
 Content calendar reviewed and balanced
 Ready for launch! 🚀


Metrics to Track During Sprint:
Time Invested:

Capture: ~5-7 hours/week (browsing + capturing + triaging)
Ideation review: ~3-5 hours (reviewing and approving ideas)
Drafting review: ~5-7 hours (reviewing and editing drafts)
Video recording: ~6-8 hours (3 batch recording sessions)
Video editing: ~15-20 hours (basic editing in CapCut, ~1 hour per video)
Scheduling: ~3-5 hours (setting up calendar, reviewing balance)

Total Time Estimate: 40-55 hours over 6 weeks (~7-9 hours/week)
Efficiency Gains from COS:

Without COS: ~100+ hours (ideation, writing, rewriting, researching)
With COS: ~40-55 hours (reviewing, editing, recording, scheduling)
Time Saved: ~50-60 hours (COS does the heavy lifting)


IMMEDIATE POST-BUILD TASKS
These are tasks Tom must complete manually, NOT part of the CC build.

Tom's Manual Tasks (Before/During Build)
Before Phase 1:

 Review this Implementation Brief thoroughly
 Prepare any feedback or changes for CC before build starts
 Ensure WOS repository access for CC

Before Phase 4:

 Create Buffer account (free tier)
 Connect LinkedIn, Facebook, Instagram to Buffer
 Generate Buffer API access token
 Provide token to CC for integration

Before Phase 6 (Content Sprint):

 Complete more details in Founder Voice Profile (words/phrases, content preferences)
 Compile list of source content to capture (articles, posts, creators)
 Block time in calendar for video recording sessions
 Set up video recording space (lighting, background, tripod)

Ongoing (Post-Build):

 Test iOS shortcut for content_capture workflow
 Capture first batch of content (articles, posts, videos)
 Triage captured content (Outreach, Ideation, or Both)
 Review and approve generated ideas
 Review and edit generated drafts
 Record and edit videos using approved scripts
 Schedule posts in Buffer (or approve automated scheduling)
 Respond to comments/engagement on posted content


Optional Manual Tasks (Lower Priority)

 Execute subreddit posts using Community Engagement guidelines
 Send partnership emails to aligned organizations
 Conduct LinkedIn outreach for WhyHi Pro (using provided templates)
 Refine Brand Foundation and Content Playbook based on performance data


ITEMS FOR BACKLOG.md
These are future enhancements to add to BACKLOG.md AFTER Phase 5 is complete.
To add items to BACKLOG.md, use:
bashpython3 add_to_backlog.py "COS Enhancement: [specific item]"
This will:

Add item to BACKLOG.md
Create matching Notion task in tasks-masterlist with Context: "Backlog"


COS Future Enhancements
Priority: Post-Launch
Effort: Varies per item
Added: [Date of COS completion]

Notifications & Alerts

 Email notifications when ideas are generated

Trigger: Content Idea Miner completes
Send: Email to Tom with count of new ideas + link to Notion


 Slack notifications when drafts are ready for approval

Trigger: Content Drafter completes
Send: Slack message with draft title + link to review


 Weekly digest of engagement metrics

Trigger: Every Monday at 9am
Send: Email with top 5 performing posts, insights, recommendations


 Alert when scheduled posts fail to publish

Trigger: Buffer API returns error or Status = "Failed"
Send: Immediate email or Slack alert



Command:
bashpython3 add_to_backlog.py "COS Enhancement: Email/Slack notifications for content approval workflows"

Advanced Analytics

 Auto-suggested posting times based on engagement patterns

Analyze: Historical performance by time-of-day and day-of-week
Suggest: Optimal posting times for each platform
Integration: Auto-fill suggested time when scheduling in Buffer


 Advanced analytics dashboard

Aggregate: Performance across platforms, use case clusters, content types
Visualize: Charts showing engagement trends over time
Insights: "Posts about X perform 2x better on LinkedIn than Facebook"
Export: Weekly/monthly reports


 A/B testing framework for messaging

Test: Two versions of same post (different hooks, different CTAs)
Track: Which version performs better
Learn: Apply insights to future content



Command:
bashpython3 add_to_backlog.py "COS Enhancement: Auto-suggested posting times based on historical engagement patterns"
python3 add_to_backlog.py "COS Enhancement: Advanced analytics dashboard for content performance"
python3 add_to_backlog.py "COS Enhancement: A/B testing framework for messaging optimization"

Content Creation Enhancements

 Automated image selection from Unsplash/Pexels

Currently: Content Drafter suggests images, Tom selects manually
Enhancement: Auto-select top image based on relevance, download, attach to draft
Approval gate: Tom can override if needed


 Video editing workflow integration

Currently: Tom edits manually in CapCut
Enhancement: If CapCut API becomes available, automate basic editing (cuts, text overlays, end screen)
Requires: CapCut API access (not currently available)


 Multi-language content support

Currently: English only
Enhancement: If WhyHi expands internationally, generate content in multiple languages
Requires: Translation API + cultural adaptation in Brand Foundation



Command:
bashpython3 add_to_backlog.py "COS Enhancement: Automated image selection (vs manual approval)"
python3 add_to_backlog.py "COS Enhancement: Video editing workflow integration (if CapCut API available)"

Community Engagement

 Community engagement tracking

Track: Responses to Reddit posts, forum posts
Aggregate: Which communities are most responsive?
Insights: Where to focus community engagement efforts


 Automated Reddit post drafting

Currently: Tom writes Reddit posts manually using Community Engagement guidelines
Enhancement: Generate Reddit-specific post drafts for each subreddit
Approval gate: Tom reviews before posting


 Sentiment analysis on comments

Analyze: Comments on posts (positive, negative, neutral)
Alert: If negative sentiment spike, flag for Tom's attention
Insights: What content generates most positive reactions?



Command:
bashpython3 add_to_backlog.py "COS Enhancement: Community engagement tracking (Reddit/forum responses)"
python3 add_to_backlog.py "COS Enhancement: Automated Reddit post drafting with approval gate"

Workflow Optimizations

 Batch approval workflows

Currently: Tom approves ideas one-by-one
Enhancement: Multi-select approve in Notion (approve 10 ideas at once)
Trigger: Batch-trigger Content Drafter for efficiency


 Smart idea prioritization

Currently: Tom manually sets priority (High/Medium/Low)
Enhancement: AI suggests priority based on:

Relevance score
Platform performance history
Content calendar gaps


Tom can override


 Auto-archive old content

Currently: Content Calendar grows indefinitely
Enhancement: Auto-archive posts older than 90 days
Keep metrics, remove from active views



Command:
bashpython3 add_to_backlog.py "COS Enhancement: Batch approval workflows for efficiency"
python3 add_to_backlog.py "COS Enhancement: Smart idea prioritization based on performance history"

Integration Expansions

 TikTok integration

Currently: LinkedIn, Facebook, Instagram only
Enhancement: Add TikTok to Buffer workflow
Requires: TikTok profile setup, Buffer TikTok integration


 Twitter/X integration

Currently: Not scheduling to Twitter/X
Enhancement: Add Twitter/X to posting platforms
Requires: Twitter API access, Buffer integration


 YouTube Shorts integration

Currently: Videos posted to Instagram/LinkedIn only
Enhancement: Auto-post short videos to YouTube Shorts
Requires: YouTube API, video format adaptation



Command:
bashpython3 add_to_backlog.py "COS Enhancement: TikTok integration for video content"
python3 add_to_backlog.py "COS Enhancement: YouTube Shorts integration"

TESTING & VALIDATION
Purpose: Comprehensive testing checklist to ensure COS works end-to-end

Database Tests
Content & Creator Capture

 Create test entry manually in Notion
 Verify all new fields present (Action Type, Topic Tags, etc.)
 Set Action Type to "Ideation" → Verify Ideation Status field becomes visible
 Set Action Type to "Outreach" → Verify Outreach Status field relevant
 Test multi-select: Set Action Type to BOTH "Ideation" AND "Outreach"

Content Ideas Queue

 Create test idea manually
 Link to source content (relation) → Verify link works both directions
 Set Status to "Approved" → Verify ready for drafting_trigger

Drafts for Review

 Create test draft manually (Social Post type)
 Verify platform-specific fields (LinkedIn/Facebook/Instagram drafts)
 Create test draft (Video Script type)
 Verify video-specific fields (script, storyboard, format)

Content Calendar

 Create test calendar entry manually
 Link to draft → Verify relation works
 Test Calendar view (group by week)
 Test Platform Performance view (group by platform, sort by engagement)


Workflow Tests
content_capture

 Share test URL via iOS shortcut
 Verify Notion entry created within 30 seconds
 Verify Source URL, Platform, Creator fields populated correctly
 Verify Action Type left empty (awaiting triage)
 Verify response message updated: "Review in Notion to triage"
 Test with different URL types:

 Twitter profile
 Instagram post
 Article/blog
 YouTube video



ideation_trigger

 Mark test entry as "Sent to COS"
 Wait 5 minutes (or trigger workflow manually)
 Verify Content Idea Miner called successfully
 Verify 2-5 ideas created in Content Ideas Queue
 Verify ideas have descriptions, platforms, clusters
 Verify source entry updated to "Ideas Generated"
 Verify relations linked (source → ideas)
 Test error handling:

 Invalid source URL → Verify error logged
 Agent timeout → Verify retry logic



drafting_trigger

 Approve test idea in Content Ideas Queue
 Wait 5 minutes (or trigger manually)
 Verify Content Drafter called successfully
 Verify draft created in Drafts for Review
 For Social Post: Verify LinkedIn/Facebook/Instagram variants present
 For Video: Verify script + storyboard + format present
 Verify idea updated to "Done"
 Verify relations linked (idea → draft)
 Test error handling:

 Agent timeout → Verify error logged
 Incomplete output → Verify flagged as "Needs Revision"



buffer_scheduling

 Approve test draft with scheduled datetime (future date)
 Wait 5 minutes (or trigger manually)
 Verify Buffer API called successfully
 Check Buffer dashboard → Verify post in queue
 Verify Content Calendar entry created
 Verify draft updated to "Scheduled"
 Verify Buffer Post ID and Queue Link populated
 Test with multiple platforms:

 LinkedIn only
 Facebook + Instagram
 All three platforms


 Test error handling:

 Invalid image URL for Instagram → Verify error flagged
 Scheduled time in the past → Verify rejected
 Buffer API failure → Verify retry logic



engagement_tracking

 Wait 24 hours after test post published (or use mock data)
 Trigger workflow manually (don't wait for cron)
 Verify Buffer API called to get analytics
 Verify Content Calendar updated with metrics (likes, comments, shares, reach)
 Test with posts from different platforms (metrics vary by platform)
 Verify cron schedule triggers at 9:00 AM PST daily

outreach_trigger (If Built)

 Mark test entry as "Draft Ready" for outreach
 Wait 15 minutes (or trigger manually)
 Verify Creator Outreach agent called
 Verify message drafted
 Verify entry updated to "Awaiting Approval"
 Tom reviews message quality


Agent Tests
Content Idea Miner

 Pass test input (sample article URL + user notes)
 Verify 2-5 ideas generated
 Check idea quality:

 Specific, actionable descriptions
 Reference appropriate formulas (Use Case Spotlight, Hidden Cost, etc.)
 Platform-appropriate (LinkedIn ideas professional, Instagram visual)
 Use case clusters assigned correctly


 Verify ideas align with Brand Foundation voice
 Verify ideas avoid anti-patterns (no clinical claims, no competitor names)

Content Drafter

 Pass test approved idea (Social Post type)
 Verify platform-specific drafts generated (LinkedIn 150-250 words, Facebook 100-200, Instagram 80-150)
 Check voice match:

 Does it sound like Tom? (casual, fast-paced, self-deprecating humor)
 Does it avoid anti-patterns?
 Does it follow the specified formula?


 Pass test approved idea (Video Script type)
 Verify script has timestamps and natural language
 Verify storyboard notes are clear and actionable
 Tom reviews draft quality and provides feedback

Creator Outreach (If Integrated)

 Pass test creator info
 Verify message is personalized (not generic template)
 Verify message references Brand Foundation positioning
 Verify platform-appropriate tone (Twitter casual vs LinkedIn professional)
 Tom reviews message quality


Integration Tests
End-to-End Ideation Flow

 Capture content → Triage as "Ideation" → Send to COS → Ideas generated → Approve idea → Draft created → Approve draft → Scheduled in Buffer → Posted → Metrics tracked
 Verify no data loss at any step
 Verify relations intact throughout flow
 Verify all statuses update correctly

End-to-End Outreach Flow (If Built)

 Capture content → Triage as "Outreach" → Mark as "Draft Ready" → Message drafted → Approve → Send → Status updated

Dual-Purpose Capture

 Mark entry as BOTH "Outreach" AND "Ideation"
 Verify both workflows trigger correctly
 Verify no conflicts or errors


Performance & Reliability Tests
Workflow Polling Frequency

 Verify workflows don't trigger too frequently (causing noise)
 Verify workflows don't trigger too slowly (causing delays)
 Recommended: 5 minutes for ideation/drafting, 15 minutes for outreach

Error Recovery

 Simulate Notion API failure → Verify retry logic works
 Simulate Buffer API failure → Verify draft marked as "Scheduling Error"
 Simulate agent timeout → Verify status updated to "Error - Retry"

Data Integrity

 Verify relations always link correctly (no orphaned entries)
 Verify statuses always update (no entries stuck in "Processing")
 Verify no duplicate entries created


User Experience Tests
Tom's Workflow (Ideation)

 Tom captures 5 pieces of content via iOS
 Tom triages all as "Ideation" in Notion
 Tom sets all to "Sent to COS"
 Tom receives 10-15 ideas within 1 hour
 Tom approves 5 ideas
 Tom receives 5 drafts within 1 hour
 Tom edits 2 drafts, approves all 5
 Tom schedules all 5 in Buffer
 Tom verifies Buffer queue shows all 5 posts

Tom's Workflow (Outreach - If Built)

 Tom captures creator profile
 Tom triages as "Outreach Target"
 Tom adds notes on why reaching out
Continue4:47 PM
 Tom marks as "Draft Ready"
 Tom receives message draft within 1 hour
 Tom reviews, edits, approves
 Message sent successfully


Documentation Tests
COS_SETUP.md

 Contains all database IDs
 Contains all webhook URLs
 Contains workflow names and purposes
 Contains API token placeholders (Buffer, Unsplash, Pexels)
 Contains troubleshooting section

COS_STATUS.md

 Lists what's built and working
 Lists any known issues
 Lists items deferred to BACKLOG.md
 Includes testing results

Handoff Document for Tom

 Clear instructions on how to use COS
 Screenshots or examples where helpful
 Troubleshooting common issues
 Contact/support information


Final Sign-Off
Before considering COS "complete," verify:

 All Phase 1-4 deliverables complete and tested
 (Optional) Phase 5 deliverables complete or explicitly deferred to BACKLOG.md
 All documentation created (COS_SETUP.md, COS_STATUS.md, Handoff doc)
 Tom has successfully tested end-to-end workflows
 Tom is comfortable using the system independently
 Items for BACKLOG.md identified and ready to add

Tom's Final Approval:

 I understand how to capture content
 I understand how to triage and approve ideas
 I understand how to review and approve drafts
 I understand how to schedule posts in Buffer
 I'm ready to start the Pre-Launch Content Sprint
 COS is approved and ready for production use


END OF COS IMPLEMENTATION BRIEF

SUMMARY FOR TOM
You now have a complete, comprehensive Implementation Brief for the Content Operating System (COS).
What's Included:

✅ Brand Foundation (positioning, voice, messaging)
✅ COS Content Playbook (formulas, use cases, video frameworks, community engagement)
✅ Technical Specifications (Notion databases, workflows, agents - exact implementation details)
✅ Build Order (phased approach over 2 weeks with testing at each stage)
✅ Pre-Launch Content Sprint Plan (6-week plan to build 30 posts + 15 videos before launch)
✅ Post-Build Tasks (what you do manually)
✅ Items for BACKLOG.md (future enhancements)
✅ Testing & Validation (comprehensive checklist)
✅ CC Handoff Prompt (what to paste into Claude Code to start the build)

Next Steps:

Review this entire brief (take your time)
When ready, copy the "CC Handoff Prompt" section (at the top of this document)
Open Claude Code, paste the prompt
Attach this full brief as context
Answer CC's setup questions (database IDs, API keys, etc.)
Let CC build the COS over 2 weeks

What You'll Be Able to Do After Build:

Capture content with one tap
Get AI-generated content ideas automatically
Receive platform-specific drafts (posts + video scripts)
Schedule to Buffer automatically
Track engagement metrics
Build a content library of 30 posts + 15 videos before launch
Post on autopilot through April

This system is designed to give you back 50-60 hours by automating ideation, drafting, and scheduling—so you can focus on running the business, not thinking up social media posts.
Ready to build? 🚀