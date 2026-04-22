import requests

from app.config import settings
from app.schemas import CampaignLaunchRequest, GeneratedAdVariant


class MetaAdsError(RuntimeError):
    pass


class MetaAdsManagerClient:
    def __init__(self) -> None:
        self.base_url = f"https://graph.facebook.com/{settings.meta_graph_version}"
        self.account_id = settings.meta_ad_account_id
        self.page_id = settings.meta_page_id
        self.access_token = settings.meta_access_token

    def _post(self, path: str, data: dict) -> dict:
        payload = {**data, "access_token": self.access_token}
        response = requests.post(f"{self.base_url}/{path}", data=payload, timeout=60)
        if response.status_code >= 400:
            raise MetaAdsError(f"Meta API error {response.status_code}: {response.text}")
        return response.json()

    def create_campaign(self, request: CampaignLaunchRequest) -> str:
        response = self._post(
            path=f"{self.account_id}/campaigns",
            data={
                "name": request.campaign_name,
                "objective": request.objective,
                "status": "PAUSED",
                "special_ad_categories": "[]",
            },
        )
        return response["id"]

    def create_adset(self, request: CampaignLaunchRequest, campaign_id: str) -> str:
        targeting = {
            "geo_locations": {"countries": request.geo_locations},
            "age_min": request.age_min,
            "age_max": request.age_max,
        }
        response = self._post(
            path=f"{self.account_id}/adsets",
            data={
                "name": f"{request.campaign_name} Ad Set",
                "campaign_id": campaign_id,
                "daily_budget": request.daily_budget,
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "LINK_CLICKS",
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "targeting": str(targeting).replace("'", '"'),
                "status": "PAUSED",
            },
        )
        return response["id"]

    def create_adcreative(self, request: CampaignLaunchRequest, variant: GeneratedAdVariant) -> str:
        object_story_spec = {
            "page_id": self.page_id,
            "link_data": {
                "message": variant.primary_text,
                "link": str(request.landing_page_url),
                "name": variant.headline,
                "call_to_action": {
                    "type": request.call_to_action,
                    "value": {"link": str(request.landing_page_url)},
                },
                "image_hash": "",
                "picture": variant.image_url,
            },
        }

        response = self._post(
            path=f"{self.account_id}/adcreatives",
            data={
                "name": f"{request.campaign_name} Creative - {variant.headline[:20]}",
                "object_story_spec": str(object_story_spec).replace("'", '"'),
            },
        )
        return response["id"]

    def create_ad(self, request: CampaignLaunchRequest, adset_id: str, creative_id: str, index: int) -> str:
        response = self._post(
            path=f"{self.account_id}/ads",
            data={
                "name": f"{request.campaign_name} Ad #{index}",
                "adset_id": adset_id,
                "creative": f'{{"creative_id":"{creative_id}"}}',
                "status": "PAUSED",
            },
        )
        return response["id"]
