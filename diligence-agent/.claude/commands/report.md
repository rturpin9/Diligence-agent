---
description: Generate PDF diligence report from existing analysis
---

Generate a professional PDF due diligence report from existing analysis and risk assessment.

## Purpose
Create a board/investment committee-ready PDF report synthesizing:
- Executive summary with overall risk rating
- Risk matrix with color-coded severity
- Financial analysis summary
- Legal analysis summary
- Operational analysis summary
- Deal term recommendations
- Open items and next steps

## Prerequisites
- Analysis notes in files/analysis_notes/
- Risk assessment in files/risk_assessment/ (recommended)

## Workflow
1. Spawn report-writer subagent
2. Read all analysis from files/analysis_notes/
3. Read risk assessment from files/risk_assessment/ (if available)
4. Generate professional PDF using reportlab
5. Save to files/reports/

## Output
- PDF report in files/reports/{company}_diligence_report_YYYYMMDD.pdf

Generate the diligence report now.
