import os

DEFAULT_SYSTEM_PROMPT = "You are an advanced AI agent. Your goal is to assist user with his questions."
DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com/openai/deployments/{model}/chat/completions"
API_KEY = os.getenv('DIAL_API_KEY', '')

# NASA
NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_API_KEY')
NASA_API = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

# Tool names
SIMPLE_CALCULATOR = "simple_calculator"
NASA_IMG_STEALER = "nasa_image_stealer"
HAIKU_GENERATOR = "haiku_generation_tool"
WEB_SEARCH = "web_search_tool"