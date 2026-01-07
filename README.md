# M&A Due Diligence Agent

A multi-agent system built on the [Claude Agent SDK](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-overview) for comprehensive M&A transaction due diligence.

## Overview

The Diligence Agent automates document review for M&A transactions by orchestrating specialized subagents to:

- **Analyze uploaded documents** across financial, legal, and operational categories
- **Identify red flags** that could impact the transaction
- **Assess risks** with severity ratings and quantified impacts
- **Generate professional reports** suitable for board/investment committee review

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      LEAD AGENT (Coordinator)                    │
└────────────────┬────────────────┬────────────────┬──────────────┘
                 │                │                │
                 ▼                ▼                ▼
┌────────────────────┐ ┌──────────────────┐ ┌─────────────────────┐
│  FINANCIAL ANALYST │ │   LEGAL ANALYST  │ │  DOCUMENT ANALYZER  │
│  Revenue, margins  │ │  Contracts, CoC  │ │  Governance, ops    │
└────────┬───────────┘ └────────┬─────────┘ └──────────┬──────────┘
         └──────────────────────┼──────────────────────┘
                                ▼
                 ┌──────────────────────────┐
                 │      RISK ASSESSOR       │
                 │  Synthesize & prioritize │
                 └────────────┬─────────────┘
                              ▼
                 ┌──────────────────────────┐
                 │      REPORT WRITER       │
                 │  Professional PDF output │
                 └──────────────────────────┘
```

## Quick Start

```bash
cd diligence-agent

# Install dependencies
uv sync

# Set up API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run the agent
uv run python diligence_agent/agent.py
```

## Usage

1. **Upload documents** to `files/uploads/`
2. **Start review** with `/diligence` command
3. **Get report** from `files/reports/`

### Available Commands

| Command | Description |
|---------|-------------|
| `/diligence` | Full comprehensive review |
| `/financial` | Financial-focused analysis |
| `/legal` | Legal/contract-focused analysis |
| `/risk` | Risk assessment from existing analysis |
| `/report` | Generate PDF report |

## Red Flags Detected

**Financial**: Customer concentration, declining margins, cash flow issues, off-balance sheet items

**Legal**: Change of control terminations, consent requirements, pending litigation, IP issues

**Operational**: Key person dependencies, integration complexity, compliance gaps

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key ([get one here](https://console.anthropic.com))

## Documentation

See [diligence-agent/README.md](./diligence-agent/README.md) for detailed documentation.

## Resources

- [Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-overview)
- [API Reference](https://docs.anthropic.com/claude)

## License

MIT
