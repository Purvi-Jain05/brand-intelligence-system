import json
import re

from prompts.product_prompt import (
    PRODUCT_DNA_PROMPT
)


class ProductDNAAgent:

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
{PRODUCT_DNA_PROMPT}

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
                "Product DNA extraction failed"
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