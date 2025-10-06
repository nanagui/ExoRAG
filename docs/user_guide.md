# User Guide – Astronomers & Citizen Scientists

## Overview
This interface enables reviewers to validate potential exoplanet transits quickly by combining AI predictions, light-curve visualizations, and scientific context retrieval.

## Roles
- **Astronomer**: Full access to predictions, upload, ingest datasets, approve candidates.
- **Analyst**: Read-only access to candidate lists, evidence, and plots.
- **Citizen Scientist (future)**: Guided upload flow with simplified messaging.

## Dashboard Workflow
1. **Sign In** – obtain a JWT token (temporary manual issuance). Store it via browser console `localStorage.setItem('EXOAI_TOKEN', 'Bearer <token>')`.
2. **Review Candidate List** – sidebar shows latest processed targets with mission and ingestion timestamp; click to select.
3. **Inspect Light Curve** – line chart displays normalized flux vs time. Hover to inspect flux values.
4. **Evidence Panel** – highlights AI-generated justification with citations. Each bullet references the originating document (NASA paper, mission report).
5. **Decision Hooks** – planned actions (Approve / Flag / Reject) to be implemented once citizen workflow is available.

## Uploading New Curves
(Available via `/api/predictions/predict`) – Use the “Analyze Light Curve” action (coming soon in UI) or issue `curl`:
```bash
curl -H "Authorization: Bearer <token>" \
     -F "file=@path/to/lightcurve.fits" \
     http://localhost:8000/api/predictions/predict
```
The response includes prediction, probability, attention weights, preprocessing statistics, and evidence summary.

## Ingestion Jobs
- Use the “Queue Ingestion” form (coming soon) or API `POST /api/predictions/ingest` with target/mission to fetch bulk light curves.
- Ingestion runs asynchronously; check candidate list for updates.

## Interpreting Outputs
- **Probability**: model confidence after softmax.
- **Attention**: relative importance of each time step; attention heatmap overlay will surface soon.
- **Evidence**: natural language summary plus citations; confirm that relevant mission documents are referenced.
- **Preprocessing Stats**: mean ≈ 0, std ≈ 1 confirms normalization; flux range >1 may indicate anomalies.

## Feedback Loop
Use the “Flag for Review” action (coming soon) or record feedback via shared spreadsheet referencing candidate `path`. Flags feed future retraining loops.
