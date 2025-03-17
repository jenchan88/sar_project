import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")  

response = model.generate_content("How can I assist in Search and Rescue operations?")

print(response.text)
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents="Explain how AI works",
# )

# print(response.text)