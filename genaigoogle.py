from google import genai
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("MY_GOOGLE_GENAI_KEY"))

def clientresponse(order):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{order} in 50 words",
    )
    return response.text

if __name__=="__main__":
    pass