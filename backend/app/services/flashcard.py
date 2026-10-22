import os
from dotenv import load_dotenv
from app.config import GROQ_API_KEY


from langchain_groq import ChatGroq
import json

load_dotenv()

class FlashcardGenerator:


    def __init__(self):

        self.llm = ChatGroq(
            model="qwen/qwen3.8-27b",
            groq_api_key=GROQ_API_KEY,
            temperature=0.3
        )



    def generate(self, answer):


        prompt = f"""

You are an educational flashcard generator.

Convert the following explanation into flashcards.

Rules:

- Create 5 flashcards.
- Each flashcard must have:
  question
  answer

- Keep questions short.
- Keep answers easy to revise.
- Return ONLY JSON.

Format:

[
 {{
 "question":"",
 "answer":""
 }}
]


Explanation:

{answer}

"""


        response = self.llm.invoke(prompt)


        print("===================")
        print("RAW RESPONSE")
        print(response.content)
        print("===================")


        try:

            cards = json.loads(
                response.content
            )


            fixed_cards = []


            for card in cards:

                fixed_cards.append({

                    "question":
                    card.get(
                        "question",
                        ""
                    ),

                    "answer":
                    card.get(
                        "answer",
                        card.get(
                            "Answer",
                            card.get(
                                "content",
                                ""
                            )
                        )
                    )

                })


            return fixed_cards



        except Exception as e:

            print(
                "FLASHCARD JSON ERROR:",
                e
            )


            print(
                response.content
            )


            return []