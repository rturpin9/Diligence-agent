---
description: Financial-focused due diligence analysis
---

Perform a financial-focused due diligence review of documents in files/uploads/.

## Focus Areas
1. **Revenue Quality**: Recognition practices, customer concentration, recurring vs. one-time
2. **Profitability**: Margin trends, EBITDA adjustments, unusual items
3. **Balance Sheet**: Working capital, debt levels, off-balance sheet items
4. **Cash Flow**: Operating cash vs. net income, cash conversion, sustainability
5. **Projections**: Assumption reasonableness, key risks to forecasts

## Red Flags to Identify
- Declining revenue or margins
- Customer concentration (>20% single customer)
- Aggressive accounting practices
- Cash flow divergence from earnings
- Undisclosed liabilities
- Covenant violations or near-misses

## Workflow
1. Spawn financial-analyst to review all financial documents in files/uploads/
2. Wait for analysis to complete in files/analysis_notes/
3. Spawn risk-assessor to evaluate financial risks
4. Spawn report-writer to create financial diligence report

## Output
- Financial analysis in files/analysis_notes/financial_analysis.md
- Risk assessment in files/risk_assessment/
- PDF report in files/reports/

Perform the financial diligence review now.
