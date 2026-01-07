# M&A Due Diligence Agent

A multi-agent system built on the Claude Agent SDK for comprehensive M&A transaction due diligence. The agent orchestrates specialized subagents to review uploaded documents, analyze for red flags, assess risks, and generate detailed diligence reports.

## Overview

The Diligence Agent automates the document review process for M&A transactions by:

1. **Analyzing uploaded documents** across financial, legal, and operational categories
2. **Identifying red flags** that could impact the transaction
3. **Assessing risks** with severity ratings and quantified impacts
4. **Generating professional reports** suitable for board/investment committee review

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      LEAD AGENT (Coordinator)                    │
│                    Orchestrates diligence workflow               │
└────────────────┬────────────────┬────────────────┬──────────────┘
                 │                │                │
                 ▼                ▼                ▼
┌────────────────────┐ ┌──────────────────┐ ┌─────────────────────┐
│  FINANCIAL ANALYST │ │   LEGAL ANALYST  │ │  DOCUMENT ANALYZER  │
│  - Revenue quality │ │  - CoC provisions│ │  - Corp governance  │
│  - Profitability   │ │  - Contracts     │ │  - Org structure    │
│  - Balance sheet   │ │  - Litigation    │ │  - Operations       │
│  - Cash flow       │ │  - Compliance    │ │  - Policies         │
└────────┬───────────┘ └────────┬─────────┘ └──────────┬──────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                ▼
                 ┌──────────────────────────┐
                 │      RISK ASSESSOR       │
                 │  - Synthesize findings   │
                 │  - Rate severity         │
                 │  - Quantify impacts      │
                 │  - Deal recommendations  │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │      REPORT WRITER       │
                 │  - Executive summary     │
                 │  - Risk matrix           │
                 │  - Detailed findings     │
                 │  - PDF generation        │
                 └──────────────────────────┘
```

## Subagent Specializations

### Financial Analyst
Reviews financial documents for:
- Revenue quality and sustainability
- Profitability trends and EBITDA adjustments
- Balance sheet risks and hidden liabilities
- Cash flow concerns and working capital
- Customer concentration analysis
- Quality of earnings assessment

### Legal Analyst
Reviews legal documents for:
- Change of control provisions and triggers
- Consent requirements for assignment
- Material contract terms and risks
- Pending litigation exposure
- IP ownership and licensing issues
- Regulatory compliance gaps

### Document Analyzer
Reviews corporate/operational documents for:
- Governance structure and issues
- Organizational dependencies
- Key person risks
- Operational red flags
- Policy and process gaps

### Risk Assessor
Synthesizes all findings to:
- Categorize risks by severity (Critical/High/Medium/Low)
- Rate likelihood of materialization
- Quantify financial impacts
- Identify deal blockers
- Recommend deal term protections
- Create mitigation action plans

### Report Writer
Generates professional PDF reports with:
- Executive summary with risk rating
- Color-coded risk matrix
- Detailed findings by category
- Deal term recommendations
- Open items and next steps

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd diligence-agent

# Install dependencies using uv
uv sync

# Or using pip
pip install -e .

# Set up your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### Starting the Agent

```bash
# Using uv
uv run python diligence_agent/agent.py

# Or directly
python diligence_agent/agent.py
```

### Workflow

1. **Upload Documents**: Place documents to review in `files/uploads/`
   - Financial statements, projections, schedules
   - Contracts and legal agreements
   - Corporate documents (bylaws, minutes, etc.)
   - Organizational materials

2. **Start Diligence Review**: Use the `/diligence` command or describe what you need

3. **Review Results**:
   - Analysis notes: `files/analysis_notes/`
   - Risk assessment: `files/risk_assessment/`
   - Final report: `files/reports/`

### Commands

| Command | Description |
|---------|-------------|
| `/diligence` | Comprehensive due diligence review |
| `/financial` | Financial-focused analysis |
| `/legal` | Legal/contract-focused analysis |
| `/risk` | Risk assessment from existing analysis |
| `/report` | Generate PDF report from analysis |

### Example Session

```
You: /diligence

