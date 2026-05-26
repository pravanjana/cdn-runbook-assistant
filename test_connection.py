import anthropic
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Send a test message
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello in one sentence!"}
    ]
)

# Print the response
print(response.content[0].text)
