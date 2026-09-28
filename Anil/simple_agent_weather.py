import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional

import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

dotenv.load_dotenv()
# Load environment variables from .env file
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# System prompt for the weather assistant
SYSTEM_PROMPT = """You are a helpful weather assistant.
You provide weather information for a given city in a concise and accurate manner.
Respond with ONLY valid JSON matching EXACTLY this structure:

Rules:
- Base your response only on the city provided.
- Ensure all fields in the JSON structure are filled accurately.
- Show the temperature in degree fahrenheit (°F) unit, example 75 °F
- show exact symbo no ascii code in result
- Do not include any additional commentary or text outside the JSON.

{{
  "city": "Name of the city",
  "weather": "sunny|rainy|cloudy|stormy|snowy",
  "temperature": "show in float number in celsius with no ascii code",
  "humidity": "show in %",
  "temperature_min": "show in float number in celsius with no ascii code",
  "temperature_max": "show in float number in celsius with no ascii code"
}}"""

# Initialize the weather language model with the specified configuration
weather_llm=ChatGroq(
    model=GROQ_MODEL,
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    verbose=True,
    max_tokens=500,
)

user_prompt = ChatPromptTemplate.from_messages([
    ("system",  SYSTEM_PROMPT),
    ("user",  "{input}"),
])

user_query = """Provide the weather details for the city Bangalore"""

weather_chain= user_prompt | weather_llm | JsonOutputParser()

weather_response = weather_chain.invoke({"input": user_query})

print(json.dumps(weather_response, indent=2))




