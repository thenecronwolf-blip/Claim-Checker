# Claim Assessment API

Flask backend deployed on Railway.

## Endpoints
- GET /
- GET /health
# Claim Checker

Flask + Hugging Face project for text analysis.

## Setup

1. Add HF_API_KEY as a Railway Environment Variable.
2. Deploy on Railway with start command: gunicorn backend.main:app –bind 0.0.0.0:$PORT
3. Access `/` for the frontend, `/analyze` to POST text for analysis.
