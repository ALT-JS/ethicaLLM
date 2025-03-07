from google import genai

genai.configure(api_key="AIzaSyBwzfEUVZzkoUF23FFbcbIDOGcQsrPFMsg")
model = genai.GenerativeModel("gemini-1.5-flash")


def generate(dialogue):
    prompt = "Please summarize the following dialogue"
    prompt += dialogue
    response = model.generate_content(prompt)
    return response.text

generate()