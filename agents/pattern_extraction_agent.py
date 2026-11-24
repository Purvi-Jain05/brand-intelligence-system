import json
import re

from prompts.pattern_prompt import (
    PATTERN_PROMPT
)


class PatternExtractionAgent:

    def __init__(
        self,
        groq_service
    ):

        self.groq = groq_service

    def extract_patterns(
        self,
        analysis_data
    ):

        prompt = f"""
{PATTERN_PROMPT}

ANALYSIS DATA:

{json.dumps(
    analysis_data,
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
                "Pattern extraction failed"
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