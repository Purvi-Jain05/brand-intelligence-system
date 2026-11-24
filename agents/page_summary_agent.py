import json
import re

from prompts.page_summary_prompt import (
    PAGE_SUMMARY_PROMPT
)


class PageSummaryAgent:

    def __init__(
        self,
        groq_service
    ):
        self.groq = groq_service

    def summarize(
        self,
        page_data
    ):

        prompt = f"""
{PAGE_SUMMARY_PROMPT}

PAGE DATA:

{json.dumps(page_data, indent=2)}
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