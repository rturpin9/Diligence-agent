---
description: Generate risk assessment from existing analysis
---

Generate a comprehensive risk assessment based on completed analysis in files/analysis_notes/.

## Purpose
Synthesize all analysis findings into a prioritized risk assessment with:
- Risk categorization by severity (Critical/High/Medium/Low)
- Quantified financial impacts
- Deal term recommendations
- Mitigation strategies

## Prerequisites
Analysis notes should already exist in files/analysis_notes/ from previous analysis runs.

## Workflow
1. Spawn risk-assessor to read all analysis from files/analysis_notes/
2. Synthesize findings across financial, legal, and operational streams
3. Generate risk matrix with severity and likelihood ratings
4. Develop deal term recommendations
5. Save to files/risk_assessment/risk_summary.md
6. Optionally spawn report-writer to generate updated PDF report

## Output
- Risk summary in files/risk_assessment/risk_summary.md
- Prioritized risk matrix
- Deal term recommendations
- Updated PDF report (if requested)

Generate the risk assessment now.
