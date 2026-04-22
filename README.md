# Advertising Automation System (ChatGPT + DALL·E + Meta Ads Manager)

This project provides a production-oriented starter backend that:

1. Uses **ChatGPT** to generate ad copy variants.
2. Uses **DALL·E** (OpenAI Images API) to generate ad creatives.
3. Pushes the campaign assets to **Meta Ads Manager** through the Meta Marketing API.

## Architecture

- `POST /v1/campaigns/launch`
  - Validates campaign input.
  - Generates copy variants with ChatGPT.
  - Generates one or more image concepts with DALL·E.
  - Creates campaign, ad set, creative, and ads in Meta.
  - Returns object IDs and generated content for auditability.

## Project Layout

- `app/main.py` – FastAPI app and route registration.
- `app/schemas.py` – Input/output data contracts.
- `app/config.py` – Environment-driven settings.
- `app/workflow.py` – End-to-end orchestration logic.
- `app/services/openai_service.py` – ChatGPT + DALL·E integration.
- `app/services/meta_ads_service.py` – Meta Marketing API integration.

## Setup

### 1) Environment variables

Create `.env` in project root:

```bash
OPENAI_API_KEY=...
OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_IMAGE_MODEL=gpt-image-1
META_ACCESS_TOKEN=...
META_AD_ACCOUNT_ID=act_1234567890
META_PAGE_ID=1234567890
META_GRAPH_VERSION=v22.0
```

### 2) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3) Run

```bash
uvicorn app.main:app --reload --port 8000
```

## Example request

```bash
curl -X POST http://localhost:8000/v1/campaigns/launch \
  -H 'Content-Type: application/json' \
  -d '{
    "campaign_name": "Spring Launch 2026",
    "objective": "OUTCOME_TRAFFIC",
    "daily_budget": 5000,
    "geo_locations": ["US"],
    "age_min": 24,
    "age_max": 45,
    "interests": ["software as a service", "marketing automation"],
    "product_description": "AI assistant for building sales funnels",
    "landing_page_url": "https://example.com",
    "call_to_action": "LEARN_MORE",
    "variants": 3
  }'
```

## Important implementation notes

- This implementation stores image URLs returned by OpenAI. In production, move assets to your own durable storage bucket for long-term reliability.
- Meta Marketing API can require additional fields depending on account setup, compliance, region, and objective.
- Add retry logic and idempotency keys before production rollout.
