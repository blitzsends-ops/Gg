from fastapi import FastAPI, HTTPException

from app.schemas import CampaignLaunchRequest, CampaignLaunchResponse
from app.services.meta_ads_service import MetaAdsError
from app.workflow import CampaignAutomationWorkflow

app = FastAPI(title="Advertising Automation API", version="0.1.0")
workflow = CampaignAutomationWorkflow()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/campaigns/launch", response_model=CampaignLaunchResponse)
def launch_campaign(payload: CampaignLaunchRequest) -> CampaignLaunchResponse:
    try:
        return workflow.launch_campaign(payload)
    except MetaAdsError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Unhandled error: {error}") from error
