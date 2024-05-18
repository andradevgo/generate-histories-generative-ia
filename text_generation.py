import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyCCtqRAO6yH-tQKHi0bi5rXQCsYrhwRuHs"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_story(resultado_1,resultado_2):
    prompt = f"Escribe un cuento muy corto y muy creativo sobre {resultado_1} y {resultado_2}"
    response = model.generate_content(prompt)
    return response.text