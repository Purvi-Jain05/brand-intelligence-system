import json
import re

from prompts.fusion_prompt import (
    FUSION_PROMPT
)


class BrandFusionAgent:

    def __init__(
        self,
        groq_service
    ):

        self.groq = groq_service

    def fuse(
        self,
        payload
    ):

        prompt = f"""
{FUSION_PROMPT}

INPUT DATA:

{json.dumps(
    payload,
    indent=2
)}
"""

        response = (
            self.groq.generate(
                prompt
            )
        )

        if not response:

            return {
                "error":
                "Fusion failed"
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