Agent: Analyzing uploaded documents. Spawning financial analyst for statements,
legal analyst for contracts, and document analyzer for corporate records.

[FINANCIAL-ANALYST-1] → Glob
[FINANCIAL-ANALYST-1] → Read
[LEGAL-ANALYST-1] → Glob
[LEGAL-ANALYST-1] → Read
[DOCUMENT-ANALYZER-1] → Glob
[DOCUMENT-ANALYZER-1] → Read
...

[RISK-ASSESSOR-1] → Glob
[RISK-ASSESSOR-1] → Read
[RISK-ASSESSOR-1] → Write

[REPORT-WRITER-1] → Glob
[REPORT-WRITER-1] → Read
[REPORT-WRITER-1] → Bash

Agent: Diligence review complete. Report saved to
files/reports/diligence_report_20251110.pdf.
2 critical red flags identified: customer concentration and pending litigation.
```

## File Structure

```
diligence-agent/
├── diligence_agent/
│   ├── agent.py              # Main entry point
│   ├── prompts/              # Agent system prompts
│   │   ├── lead_agent.txt
│   │   ├── document_analyzer.txt
│   │   ├── financial_analyst.txt
│   │   ├── legal_analyst.txt
│   │   ├── risk_assessor.txt
│   │   └── report_writer.txt
│   └── utils/                # Utility modules
│       ├── subagent_tracker.py
│       ├── transcript.py
│       └── message_handler.py
├── .claude/
│   ├── commands/             # Slash commands
│   │   ├── diligence.md
│   │   ├── financial.md
│   │   ├── legal.md
│   │   ├── risk.md
│   │   └── report.md
│   └── skills/               # Reusable skills
│       └── pdf/
├── files/                    # Working directories (created at runtime)
│   ├── uploads/              # Input documents
│   ├── analysis_notes/       # Analyst findings
│   ├── risk_assessment/      # Risk synthesis
│   └── reports/              # Final PDF reports
├── logs/                     # Session logs
├── pyproject.toml
├── .env.example
└── README.md
```

## Red Flags Detected

The agent is trained to identify these M&A red flags:

### Financial
- Declining revenue or margins
- Customer concentration (>20% single customer)
- Off-balance sheet liabilities
- Cash flow divergence from earnings
- Aggressive accounting practices
- Debt covenant issues

### Legal
- Change of control terminations
- Unfavorable consent requirements
- Material pending litigation
- IP ownership disputes
- Compliance violations
- Environmental liabilities

### Operational
- Key person dependencies
- Technology obsolescence
- Supplier concentration
- Integration complexity
- Deferred maintenance

## Output Examples

### Risk Matrix (from report)

| Category | Risk | Severity | Likelihood | Exposure |
|----------|------|----------|------------|----------|
| Financial | Customer concentration | Critical | High | $2.5M revenue at risk |
| Legal | CoC consent required | High | High | Deal blocker if not obtained |
| Operational | Key person dependency | Medium | Medium | $500K replacement cost |

### Deal Recommendations

- **Escrow**: $2M holdback for 18 months
- **Rep/Warranty**: Enhanced financial representations
- **Closing Condition**: Key customer consent
- **Indemnity**: Special indemnity for pending litigation

## Configuration

The agent uses these Claude Agent SDK options:

```python
ClaudeAgentOptions(
    permission_mode="bypassPermissions",
    setting_sources=["project"],
    system_prompt=lead_agent_prompt,
    allowed_tools=["Task"],
    agents=agents,  # Subagent definitions
    hooks=hooks,    # Tool tracking hooks
    model="haiku"
)
```

## Logging

Session logs are saved to `logs/session_YYYYMMDD_HHMMSS/`:
- `transcript.txt` - Human-readable conversation log
- `tool_calls.jsonl` - Structured tool usage log

## Dependencies

- `claude-agent-sdk>=0.1.0`
- `python-dotenv>=1.0.0`
- `reportlab>=4.0.0`
- `matplotlib>=3.7.0`

## Limitations

- Does not provide legal or financial advice
- Analysis quality depends on document quality and completeness
- PDF text extraction may be imperfect for scanned documents
- Findings should be reviewed by qualified professionals
