import google.genai as genai
import os


api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content('What is the capital of India')
print(response.text)