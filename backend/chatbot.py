from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[
            {"role": "system", "content": "You're a fashion stylist bot."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
