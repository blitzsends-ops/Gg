from app.schemas import CampaignLaunchRequest


def test_campaign_launch_request_defaults() -> None:
    payload = CampaignLaunchRequest(
        campaign_name="Demo Campaign",
        daily_budget=1000,
        product_description="An AI platform helping marketers build and optimize ad funnels quickly.",
        landing_page_url="https://example.com",
    )

    assert payload.variants == 3
    assert payload.geo_locations == ["US"]
    assert payload.call_to_action == "LEARN_MORE"
