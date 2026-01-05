import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Prompt Builder", layout="centered")

# ------------------------------------------------------------
# Prompt Builder v1.1 (Guided Questions RESTORED)
# - Adds question flows for every tool/category:
#   ChatGPT, Gemini, NotebookLM, Gemini Gems, Google AI Studio, Google Antigravity
# - Adds NotebookLM Podcast option as "Coming soon" (honest + visible)
# - Keeps this as a single-file Streamlit app (same entrypoint filename safe)
# ------------------------------------------------------------

APP_TITLE = "Prompt Builder"
APP_TAGLINE = "Answer a few questions → get a prompt you can copy/paste."
APP_SUBTEXT = (
    "This tool helps beginners by asking the right questions first. "
    "It does not call any AI by itself — it only builds a prompt for you."
)

STRICT_RULES = """Strict rules (recommended):
- Do not invent facts, names, features, prices, or statistics.
- If required information is missing, ask up to 3 clarifying questions before proceeding.
- Clearly label any assumptions.
- Prefer accuracy and clarity over creativity.
"""

TOOLS = {
    "ChatGPT": {
        "desc": "For writing, planning, brainstorming, and structured outputs.",
        "who": "Creators, marketers, students, and builders who want clear output with constraints.",
        "questions": [
            {
                "id": "Goal",
                "label": "What do you want ChatGPT to produce?",
                "type": "text",
                "help": "One sentence is enough. Example: 'Write a LinkedIn post announcing Prompt Builder.'",
                "ph": "E.g., Write a LinkedIn post announcing Prompt Builder."
            },
            {
                "id": "Audience",
                "label": "Who is this for?",
                "type": "text",
                "help": "Example: 'Beginners exploring AI tools' or 'Small business owners'.",
                "ph": "E.g., Beginners exploring AI tools"
            },
            {
                "id": "Tone",
                "label": "Tone",
                "type": "single",
                "options": ["Neutral", "Professional", "Friendly", "Direct (no fluff)", "Persuasive"],
                "help": "Pick the voice you want in the output."
            },
            {
                "id": "Format",
                "label": "Output format",
                "type": "single",
                "options": ["Bullets", "Numbered steps", "Short paragraphs", "Checklist", "Table"],
                "help": "How should the answer be structured?"
            },
            {
                "id": "Constraints",
                "label": "Any constraints or must-includes?",
                "type": "text",
                "help": "Optional, but helpful. Example: 'Include 3 bullet benefits and a call-to-action.'",
                "ph": "E.g., Include 3 benefits and a call-to-action.",
                "optional": True
            },
            {
                "id": "Role",
                "label": "Role (optional)",
                "type": "text",
                "help": "Optional: 'marketing strategist', 'copy editor', 'product manager'. Leave blank if unsure.",
                "ph": "E.g., marketing strategist",
                "optional": True
            },
        ],
        "template": """{ROLE_BLOCK}Task:
{Goal}

Audience:
{Audience}

Tone:
{Tone}

Format:
{Format}

Constraints / must-includes:
{Constraints}
"""
    },

    "Gemini": {
        "desc": "For structured workflows, calendars, plans, and multi-step outputs.",
        "who": "Anyone who wants a reusable workflow or a structured plan.",
        "questions": [
            {
                "id": "Task",
                "label": "What should Gemini do?",
                "type": "text",
                "help": "Example: 'Create a 2-week LinkedIn content calendar for Prompt Builder.'",
                "ph": "E.g., Create a 2-week LinkedIn content calendar for Prompt Builder."
            },
            {
                "id": "Goal",
                "label": "What does success look like?",
                "type": "text",
                "help": "Example: 'A day-by-day calendar with post ideas and short outlines.'",
                "ph": "E.g., Day-by-day calendar with post ideas and short outlines."
            },
            {
                "id": "Structure",
                "label": "Preferred structure",
                "type": "single",
                "options": ["Numbered steps", "Outline", "Table", "Headings + bullets"],
                "help": "How should Gemini format the output?"
            },
            {
                "id": "Detail",
                "label": "Detail level",
                "type": "single",
                "options": ["High-level", "Practical detail", "Very detailed"],
                "help": "How much detail do you want?"
            },
            {
                "id": "Constraints",
                "label": "Constraints (optional)",
                "type": "text",
                "help": "Example: 'No jargon, include examples, keep each post under 1200 characters.'",
                "ph": "E.g., No jargon; include examples; keep it short.",
                "optional": True
            },
        ],
        "template": """Task:
{Task}

Success criteria:
{Goal}

Structure:
{Structure}

Detail level:
{Detail}

Constraints:
{Constraints}
""",
        "visual_block": """Optional visual creative step (Flow / Nano Banana Pro workflow):
- Create a short creative brief for one supporting image that matches the task above.
- Provide 2 image prompt variations.
- Do NOT assume brand colors, logos, or assets.
- If visual inputs (brand colors, product name, style) are missing, ask first.
"""
    },

    "NotebookLM": {
        "desc": "For source-based research and step-by-step learning grounded in your uploaded sources.",
        "who": "People who want grounded output that stays tied to their sources.",
        "questions": [
            {
                "id": "UseCase",
                "label": "What are you using NotebookLM for?",
                "type": "single",
                "options": [
                    "Research a topic from my sources",
                    "Learn step-by-step from my sources",
                    "Create a plan/blueprint from my sources",
                    "Podcast planning (coming soon)"
                ],
                "help": "Pick the closest match. Podcast planning is shown as 'coming soon' to be honest and avoid confusion."
            },
            {
                "id": "Sources",
                "label": "What sources will you add to NotebookLM?",
                "type": "single",
                "options": ["PDF(s)", "Google Doc(s)", "Web articles", "Mixed sources"],
                "help": "NotebookLM works best when you upload the sources first."
            },
            {
                "id": "Goal",
                "label": "What do you want NotebookLM to produce from your sources?",
                "type": "text",
                "help": "Be specific. Example: 'Summarize and produce a step-by-step launch checklist.'",
                "ph": "E.g., Summarize my notes and produce a step-by-step checklist."
            },
            {
                "id": "Experience",
                "label": "Your experience level",
                "type": "single",
                "options": ["Beginner", "Intermediate", "Advanced"],
                "help": "This controls how technical the explanations should be."
            },
            {
                "id": "StepMode",
                "label": "How should it guide you?",
                "type": "single",
                "options": ["One stage at a time (type 'next')", "All at once"],
                "help": "The transcript demonstrated the 'type next' approach."
            },
        ],
        "template": """You are an AI research assistant using ONLY my provided sources in NotebookLM.

My sources type:
{Sources}

My goal:
{Goal}

My experience level:
{Experience}

Guidance mode:
{StepMode}

Rules:
- Use my sources first. Stay grounded in them.
- If something is missing from my sources, ask up to 3 clarifying questions.
- Clearly label anything that is not supported by sources.

Use case:
{UseCase}

{PODCAST_NOTICE}
"""
    },

    "Gemini Gems": {
        "desc": "For creating a focused, reusable assistant with boundaries (a ‘Gem’).",
        "who": "Users who want a reusable assistant that stays focused on one job.",
        "questions": [
            {
                "id": "GemName",
                "label": "Name your Gem",
                "type": "text",
                "help": "Example: 'Email Calendar Helper' or 'LinkedIn Post Assistant'.",
                "ph": "E.g., LinkedIn Post Assistant"
            },
            {
                "id": "Role",
                "label": "What role should it play?",
                "type": "text",
                "help": "Example: 'Act as a social media marketing assistant.'",
                "ph": "E.g., Act as a social media marketing assistant."
            },
            {
                "id": "Scope",
                "label": "What is it allowed to do?",
                "type": "text",
                "help": "Keep it narrow and clear. Example: 'Create outlines and calendars; don't write final copy unless asked.'",
                "ph": "E.g., Create outlines + calendars; don't write final copy unless asked."
            },
            {
                "id": "Avoid",
                "label": "What should it NOT do?",
                "type": "text",
                "help": "Example: 'Do not guess; ask questions when unclear; no legal advice.'",
                "ph": "E.g., Do not invent facts; ask questions when unclear."
            },
            {
                "id": "OutputStyle",
                "label": "Preferred output style",
                "type": "single",
                "options": ["Bullets", "Numbered steps", "Table", "Short paragraphs"],
                "help": "How you want the Gem to respond by default."
            },
        ],
        "template": """Create a Gemini Gem with the following configuration.

Gem name:
{GemName}

Role:
{Role}

Allowed scope:
{Scope}

Must NOT do:
{Avoid}

Default output style:
{OutputStyle}

Before starting, confirm you understand the role and boundaries.
"""
    },

    "Google AI Studio": {
        "desc": "For generating small web apps/tools when you provide clear inputs and outputs.",
        "who": "Builders who want small functional utilities (calculators, generators, simple tools).",
        "questions": [
            {
                "id": "AppType",
                "label": "What type of app do you want to build?",
                "type": "single",
                "options": ["Calculator", "Generator", "Form-based tool", "Dashboard"],
                "help": "Pick the closest match."
            },
            {
                "id": "Users",
                "label": "Who is the app for?",
                "type": "text",
                "help": "Example: 'investors', 'students', 'small business owners'.",
                "ph": "E.g., small business owners"
            },
            {
                "id": "Problem",
                "label": "What problem does this app solve?",
                "type": "text",
                "help": "One sentence. Example: 'Estimate monthly taxes from a portfolio.'",
                "ph": "E.g., Estimate monthly costs from user inputs."
            },
            {
                "id": "Inputs",
                "label": "What inputs does the user provide?",
                "type": "text",
                "help": "List the fields. Example: 'income, expenses, tax rate'.",
                "ph": "E.g., income, rent, utilities, food, transport"
            },
            {
                "id": "Outputs",
                "label": "What outputs should the app show?",
                "type": "text",
                "help": "Example: 'total + breakdown table + chart'.",
                "ph": "E.g., total + breakdown table"
            },
            {
                "id": "Constraints",
                "label": "Build constraints",
                "type": "single",
                "options": ["Fully functional + input validation", "Minimal demo only", "Explain logic with comments"],
                "help": "Choose how robust it should be."
            },
        ],
        "template": """Build a {AppType} web app.

Target users:
{Users}

Problem to solve:
{Problem}

Inputs (fields and types):
{Inputs}

Outputs (what to show):
{Outputs}

Constraints:
{Constraints}

Requirements:
- Provide complete working code.
- Validate inputs and handle edge cases.
- Ask clarifying questions only if required details are missing.
"""
    },

    "Google Antigravity": {
        "desc": "For reframing a problem and breaking mental blocks before execution.",
        "who": "Anyone who feels stuck and wants better angles before taking action.",
        "questions": [
            {
                "id": "Situation",
                "label": "Describe the situation",
                "type": "text",
                "help": "1–3 sentences about what’s going on.",
                "ph": "E.g., I want to grow my tool but I’m unsure what to focus on first."
            },
            {
                "id": "Outcome",
                "label": "What outcome do you want?",
                "type": "text",
                "help": "Example: 'Give me 5 alternative approaches and the best next step.'",
                "ph": "E.g., Give me 5 alternative approaches and the best next step."
            },
            {
                "id": "Pushback",
                "label": "How hard should it challenge assumptions?",
                "type": "single",
                "options": ["Gentle", "Balanced", "Hard pushback"],
                "help": "Pick how direct you want it to be."
            },
            {
                "id": "Constraints",
                "label": "Constraints (optional)",
                "type": "text",
                "help": "Example: 'No therapy tone. No pep talk. Just practical reframes.'",
                "ph": "E.g., No pep talk; give practical reframes.",
                "optional": True
            },
        ],
        "template": """You are a reframing assistant.

Situation:
{Situation}

Desired outcome:
{Outcome}

Challenge level:
{Pushback}

Constraints:
{Constraints}

Instructions:
- Challenge assumptions and propose alternative perspectives.
- Focus on reframing and options, not execution.
- If anything is unclear, ask up to 3 clarifying questions before proceeding.
"""
    },
}


