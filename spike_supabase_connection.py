import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

try:
    supabase = create_client(url, key)
    # Query the 'items' table we just created
    response = supabase.table("items").select("*").execute()
    print(f"✅ Connection successful! Data from items table: {response.data}")
except Exception as e:
    print(f"❌ Connection failed: {e}")