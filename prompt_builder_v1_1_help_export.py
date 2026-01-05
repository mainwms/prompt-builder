
import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Prompt Builder", layout="centered")

# ==========================================================
# Prompt Builder v1.1 — Help + Exports + Clarity (No AI calls)
# ==========================================================

APP_TITLE = "Prompt Builder"
APP_TAGLINE = "Build the right prompt — the first time."
APP_SUBTEXT = "Choose a tool, answer a few guided questions, then copy/paste a prompt that reduces ambiguity and assumptions."

# -------------------------
# GLOBAL STRICT MODE BLOCK
# -------------------------
STRICT_BLOCK = """Rules:
- Do not invent facts, names, features, prices, or statistics.
- If required information is missing, ask up to 3 clarifying questions before proceeding.
- Clearly label any assumptions or inferences.
- Prefer accuracy and clarity over creativity.
"""

# -------------------------
# TOOL DEFINITIONS (schema-driven)
# -------------------------
TOOLS = {
    "ChatGPT": {
        "description": "Writing, planning, reasoning, and role-based tasks.",
        "who_its_for": "Creators, marketers, students, and builders who want clear output with constraints.",
        "best_for": [
            "Drafting posts, scripts, emails, plans",
            "Role-based reasoning (Act as …)",
            "Structured outputs (steps, tables, checklists)"
        ],
        "questions": [
            {
                "id": "Goal",
                "label": "Goal",
                "type": "text",
                "help": "In one sentence: what do you want the AI to produce? Example: 'Write a LinkedIn post explaining prompt builders.'",
                "placeholder": "E.g., Write a LinkedIn post explaining why prompt builders help beginners."
            },
            {
                "id": "Audience",
                "label": "Audience",
                "type": "text",
                "help": "Who will read/use the output? Example: 'Beginners in AI tools' or 'Prospective customers'.",
                "placeholder": "E.g., Beginners exploring AI tools"
            },
            {
                "id": "Tone",
                "label": "Tone",
                "type": "single",
                "options": ["Neutral", "Professional", "Friendly", "Direct (no fluff)", "Persuasive"],
                "help": "Pick the voice you want the output written in."
            },
            {
                "id": "Output Format",
                "label": "Output Format",
                "type": "single",
                "options": ["Bullets", "Numbered steps", "Table", "Short paragraphs", "Checklist"],
                "help": "How should the answer be formatted?"
            },
            {
                "id": "Depth",
                "label": "Depth",
                "type": "single",
                "options": ["Brief", "Detailed", "Deep dive"],
                "help": "How much detail do you want?"
            },
            {
                "id": "Role (optional)",
                "label": "Role (optional)",
                "type": "text",
                "help": "Optional: make the AI behave like a specialist. Example: 'marketing strategist' or 'copy editor'. Leave blank if unsure.",
                "placeholder": "E.g., marketing strategist"
            },
        ],
        "template": """{ROLE_BLOCK}Goal:
{Goal}

Audience:
{Audience}

Tone:
{Tone}

Output format:
{Output Format}

Depth:
{Depth}
"""
    },

    "Gemini": {
        "description": "Structured workflows and multi-step outputs.",
        "who_its_for": "Anyone building repeatable workflows, plans, calendars, or structured documents.",
        "best_for": [
            "Workflows and multi-step plans",
            "Structured outputs with headings/steps",
            "Optional visual creative workflow (Flow / Nano Banana Pro)"
        ],
        "questions": [
            {
                "id": "Task",
                "label": "Task",
                "type": "text",
                "help": "What should Gemini do? Example: 'Create a weekly content workflow'.",
                "placeholder": "E.g., Create a weekly content workflow for LinkedIn posts."
            },
            {
                "id": "Objective",
                "label": "Objective",
                "type": "text",
                "help": "What does 'success' look like? Example: 'A numbered plan I can follow'.",
                "placeholder": "E.g., A step-by-step plan with templates I can reuse."
            },
            {
                "id": "Structure",
                "label": "Structure",
                "type": "single",
                "options": ["Numbered steps", "Outline", "Table", "Headings + bullets"],
                "help": "Choose the structure Gemini should follow."
            },
            {
                "id": "Depth",
                "label": "Depth",
                "type": "single",
                "options": ["High-level", "Practical detail", "Very detailed"],
                "help": "How detailed should the workflow be?"
            },
        ],
        "visual_block": """Visual Creative Step (Flow / Nano Banana Pro workflow):
- Create a short creative brief for a supporting image.
- Generate image prompt(s) suitable for Flow / Nano Banana Pro.
- Provide 2 variations.
- Do NOT assume brand colors, logos, or assets.
- If visual inputs (brand colors, product name, style) are missing, ask before generating.
""",
        "template": """Task:
{Task}

Objective:
{Objective}

Structure:
{Structure}

Depth:
{Depth}
"""
    },

    "NotebookLM": {
        "description": "Source-based research and step-by-step learning.",
        "who_its_for": "People who want grounded answers based on their own sources (docs, PDFs, notes).",
        "best_for": [
            "Research assistant behavior",
            "Blueprints based on sources",
            "Step-by-step learning (type 'next')"
        ],
        "questions": [
            {
                "id": "Goal",
                "label": "Goal",
                "type": "text",
                "help": "What do you want NotebookLM to help you do with your sources? Example: 'Build a launch plan from my notes.'",
                "placeholder": "E.g., Build a step-by-step launch plan based on my uploaded notes."
            },
            {
                "id": "Experience Level",
                "label": "Experience Level",
                "type": "single",
                "options": ["Beginner", "Intermediate", "Advanced"],
                "help": "How technical should explanations be?"
            },
        ],
        "template": """You are an AI research assistant using my provided sources.

Goal:
{Goal}

Assume my experience level is {Experience Level}.
Guide me step by step.
Present one stage at a time.
After each stage, stop and wait for me to type "next" before continuing.

Use my sources first.
If anything is missing, ask clarifying questions.
Clearly label anything that is not supported by sources.
"""
    },

    "Gemini Gems": {
        "description": "Persistent assistants with narrow roles.",
        "who_its_for": "Users who want a reusable assistant that stays focused on one job.",
        "best_for": [
            "A dedicated assistant (e.g., 'email calendar helper')",
            "Stable behavior across chats",
            "Clear boundaries (avoid scope creep)"
        ],
        "questions": [
            {
                "id": "Role",
                "label": "Role",
                "type": "text",
                "help": "Name the assistant role. Example: 'marketing assistant' or 'research helper'.",
                "placeholder": "E.g., marketing assistant"
            },
            {
                "id": "Scope",
                "label": "Scope",
                "type": "text",
                "help": "What is it allowed to do? Keep it narrow. Example: 'Plan content calendars and outline posts.'",
                "placeholder": "E.g., Plan content calendars and outline posts; do not write final copy unless asked."
            },
            {
                "id": "Avoid",
                "label": "Avoid",
                "type": "text",
                "help": "What should it NOT do? Example: 'Don't guess; ask questions; no legal advice'.",
                "placeholder": "E.g., Do not invent facts; do not expand scope; ask questions when unclear."
            },
        ],
        "template": """You are a persistent Gemini Gem.

Role:
{Role}

Scope:
{Scope}

You should NOT:
{Avoid}

Confirm you understand your role and boundaries before starting.
"""
    },

    "Google AI Studio": {
        "description": "App, tool, and calculator generation.",
        "who_its_for": "Builders who want small, functional web tools from a clear spec.",
        "best_for": [
            "Simple web apps and calculators",
            "Utilities with defined inputs/outputs",
            "Clean requirements and validation"
        ],
        "questions": [
            {
                "id": "App Type",
                "label": "App Type",
                "type": "single",
                "options": ["Calculator", "Generator", "Form-based tool", "Dashboard"],
                "help": "Pick the kind of app you want AI Studio to generate."
            },
            {
                "id": "Purpose",
                "label": "Purpose",
                "type": "text",
                "help": "One sentence describing what the app does.",
                "placeholder": "E.g., Estimate monthly expenses from user inputs."
            },
            {
                "id": "Inputs",
                "label": "Inputs",
                "type": "text",
                "help": "What does the user enter? Example: 'numbers for rent, food, utilities'.",
                "placeholder": "E.g., Numeric fields for rent, utilities, food, transport."
            },
            {
                "id": "Outputs",
                "label": "Outputs",
                "type": "text",
                "help": "What should the app show? Example: 'total, breakdown table, chart'.",
                "placeholder": "E.g., Total monthly cost + breakdown table."
            },
            {
                "id": "Constraints",
                "label": "Constraints",
                "type": "single",
                "options": ["Fully functional + validation", "Minimal demo only", "Explain logic in comments"],
                "help": "Choose a constraint set. You can refine inside the AI Studio chat too."
            },
        ],
        "template": """Build a {App Type} application.

Purpose:
{Purpose}

Inputs:
{Inputs}

Outputs:
{Outputs}

Constraints:
{Constraints}

Provide complete working code.
Validate inputs and handle edge cases.
Ask clarifying questions only if required details are missing.
"""
    },

    "Google Antigravity": {
        "description": "Reframing and breaking mental blocks.",
        "who_its_for": "Anyone who feels stuck and wants better angles before executing.",
        "best_for": [
            "Reframing a problem",
            "Generating better options",
            "Finding missing assumptions"
        ],
        "questions": [
            {
                "id": "Situation",
                "label": "Situation",
                "type": "text",
                "help": "Describe the situation in 1–3 sentences.",
                "placeholder": "E.g., I want to build a prompt tool but feel overwhelmed by options."
            },
            {
                "id": "Desired Outcome",
                "label": "Desired Outcome",
                "type": "text",
                "help": "What do you want Antigravity to produce? Example: '5 alternative approaches'.",
                "placeholder": "E.g., Give me 5 alternative directions and the best next step."
            },
            {
                "id": "Challenge Level",
                "label": "Challenge Level",
                "type": "single",
                "options": ["Gentle", "Balanced", "Hard pushback"],
                "help": "How hard should it challenge your assumptions?"
            },
        ],
        "template": """You are a reframing assistant.

Situation:
{Situation}

Desired outcome:
{Desired Outcome}

Challenge level:
{Challenge Level}

Challenge assumptions and propose alternative perspectives.
Focus on reframing, not execution.

If anything is unclear, ask up to 3 clarifying questions before proceeding.
"""
    }
}