def render_question(q: dict):
    qid = q["id"]
    qtype = q.get("type")
    label = q.get("label", qid)
    help_text = q.get("help", None)

    if qtype == "text":
        val = st.text_input(
            label,
            value="",
            placeholder=q.get("ph", ""),
            help=help_text
        )
        return qid, val
    if qtype == "single":
        opts = q.get("options", [])
        val = st.selectbox(label, opts, index=0, help=help_text)
        return qid, val

    st.warning(f"Unsupported question type: {qtype}")
    return qid, ""


def validate_required(tool_schema: dict, answers: dict):
    missing = []
    for q in tool_schema["questions"]:
        if q.get("optional"):
            continue
        if q.get("type") == "text" and not (answers.get(q["id"], "") or "").strip():
            missing.append(q.get("label", q["id"]))
    return missing


def assemble_prompt(tool_name: str, answers: dict, strict_mode: bool, include_visual: bool) -> str:
    schema = TOOLS[tool_name]
    prompt = schema["template"]

    # Role block (ChatGPT only)
    if tool_name == "ChatGPT":
        role = (answers.get("Role", "") or "").strip()
        role_block = f"Act as: {role}\n\n" if role else ""
        prompt = prompt.replace("{ROLE_BLOCK}", role_block)
    else:
        prompt = prompt.replace("{ROLE_BLOCK}", "")

    # Podcast notice (NotebookLM)
    if tool_name == "NotebookLM":
        use_case = answers.get("UseCase", "")
        podcast_notice = ""
        if "Podcast planning" in use_case:
            podcast_notice = (
                "NOTE (Podcast planning):\n"
                "- Podcast Mode inside this Prompt Builder is marked as COMING SOON.\n"
                "- For now, use this prompt to create a podcast plan grounded in your sources.\n"
                "- Ask for an episode outline, talking points, and a script draft.\n"
                "- Clearly separate what is sourced vs. what is suggested.\n"
            )
        prompt = prompt.replace("{PODCAST_NOTICE}", podcast_notice)
    else:
        prompt = prompt.replace("{PODCAST_NOTICE}", "")

    # Replace tokens
    for k, v in answers.items():
        prompt = prompt.replace("{" + k + "}", v if isinstance(v, str) else str(v))

    # Optional Gemini visual step
    if tool_name == "Gemini" and include_visual:
        prompt = prompt.strip() + "\n\n" + TOOLS["Gemini"]["visual_block"]

    # Strict mode
    if strict_mode:
        prompt = prompt.strip() + "\n\n" + STRICT_RULES

    return prompt.strip() + "\n"


