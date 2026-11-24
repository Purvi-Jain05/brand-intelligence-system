import json
import re
from pathlib import Path

from prompts.memory_prompt import (
    MEMORY_PROMPT
)


class BrandMemoryBuilder:

    def __init__(
        self,
        groq_service
    ):

        self.groq = groq_service

    def build(
        self,
        brand_brain
    ):

        prompt = f"""
{MEMORY_PROMPT}

BRAND BRAIN:

{json.dumps(
    brand_brain,
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
                "Memory generation failed"
            }

        try:

            cleaned = re.sub(
                r"```json|```",
                "",
                response
            ).strip()

            memory = json.loads(
                cleaned
            )

        except Exception:

            return {
                "raw_output":
                response
            }

        Path(
            "memory"
        ).mkdir(
            exist_ok=True
        )

        with open(
            "memory/brand_memory.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                memory,
                f,
                indent=2,
                ensure_ascii=False
            )

        return memory