---
description: Start comprehensive M&A due diligence review of uploaded documents
---

Perform a comprehensive M&A due diligence review of documents in files/uploads/.

## Scope
Conduct full due diligence covering:
1. **Financial Analysis**: Review financial statements, projections, and metrics for red flags
2. **Legal Analysis**: Review contracts and agreements for change of control issues, consent requirements, and risks
3. **Operational Analysis**: Review corporate and organizational documents for governance and operational concerns

## Workflow
1. Spawn financial-analyst, legal-analyst, and document-analyzer subagents IN PARALLEL
2. Each analyst reviews their assigned document categories in files/uploads/
3. Wait for all analysts to complete and save findings to files/analysis_notes/
4. Spawn risk-assessor to synthesize all findings and create risk summary
5. Spawn report-writer to generate comprehensive PDF diligence report

## Output
- Analysis notes saved to files/analysis_notes/
- Risk assessment saved to files/risk_assessment/
- Final PDF report saved to files/reports/

## Instructions
Review all documents in files/uploads/ and generate a comprehensive due diligence report. Focus on identifying red flags, transaction risks, and deal term recommendations.

Begin the diligence review now.
