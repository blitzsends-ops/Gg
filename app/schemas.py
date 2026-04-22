from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class CampaignLaunchRequest(BaseModel):
    campaign_name: str = Field(min_length=3, max_length=120)
    objective: str = "OUTCOME_TRAFFIC"
    daily_budget: int = Field(gt=0, description="Smallest currency unit (e.g., cents)")

    geo_locations: list[str] = Field(default_factory=lambda: ["US"])
    age_min: int = Field(default=18, ge=13, le=65)
    age_max: int = Field(default=45, ge=13, le=65)
    interests: list[str] = Field(default_factory=list)

    product_description: str = Field(min_length=20)
    landing_page_url: HttpUrl
    call_to_action: Literal["LEARN_MORE", "SHOP_NOW", "SIGN_UP", "CONTACT_US"] = "LEARN_MORE"
    variants: int = Field(default=3, ge=1, le=5)


class GeneratedAdVariant(BaseModel):
    headline: str
    primary_text: str
    image_url: str


class CampaignLaunchResponse(BaseModel):
    campaign_id: str
    adset_id: str
    ad_ids: list[str]
    variants: list[GeneratedAdVariant]
