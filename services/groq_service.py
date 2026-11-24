import os
import time

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

        self.model = (
            "llama-3.1-8b-instant"
        )

    def generate(
        self,
        prompt,
        retries=3
    ):

        for attempt in range(retries):

            try:

                response = (
                    self.client.chat.completions.create(
                        model=self.model,

                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],

                        temperature=0.2
                    )
                )

                return (
                    response
                    .choices[0]
                    .message
                    .content
                )

            except Exception as e:

                print(
                    f"Groq Retry {attempt+1}: {e}"
                )

                time.sleep(
                    3
                )

        return None