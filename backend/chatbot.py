# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_response(user_input):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",  # or "gpt-4"
#         messages=[
#             {"role": "system", "content": "You're a fashion stylist bot."},
#             {"role": "user", "content": user_input}
#         ],
#         temperature=0.7
#     )
#     return response.choices[0].message.content.strip()


from groq import Groq
from dotenv import load_dotenv
import os

# Load the API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Define the response function
def generate_response(user_input):
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # or use "llama3-8b-8192", etc.
        messages=[
            {"role": "system", "content": "You're a fashion stylist bot."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


