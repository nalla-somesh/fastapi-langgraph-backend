import google.generativeai as genai
from typing import AsyncGenerator
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("gemini")

class GeminiAgent:
    def __init__(self):
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    async def generate_stream(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> AsyncGenerator[str, None]:
        try:
            logger.info("Generating response", prompt_length=len(prompt), temperature=temperature, max_tokens=max_tokens)
            
            config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            
            response = self.model.generate_content(prompt, generation_config=config, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error("Error generating response", error=str(e))
            yield f"Error: {str(e)}"

gemini_agent = GeminiAgent()
