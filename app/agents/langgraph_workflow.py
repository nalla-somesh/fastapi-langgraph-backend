from typing import AsyncGenerator
from app.agents.gemini_agent import gemini_agent

class ChatWorkflow:
    async def process_message_stream(self, user_input: str, temperature: float = 0.7, max_tokens: int = 1000) -> AsyncGenerator[str, None]:
        async for chunk in gemini_agent.generate_stream(user_input, temperature, max_tokens):
            yield chunk

chat_workflow = ChatWorkflow()
