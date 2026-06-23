import datetime

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/process_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")
import csv
import os
import shutil
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

manifest_dir = os.path.join("01_ingest", "manifests")
archive_dir = os.path.join("01_ingest", "archive")

def ingest_and_upsert():
    for filename in os.listdir(manifest_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(manifest_dir, filename)
            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                       supabase.table("items").upsert(row, on_conflict='sku').execute()
                        msg = f"Successfully processed: {row['sku']}"
                        print(f"✅ {msg}")
                        log_event(msg)
                
                shutil.move(file_path, os.path.join(archive_dir, filename))
                log_event(f"Archived: {filename}")
            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

if __name__ == "__main__":
    ingest_and_upsert()