# -------------------------
# UI
# -------------------------
st.title(APP_TITLE)
st.subheader(APP_TAGLINE)
st.caption(APP_SUBTEXT)

with st.expander("What this is / who it’s for", expanded=True):
    st.write(
        "**Prompt Builder** helps people who don’t know what to type into AI tools yet. "
        "You choose a tool, answer a few guided questions, then copy/paste the generated prompt."
    )
    st.write("**Important:** This app does not run AI. It only builds a prompt for you.")
    st.write("**Beginner-friendly:** the questions and “?” tips show what to enter and why.")

with st.sidebar:
    st.header("Quick Start")
    st.write("1) Pick a tool/category")
    st.write("2) Answer the questions")
    st.write("3) Click **Generate Prompt**")
    st.write("4) Copy → paste into the tool you selected")
    st.divider()
    strict_mode = st.toggle(
        "Strict mode (recommended)",
        value=True,
        help="Adds instructions that reduce guessing and hallucinations."
    )

tool_name = st.selectbox("Select a tool/category", list(TOOLS.keys()))
schema = TOOLS[tool_name]

st.info(schema["desc"])
st.caption(f"Who it’s for: {schema['who']}")

answers = {}
st.markdown("### Answer these questions")
for q in schema["questions"]:
    qid, val = render_question(q)
    answers[qid] = val

