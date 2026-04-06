# AI_PROMPTING.md — How to Work with AI Effectively

> A practical guide compiled from real usage patterns.
> Built for: a marketer learning to use AI as a development and thinking partner.

---

## CORE PRINCIPLE

**AI is a collaborator, not a search engine.**
The quality of what you get back is almost entirely determined by the quality of what you put in.
Treat it like briefing a very smart contractor who knows nothing about your specific situation.

---

## THE GOLDEN RULES

### 1. Always give context first
Bad:
```
how do i pull data from an api
```

Good:
```
I'm building a Python tool that pulls marketing data from the Meta Ads API.
I'm a beginner-intermediate Python developer on Linux.
How do I authenticate and make my first API call?
```

### 2. Be specific about your output format
Bad:
```
explain attribution models
```

Good:
```
Explain the 3 most common marketing attribution models in plain English.
Give a one-line summary of each, then a concrete example using Google Ads + Meta Ads.
Keep it under 200 words.
```

### 3. Tell the AI your level
Always include one of:
- "I'm a beginner in Python"
- "I understand basic Python but not APIs yet"
- "Explain this like I'm a marketer, not an engineer"

This prevents over-explanation AND under-explanation.

### 4. Ask for steps, not just answers
Bad:
```
write me a script to analyze my data
```

Good:
```
Walk me through the steps to build a script that:
1. Loads a CSV of Meta Ads data
2. Calculates ROAS per campaign
3. Prints the top 3 campaigns

Show me the code step by step and explain each part briefly.
```

### 5. Use constraints
AI responses without constraints tend to bloat. Use:
- "Keep the code under 30 lines"
- "Respond in bullet points only"
- "Give me only the function, no explanation"
- "One approach only — the simplest one"

---

## PROMPT TEMPLATES

### 🔧 For coding tasks
```
Context: [brief project description]
My level: [beginner / intermediate]
Task: [what you want to build or fix]
Constraints: [language, libraries, length, style]
Output format: [code only / code + explanation / pseudocode first]
```

### 🐛 For debugging
```
Here is my code: [paste code]
Here is the error I'm getting: [paste error]
What I've already tried: [list attempts]
What I think the issue might be: [your guess]
```

### 💡 For learning a concept
```
Explain [concept] to me as if I'm a digital marketer learning Python.
Use an analogy from marketing if possible.
Then show me a minimal code example (under 20 lines).
```

### 📋 For planning / architecture
```
I want to build [X].
My constraints are: [time / skill level / tools available]
Give me:
1. A high-level approach (3–5 steps)
2. What I should build first
3. What I should skip for now
```

### 🔄 For continuing a session
```
Here is my project context: [paste PROJECT_CONTEXT.md]
Last session I worked on: [brief description]
Today I want to: [specific task]
```

---

## ADVANCED TECHNIQUES

### Chain of thought — ask the AI to think before answering
Add this to complex questions:
```
Think through this step by step before giving me your answer.
```

### Negative examples — tell it what NOT to do
```
Explain X. Do NOT use jargon. Do NOT give me more than 3 approaches.
```

### Ask for options with tradeoffs
```
Give me 2–3 ways to solve this. For each, tell me:
- What it's best for
- What the downside is
- Which you'd recommend for my situation
```

### Role assignment
```
You are a senior Python developer reviewing my code.
Be direct. Point out anything that would fail in production.
```

### Iterate, don't restart
Instead of starting over when output is wrong:
```
That's close but [specific issue]. Can you adjust [specific thing] while keeping everything else the same?
```

---

## WORKING WITH CLAUDE SPECIFICALLY

### Memory
Claude has no memory between conversations. Always paste PROJECT_CONTEXT.md at the start of a new session.

### Long conversations
In a long session, Claude can drift. If answers start feeling off, re-anchor:
```
Reminder of context: [paste key section from PROJECT_CONTEXT.md]
```

### Artifacts / files
Claude can create files, write code, and build interactive tools directly.
If you want a file you can download, say: "Create this as a file I can download."

### When Claude is wrong
Don't just accept it. Say:
```
I don't think that's right because [reason]. Can you reconsider?
```
Claude responds well to pushback with a reason.

### Best uses for Claude vs ChatGPT
| Task | Claude | ChatGPT |
|------|--------|---------|
| Long document analysis | ✅ Better | OK |
| Code with explanation | ✅ Strong | ✅ Strong |
| Creative writing | ✅ Strong | ✅ Strong |
| Browsing / search | Both support | Both support |
| Building interactive artifacts | ✅ Native | Limited |
| Casual chat | Both fine | Both fine |

---

## PROMPTING ANTI-PATTERNS (avoid these)

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| "Write me an app" | Too vague, produces bloat | Scope it: "Write a Python function that does X" |
| "Is this good?" | No criteria given | "Review this for: readability, error handling, and beginner-friendliness" |
| "Fix my code" (no error) | AI guesses what's wrong | Always include the error message |
| Starting over every session | AI loses all context | Use PROJECT_CONTEXT.md |
| Accepting first output | First drafts are rarely optimal | Always ask for at least one iteration |

---

## QUICK REFERENCE — PHRASES THAT IMPROVE OUTPUTS

| When you want... | Add this to your prompt |
|---|---|
| Simpler output | "Explain like I'm a marketer, not a developer" |
| Shorter output | "Be concise. Max 150 words." |
| More practical | "Give me a real example, not a theoretical one" |
| Step by step | "Walk me through this step by step" |
| Options | "Give me 3 approaches with tradeoffs" |
| Just the code | "Code only. No explanation." |
| Just the concept | "No code. Just explain the concept." |
| Honest feedback | "Be direct. Tell me what's wrong with this." |

---

*This document is a living reference. Update it as you discover what works.*
*Last updated: 2026-04-06*
