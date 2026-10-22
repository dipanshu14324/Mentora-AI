from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

import json



class QuizGenerator:


    def __init__(self):

        self.llm = ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0.3
        )



    def generate(self, text, number=5):


        prompt=f"""

You are an expert teacher.

Create {number} multiple choice questions
from the given explanation.

Rules:

- Return ONLY JSON.
- Each question has 4 options.
- Include correct answer.
- Include explanation.

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


Content:

{text}

"""


        response = self.llm.invoke(prompt)



        try:

            return json.loads(
                response.content
            )


        except Exception:

            return []