# -------------------------
# SIDEBAR: QUICK START
# -------------------------
with st.sidebar:
    st.header("Quick Start")
    st.write("1) Choose a tool\n2) Answer the questions\n3) Generate prompt\n4) Copy → paste into the tool")
    st.divider()
    st.subheader("Who this is for")
    st.write("Beginners who want guidance *and* advanced users who want predictable, reusable prompts.")
    st.divider()
    strict_mode = st.toggle("Strict mode (recommended)", value=True, help="Reduces hallucinations by forcing clarifying questions instead of guessing.")
    st.caption("Tip: Leave Strict mode ON unless you have complete info and want more creative flexibility.")

# -------------------------
# MAIN UI
# -------------------------
st.title(APP_TITLE)
st.subheader(APP_TAGLINE)
st.caption(APP_SUBTEXT)

tool_name = st.selectbox("Which AI tool are you using?", list(TOOLS.keys()), help="Pick the exact tool you will paste the prompt into.")
tool = TOOLS[tool_name]

with st.expander("What this tool does (and why it helps)", expanded=True):
    st.write("This app **builds** a prompt from your selections. It does not guess.")
    st.write("It’s designed to help you get outputs that are **clear, structured, and less assumption-prone**.")
    st.write(f"**Selected tool:** {tool_name}")
    st.write(f"**Best for:** {', '.join(tool['best_for'])}")
    st.write(f"**Who it’s for:** {tool['who_its_for']}")

