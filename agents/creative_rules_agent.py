import json
import re

from prompts.creative_rules_prompt import (
    CREATIVE_RULES_PROMPT
)


class CreativeRulesAgent:

    def __init__(
        self,
        groq_service
    ):

        self.groq = groq_service

    def extract(
        self,
        patterns
    ):

        prompt = f"""
{CREATIVE_RULES_PROMPT}

PATTERNS:

{json.dumps(
    patterns,
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
                "Creative Rules extraction failed"
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