import json
import re

from prompts.visual_prompt import (
    VISUAL_PROMPT
)


class VisualAnalysisAgent:

    def __init__(
        self,
        gemini_service
    ):

        self.gemini = gemini_service

    def analyze(
        self,
        image_path
    ):

        response = (
            self.gemini.analyze_image(
                image_path,
                VISUAL_PROMPT
            )
        )

        if not response:

            return {
                "error":
                "Visual analysis failed"
            }

        try:

            cleaned = re.sub(
                r"```json|```",
                "",
                response
            ).strip()

            return json.loads(
                cleaned
            )

        except Exception:

            return {
                "raw_output":
                response
            }