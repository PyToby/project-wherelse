import google.genai as genai
import os

def generate_response(a, b):
    #client = genai.Client(api_key=os.getenv("API_KEY"))
    client = genai.Client(api_key='AIzaSyCIRWDmpm5Jxy5_ZX3IL5u9UOHKJr753T8')
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f'Compare these two services: {a} and {b}. Summarize their differences into ONE sentence only. Return only json formated text in this format: {{ "comparison": "data"}}' 
    )
    return response.text