include_visual = False
if tool_name == "Gemini":
    include_visual = st.toggle(
        "Add optional visual creative step (Flow / Nano Banana Pro workflow)",
        value=False,
        help="Adds a short creative brief + image prompt block. This does NOT generate images automatically."
    )

st.divider()

if st.button("Generate Prompt", type="primary"):
    missing = validate_required(schema, answers)
    if missing:
        st.error("Please fill in: " + ", ".join(missing))
    else:
        prompt = assemble_prompt(tool_name, answers, strict_mode=strict_mode, include_visual=include_visual)
        st.session_state["last_prompt"] = prompt
        st.session_state["last_tool"] = tool_name
        st.session_state["last_answers"] = answers
        st.session_state["last_visual"] = include_visual
        st.success("Prompt generated. Copy and paste it into your selected tool.")

prompt_out = st.session_state.get("last_prompt", "")
if prompt_out:
    st.markdown("### Your Prompt")
    st.caption(f"Paste into: {st.session_state.get('last_tool', tool_name)}")
    st.text_area("Copy from here:", prompt_out, height=380)

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_tool = st.session_state.get("last_tool", tool_name).replace(" ", "_").lower()

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download Prompt (.txt)",
            data=prompt_out.encode("utf-8"),
            file_name=f"prompt_{safe_tool}_{ts}.txt",
            mime="text/plain"
        )
    with col2:
        payload = {
            "tool": st.session_state.get("last_tool", tool_name),
            "strict_mode": bool(strict_mode),
            "include_visual_step": bool(st.session_state.get("last_visual", False)) if tool_name == "Gemini" else False,
            "answers": st.session_state.get("last_answers", answers),
            "generated_at": ts,
            "app": "prompt_builder_v1_1_help_export.py (guided questions restored)"
        }
        st.download_button(
            "Download Inputs (.json)",
            data=json.dumps(payload, indent=2).encode("utf-8"),
            file_name=f"prompt_inputs_{safe_tool}_{ts}.json",
            mime="application/json"
        )

    with st.expander("Example (what good answers look like)"):
        if tool_name == "NotebookLM":
            st.write("- Use case: Create a plan/blueprint from my sources")
            st.write("- Sources: PDF(s)")
            st.write("- Goal: Summarize my notes and produce a step-by-step launch checklist.")
            st.write("- Guidance: One stage at a time (type 'next')")
        elif tool_name == "Gemini":
            st.write("- Task: Create a 2-week LinkedIn content calendar for Prompt Builder.")
            st.write("- Success: Day-by-day topics + short outlines + CTA ideas.")
        else:
            st.write("Tip: Write short, specific goals. If you're unsure, describe what success looks like.")
else:
    st.caption("When ready, click **Generate Prompt** to create the prompt.")
