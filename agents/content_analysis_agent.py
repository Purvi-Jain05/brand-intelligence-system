import json
import re

from prompts.content_prompt import (
    CONTENT_PROMPT
)


class ContentAnalysisAgent:

    def __init__(
        self,
        groq_service
    ):

        self.groq = groq_service

    def analyze(
        self,
        page
    ):

        page_data = {

            "url":
            page.get(
                "url",
                ""
            ),

            "title":
            page.get(
                "title",
                ""
            ),

            "headings":
            page.get(
                "headings",
                []
            ),

            "text":
            page.get(
                "text",
                ""
            )[:3000]
        }

        prompt = f"""
{CONTENT_PROMPT}

PAGE DATA:

{json.dumps(
    page_data,
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
                "Content analysis failed"
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