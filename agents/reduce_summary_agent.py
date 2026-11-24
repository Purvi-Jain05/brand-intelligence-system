import json
import re

from prompts.reduce_summary_prompt import (
    REDUCE_SUMMARY_PROMPT
)


class ReduceSummaryAgent:

    def __init__(
        self,
        groq_service
    ):
        self.groq = groq_service

    def reduce(
        self,
        summaries
    ):

        prompt = f"""
{REDUCE_SUMMARY_PROMPT}

SUMMARIES:

{json.dumps(
    summaries,
    indent=2
)}
"""

        response = self.groq.generate(
            prompt
        )

        if not response:

            return {}

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