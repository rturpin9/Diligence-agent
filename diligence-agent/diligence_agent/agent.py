"""Entry point for M&A diligence agent using AgentDefinition for subagents."""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition, HookMatcher

from diligence_agent.utils.subagent_tracker import SubagentTracker
from diligence_agent.utils.transcript import setup_session, TranscriptWriter
from diligence_agent.utils.message_handler import process_assistant_message

# Load environment variables
load_dotenv()

# Paths to prompt files
PROMPTS_DIR = Path(__file__).parent / "prompts"

# Working directories for diligence workflow
WORKING_DIRS = [
    "files/uploads",          # Where users upload documents for review
    "files/analysis_notes",   # Where analysts save their findings
    "files/risk_assessment",  # Where risk assessor saves synthesis
    "files/reports",          # Where final reports are saved
]


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = PROMPTS_DIR / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def setup_working_directories():
    """Create working directories for the diligence workflow."""
    for dir_path in WORKING_DIRS:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


async def chat():
    """Start interactive chat with the diligence agent."""

    # Check API key first, before creating any files
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nError: ANTHROPIC_API_KEY not found.")
        print("Set it in a .env file or export it in your shell.")
        print("Get your key at: https://console.anthropic.com/settings/keys\n")
        return

    # Setup working directories
    setup_working_directories()

    # Setup session directory and transcript
    transcript_file, session_dir = setup_session()

    # Create transcript writer
    transcript = TranscriptWriter(transcript_file)

    # Load prompts
    lead_agent_prompt = load_prompt("lead_agent.txt")
    document_analyzer_prompt = load_prompt("document_analyzer.txt")
    financial_analyst_prompt = load_prompt("financial_analyst.txt")
    legal_analyst_prompt = load_prompt("legal_analyst.txt")
    risk_assessor_prompt = load_prompt("risk_assessor.txt")
    report_writer_prompt = load_prompt("report_writer.txt")

    # Initialize subagent tracker with transcript writer and session directory
    tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)

    # Define specialized subagents for M&A due diligence
    agents = {
        "document-analyzer": AgentDefinition(
            description=(
                "Use this agent to analyze corporate documents, organizational records, "
                "and operational materials. Reviews documents in files/uploads/ for governance "
                "issues, organizational concerns, and operational red flags. Writes analysis "
                "to files/analysis_notes/. Ideal for bylaws, board minutes, org charts, "
                "policies, and general business documents."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=document_analyzer_prompt,
            model="haiku"
        ),
        "financial-analyst": AgentDefinition(
            description=(
                "Use this agent to analyze financial documents for M&A due diligence. "
                "Reviews financial statements, projections, and supporting schedules in files/uploads/. "
                "Identifies financial red flags including revenue quality issues, profitability concerns, "
                "balance sheet risks, and cash flow problems. Calculates key ratios and trends. "
                "Writes analysis to files/analysis_notes/financial_analysis.md."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=financial_analyst_prompt,
            model="haiku"
        ),
        "legal-analyst": AgentDefinition(
            description=(
                "Use this agent to analyze legal documents and contracts for M&A due diligence. "
                "Reviews contracts, agreements, and legal documents in files/uploads/. "
                "Identifies change of control provisions, consent requirements, termination rights, "
                "litigation risks, and compliance issues. Writes analysis to "
                "files/analysis_notes/legal_analysis.md."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=legal_analyst_prompt,
            model="haiku"
        ),
        "risk-assessor": AgentDefinition(
            description=(
                "Use this agent AFTER all analyzers have completed their work to synthesize "
                "findings into a comprehensive risk assessment. Reads all analysis from "
                "files/analysis_notes/, categorizes risks by severity and likelihood, "
                "quantifies impacts, and provides deal recommendations. Writes assessment to "
                "files/risk_assessment/risk_summary.md. Use before report-writer."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=risk_assessor_prompt,
            model="opus"  # Opus for complex risk synthesis and judgment
        ),
        "report-writer": AgentDefinition(
            description=(
                "Use this agent to create the final due diligence report. Reads analysis from "
                "files/analysis_notes/ and risk assessment from files/risk_assessment/, then "
                "synthesizes into a professional PDF report with executive summary, risk matrix, "
                "findings by category, and recommendations. Saves to files/reports/ using reportlab. "
                "Does NOT conduct analysis - only reads existing findings and creates reports."
            ),
            tools=["Skill", "Write", "Glob", "Read", "Bash"],
            prompt=report_writer_prompt,
            model="sonnet"  # Sonnet for professional report writing
        )
    }

    # Set up hooks for tracking
    hooks = {
        'PreToolUse': [
            HookMatcher(
                matcher=None,  # Match all tools
                hooks=[tracker.pre_tool_use_hook]
            )
        ],
        'PostToolUse': [
            HookMatcher(
                matcher=None,  # Match all tools
                hooks=[tracker.post_tool_use_hook]
            )
        ]
    }

    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],  # Load skills from project .claude directory
        system_prompt=lead_agent_prompt,
        allowed_tools=["Task"],
        agents=agents,
        hooks=hooks,
        model="haiku"
    )

    print("\n" + "=" * 60)
    print("  M&A Due Diligence Agent")
    print("=" * 60)
    print("\nAnalyze documents for M&A transactions and generate")
    print("comprehensive due diligence reports with risk assessment.")
    print("\nModels: Haiku (analysts) → Opus (risk) → Sonnet (report)")
    print("\nWorkflow:")
    print("  1. Upload documents to files/uploads/")
    print("  2. Request diligence review")
    print("  3. Receive PDF report in files/reports/")
    print("\nCommands:")
    print("  /diligence  - Start comprehensive due diligence review")
    print("  /financial  - Financial-focused analysis")
    print("  /legal      - Legal/contract-focused analysis")
    print("  /risk       - Risk assessment of current findings")
    print("\nType 'exit' to quit.\n")

    try:
        async with ClaudeSDKClient(options=options) as client:
            while True:
                # Get input
                try:
                    user_input = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    break

                if not user_input or user_input.lower() in ["exit", "quit", "q"]:
                    break

                # Write user input to transcript (file only, not console)
                transcript.write_to_file(f"\nYou: {user_input}\n")

                # Send to agent
                await client.query(prompt=user_input)

                transcript.write("\nAgent: ", end="")

                # Stream and process response
                async for msg in client.receive_response():
                    if type(msg).__name__ == 'AssistantMessage':
                        process_assistant_message(msg, tracker, transcript)

                transcript.write("\n")
    finally:
        transcript.write("\n\nGoodbye!\n")
        transcript.close()
        tracker.close()
        print(f"\nSession logs saved to: {session_dir}")
        print(f"  - Transcript: {transcript_file}")
        print(f"  - Tool calls: {session_dir / 'tool_calls.jsonl'}")


if __name__ == "__main__":
    asyncio.run(chat())
