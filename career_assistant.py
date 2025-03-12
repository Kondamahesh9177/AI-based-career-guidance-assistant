
import google.generativeai as genai


genai.configure(api_key="AIzaSyDYS6wl92ccNLg3glkuDHS4TC7vi8iwRk4")


def is_career_related(query):
    """Classifies if a given query is career-related using Gemini API."""
    model = genai.GenerativeModel("gemini-2.0-flash") 

    prompt = f"Is the following query related to career guidance? Respond with 'yes' or 'no' only. Query: {query}"
    
    response = model.generate_content(prompt)
    result = response.text.lower().strip()

    return result == "yes"


def generate_career_response(query):
    """Generates a career guidance response using Gemini API."""
    model = genai.GenerativeModel("gemini-2.0-flash")  

    prompt = f"Provide career guidance for the following query: {query}"
    
    response = model.generate_content(prompt)
    
    return response.text  


def handle_query(query):
    if is_career_related(query):
        return generate_career_response(query)
    else:
        return "Sorry, I can only provide career guidance. Please ask a career-related question."
