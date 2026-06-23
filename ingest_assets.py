import datetime

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/process_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

asset_dir = os.path.join("01_ingest", "assets")

def ingest_assets():
    for filename in os.listdir(asset_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            sku = os.path.splitext(filename)[0] # Extract SKU from filename
            file_path = os.path.join(asset_dir, filename)
            
            with open(file_path, 'rb') as f:
                # Upload to 'assets' bucket
                supabase.storage.from_("assets").upload(
                    path=filename,
                    file=f,
                    file_options={"content-type": "image/jpeg"}
                )
            
            # Get public URL
            public_url = supabase.storage.from_("assets").get_public_url(filename)
            
            # Update the item record in Supabase
            supabase.table("items").update({"image_url": public_url}).eq("sku", sku).execute()
            print(f"✅ Linked image for {sku}")

if __name__ == "__main__":
    ingest_assets()