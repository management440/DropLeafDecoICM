import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    raise EnvironmentError("TAVILY_API_KEY not found in .env file.")

tavily = TavilyClient(api_key=api_key)

if __name__ == "__main__":
    print("Performing test search...")
    try:
        response = tavily.search("Keith Murray controlled bubble vase features")
        if response and 'results' in response:
            print("SUCCESS: Authentication and retrieval operational.")
            first_result = response['results'][0]
            print(f"Snippet: {first_result['title']} - {first_result['url']}")
        else:
            print("WARNING: Received response, but format was unexpected.")
    except Exception as e:
        print(f"ERROR: Connection failed: {e}")