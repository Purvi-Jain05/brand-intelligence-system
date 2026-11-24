import json
import re

from prompts.audience_prompt import (
    AUDIENCE_PROMPT
)


class AudienceDNAAgent:

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
{AUDIENCE_PROMPT}

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
                "Audience DNA extraction failed"
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