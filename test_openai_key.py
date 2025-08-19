import os
from dotenv import load_dotenv
import json
import sys
import time

try:
    import openai
except ImportError:
    print("openai package not installed")
    sys.exit(1)

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print("OPENAI_KEY_PRESENT=", bool(key))
print("OPENAI_KEY_LENGTH=", len(key) if key else None)
if not key:
    sys.exit(0)
openai.api_key = key

# Legacy OpenAI test script removed after migration to Gemini-only implementation.