st.info(tool["description"])

# Questions (schema-driven)
answers = {}
for q in tool["questions"]:
    qid = q["id"]
    qtype = q["type"]
    label = q["label"]
    help_text = q.get("help", None)

    if qtype == "text":
        answers[qid] = st.text_input(
            label,
            value="",
            placeholder=q.get("placeholder", ""),
            help=help_text
        )
    elif qtype == "single":
        answers[qid] = st.selectbox(
            label,
            q["options"],
            index=0,
            help=help_text
        )

# Gemini: visual workflow toggle (Nano Banana Pro via Flow)
visual_step = False
if tool_name == "Gemini":
    visual_step = st.toggle(
        "Include visual creative step (Flow / Nano Banana Pro workflow)",
        value=False,
        help="Adds a creative brief + image prompt block you can paste into Flow/Nano Banana Pro. Does not generate images automatically."
    )

st.divider()

# Generate prompt
if st.button("Generate Prompt", type="primary"):
    # Basic validation: require non-empty for text fields except optional role
    missing = []
    for q in tool["questions"]:
        if q["type"] == "text":
            if q["id"] == "Role (optional)":
                continue
            if not answers.get(q["id"], "").strip():
                missing.append(q["label"])

    if missing:
        st.error("Please fill in: " + ", ".join(missing))
        st.stop()

    prompt = tool["template"]

    # ChatGPT role block
    role_block = ""
    if tool_name == "ChatGPT":
        role_val = answers.get("Role (optional)", "").strip()
        if role_val:
            role_block = f"Act as: {role_val}\n\n"
    prompt = prompt.replace("{ROLE_BLOCK}", role_block)

    # Replace placeholders
    for k, v in answers.items():
        prompt = prompt.replace("{" + k + "}", v)

    # Gemini visual block
    if tool_name == "Gemini" and visual_step:
        prompt += "\n" + tool["visual_block"]

    # Strict mode
    if strict_mode:
        prompt += "\n" + STRICT_BLOCK

    # Store in session for downloads
    st.session_state["last_prompt"] = prompt
    st.session_state["last_tool"] = tool_name
    st.session_state["last_answers"] = answers
    st.success("Prompt generated. Copy and paste it into your selected AI tool.")

