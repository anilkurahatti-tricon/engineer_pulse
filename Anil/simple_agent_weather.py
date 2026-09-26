# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq


# load_dotenv()

# from langchain.agents import create_agent

# groq_api_key = os.getenv("GROQ_API_KEY")
# os.environ["GROQ_API_KEY"] = groq_api_key

# def get_weather(city:str)-> str:
#     """Get weather for a given city."""
#     return f"It is always sunny in {city}!"

# agent=create_agent(
#     model="openai/gpt-oss-20b",
#     model_provider="groq",
#     tools=[get_weather],
#     system_prompt="You are a helpful weather assistant."    
# )

# result=agent.invoke (
#     {
#         "message":[
#             {
#                 "role":"user",
#                 "content":"What's the weather in San Francisco??"
#             }
#         ]
#     }
# )

# print(result["messages"][-1].content_blocks)