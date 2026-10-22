from langchain_groq import ChatGroq

class QuestionRewriter:

    def __init__(self):

        self.llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.3,
            streaming=True
        )
        


    def rewrite(self, history, question):

        if len(history.messages) == 0:
            return question

        history_text = ""

        for msg in history.messages[-6:]:

            history_text += f"{msg.type}: {msg.content}\n"

        prompt = f"""
You rewrite follow-up questions.

Conversation:

{history_text}

Current Question:
{question}

Rewrite the current question so it is fully self-contained.

Return ONLY the rewritten question.
"""

        response = self.llm.invoke(prompt)

        return response.content.strip()