# Output panel
prompt_out = st.session_state.get("last_prompt", "")
if prompt_out:
    st.subheader("Your Prompt")
    st.caption(f"Paste into: {st.session_state.get('last_tool', tool_name)}")
    st.text_area("Copy from here:", prompt_out, height=360)

    # Exports
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename_txt = f"prompt_{st.session_state.get('last_tool', 'tool').replace(' ', '_').lower()}_{ts}.txt"
    filename_json = f"prompt_inputs_{st.session_state.get('last_tool', 'tool').replace(' ', '_').lower()}_{ts}.json"

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download Prompt (.txt)",
            data=prompt_out.encode("utf-8"),
            file_name=filename_txt,
            mime="text/plain"
        )
    with col2:
        payload = {
            "tool": st.session_state.get("last_tool", tool_name),
            "strict_mode": strict_mode,
            "visual_step_enabled": bool(tool_name == "Gemini" and visual_step),
            "answers": st.session_state.get("last_answers", answers),
            "generated_at": ts
        }
        st.download_button(
            "Download Inputs (.json)",
            data=json.dumps(payload, indent=2).encode("utf-8"),
            file_name=filename_json,
            mime="application/json"
        )

    with st.expander("Examples (quick copy ideas)"):
        if tool_name == "ChatGPT":
            st.write("- Goal: Write a LinkedIn post explaining how to use a prompt builder.")
            st.write("- Audience: Beginners in AI tools")
            st.write("- Role (optional): marketing strategist")
        elif tool_name == "Gemini":
            st.write("- Task: Create a 7-day content plan for LinkedIn.")
            st.write("- Objective: Provide a daily post topic + a short outline.")
            st.write("- Turn ON visual step if you want an image prompt for Flow / Nano Banana Pro.")
        elif tool_name == "NotebookLM":
            st.write("- Goal: Summarize my notes and create a step-by-step action plan.")
            st.write("- Upload your sources into NotebookLM first, then paste the prompt.")
        elif tool_name == "Google AI Studio":
            st.write("- Purpose: Build a simple calculator users can embed on a website.")
            st.write("- Inputs: numeric fields")
            st.write("- Outputs: total + breakdown table")
        else:
            st.write("Use short, concrete statements. If unsure, describe what success looks like.")

else:
    st.caption("Tip: Answer the questions above, then click **Generate Prompt**.")
