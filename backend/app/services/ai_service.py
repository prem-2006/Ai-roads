import json

from openai import OpenAI

from app.config import get_settings


SYSTEM_PROMPT = (
    "You are a road safety analyst. Analyze the data and answer clearly. "
    "Use concise, practical insights and mention uncertainty when needed."
)


class AIService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key) if self.settings.openai_api_key else None

    def ask(self, question: str, data_summary: dict) -> str:
        if not self.client:
            return (
                "AI key is not configured. Please set OPENAI_API_KEY in backend/.env. "
                f"Question received: {question}"
            )

        response = self.client.chat.completions.create(
            model=self.settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Question: {question}\n\n"
                        f"Road accident data summary (JSON):\n{json.dumps(data_summary)}"
                    ),
                },
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content or "No response generated."
