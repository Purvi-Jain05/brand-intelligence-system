import json
import re

from prompts.product_analysis_prompt import (
    PRODUCT_ANALYSIS_PROMPT
)


class ProductAnalysisAgent:

    def __init__(
        self,
        groq_service
    ):

        self.groq = groq_service

    def analyze(
        self,
        product_page
    ):

        payload = {

            "url":
            product_page.get(
                "url",
                ""
            ),

            "title":
            product_page.get(
                "title",
                ""
            ),

            "headings":
            product_page.get(
                "headings",
                []
            ),

            "text":
            product_page.get(
                "text",
                ""
            )[:6000]
        }

        prompt = f"""
{PRODUCT_ANALYSIS_PROMPT}

PRODUCT PAGE DATA:

{json.dumps(
    payload,
    indent=2,
    ensure_ascii=False
)}
"""

        response = self.groq.generate(
            prompt
        )

        if not response:

            return {
                "error":
                "Empty response from model"
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

                "error":
                "JSON parsing failed",

                "raw_output":
                response
            }