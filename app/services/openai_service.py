from openai import OpenAI

from app.config import settings
from app.schemas import CampaignLaunchRequest, GeneratedAdVariant


class OpenAIAdGenerator:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_copy_variants(self, request: CampaignLaunchRequest) -> list[dict[str, str]]:
        prompt = (
            "You are a senior performance marketer. Generate ad copy variants for Meta Ads. "
            "Return STRICT JSON array with objects containing: headline, primary_text, image_prompt. "
            f"Number of variants: {request.variants}. "
            f"Product: {request.product_description}. "
            f"Audience interests: {', '.join(request.interests) if request.interests else 'broad audience'}. "
            f"CTA: {request.call_to_action}."
        )

        response = self.client.responses.create(
            model=settings.openai_chat_model,
            input=prompt,
            temperature=0.8,
        )

        text_payload = response.output_text.strip()
        import json

        variants = json.loads(text_payload)
        return variants

    def generate_image(self, image_prompt: str) -> str:
        result = self.client.images.generate(
            model=settings.openai_image_model,
            prompt=image_prompt,
            size="1024x1024",
        )
        return result.data[0].url

    def build_variants(self, request: CampaignLaunchRequest) -> list[GeneratedAdVariant]:
        copy_variants = self.generate_copy_variants(request)
        generated: list[GeneratedAdVariant] = []
        for variant in copy_variants:
            image_url = self.generate_image(variant["image_prompt"])
            generated.append(
                GeneratedAdVariant(
                    headline=variant["headline"],
                    primary_text=variant["primary_text"],
                    image_url=image_url,
                )
            )
        return generated
