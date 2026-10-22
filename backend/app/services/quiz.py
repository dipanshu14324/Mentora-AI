import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


class QuizGenerator:


    def __init__(self):

        self.llm = ChatGroq(
            model="qwen/qwen3.8-27b",
            temperature=0.3,
            streaming=False,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )



    def generate(self,text):


        prompt=f"""

You are an AI teacher.

Create MCQ quiz from this explanation.


Rules:

- Create 5 questions.
- Each question has 4 options.
- Give correct answer.
- Give explanation.


Return ONLY JSON.


Format:


[
{{
"question":"",
"options":[
"",
"",
"",
""
],
"answer":"",
"explanation":""
}}
]


Explanation:

{text}

"""


        response=self.llm.invoke(prompt)


        try:

            return json.loads(
                response.content
            )


        except Exception as e:

            print("Quiz JSON Error:",e)
            print(response.content)

            return []