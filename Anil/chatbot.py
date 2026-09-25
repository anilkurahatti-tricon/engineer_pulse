from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

print("chatbot (groq streaming): type 'quit','exit', 'bye' to exit")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Exiting chatbot...")
        break
    
    print("chatbot: ", end="",flush=True)
    
    stream=client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role":"system","content":"You are a helpful chatbot."},
            {"role":"user","content":user_input}
                ],
        max_tokens=1000,
        stream=True
    )
        
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print() 