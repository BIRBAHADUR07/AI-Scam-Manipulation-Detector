import google.generativeai as genai

try:
    genai.configure(api_key="AIzaSyD1YsAawa4vxrdq9OD7skuS55TuTnPVcUg")
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("hello")
    print("API is active, generated:", response.text)
except Exception as e:
    print(f"API failed: {e}")
