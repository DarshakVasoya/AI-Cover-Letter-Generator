import os, time, sys
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')
print('GEMINI_KEY_PRESENT=', bool(API_KEY))
print('GEMINI_KEY_LENGTH=', len(API_KEY) if API_KEY else None)
if not API_KEY:
    sys.exit(0)
try:
    import google.generativeai as genai
except ImportError:
    print('google-generativeai not installed')
    sys.exit(1)
try:
    genai.configure(api_key=API_KEY)
    model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    start = time.time()
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content('Reply only: OK')
    latency = time.time() - start
    text = getattr(resp, 'text', '').strip() if resp else ''
    print('API_CALL_STATUS=success')
    print('REPLY=', text)
    print(f'LATENCY_SEC={latency:.2f}')
except Exception as e:
    print('API_CALL_STATUS=error')
    print('ERROR_TYPE=', type(e).__name__)
    print('ERROR=', e)
