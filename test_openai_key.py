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

# Use a minimal prompt
try:
    start = time.time()
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Reply with ONLY: OK"}],
        max_tokens=3,
        temperature=0,
    )
    dur = time.time() - start
    content = resp.choices[0].message["content"].strip()
    print("API_CALL_STATUS=success")
    print("REPLY=", content)
    print(f"LATENCY_SEC={dur:.2f}")
except Exception as e:
    print("API_CALL_STATUS=error")
    print("ERROR_TYPE=", type(e).__name__)
    print("ERROR=", e)
