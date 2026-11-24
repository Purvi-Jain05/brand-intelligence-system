import os
import json
import time

from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv(
                "GEMINI_API_KEY"
            )
        )

        self.model = (
            "gemini-2.5-flash"
        )

    # -------------------------
    # Generic Retry Wrapper
    # -------------------------

    def _execute(
        self,
        contents,
        max_retries=3
    ):

        for attempt in range(
            max_retries
        ):

            try:

                response = (
                    self.client.models.generate_content(
                        model=self.model,
                        contents=contents
                    )
                )

                return response.text

            except Exception as e:

                print(
                    f"\nGemini Retry {attempt+1}: {e}"
                )

                time.sleep(
                    5 * (attempt + 1)
                )

        return None

    # -------------------------
    # Text Analysis
    # -------------------------

    def analyze_text(
        self,
        prompt
    ):

        return self._execute(
            prompt
        )

    # -------------------------
    # Image Analysis
    # -------------------------

    def analyze_image(
        self,
        image_path,
        prompt
    ):

        try:

            image = Image.open(
                image_path
            )

            return self._execute(
                [
                    prompt,
                    image
                ]
            )

        except Exception as e:

            print(
                f"\nGemini Image Error: {e}"
            )

            return None

    # -------------------------
    # JSON Helper
    # -------------------------

    def analyze_json(
        self,
        prompt
    ):

        response = (
            self.analyze_text(
                prompt
            )
        )

        if not response:

            return None

        try:

            cleaned = (
                response
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

            return json.loads(
                cleaned
            )

        except Exception:

            return {
                "raw_output":
                response
            }