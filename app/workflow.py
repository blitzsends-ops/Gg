from app.schemas import CampaignLaunchRequest, CampaignLaunchResponse
from app.services.meta_ads_service import MetaAdsManagerClient
from app.services.openai_service import OpenAIAdGenerator


class CampaignAutomationWorkflow:
    def __init__(self) -> None:
        self.ai = OpenAIAdGenerator()
        self.meta = MetaAdsManagerClient()

    def launch_campaign(self, request: CampaignLaunchRequest) -> CampaignLaunchResponse:
        variants = self.ai.build_variants(request)

        campaign_id = self.meta.create_campaign(request)
        adset_id = self.meta.create_adset(request, campaign_id)

        ad_ids: list[str] = []
        for idx, variant in enumerate(variants, start=1):
            creative_id = self.meta.create_adcreative(request, variant)
            ad_id = self.meta.create_ad(request, adset_id, creative_id, idx)
            ad_ids.append(ad_id)

        return CampaignLaunchResponse(
            campaign_id=campaign_id,
            adset_id=adset_id,
            ad_ids=ad_ids,
            variants=variants,
        )
