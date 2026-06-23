import csv
import os

manifest_path = os.path.join("01_ingest", "manifests", "manifest.csv")

def validate_manifest():
    try:
        with open(manifest_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            items = list(reader)
            
            print(f"✅ Successfully read {len(items)} items from manifest.")
            for item in items:
                print(f"   -> Found: {item['title']} (SKU: {item['sku']})")
                
    except FileNotFoundError:
        print(f"❌ Error: Could not find manifest at {manifest_path}")
    except Exception as e:
        print(f"❌ Validation error: {e}")

if __name__ == "__main__":
    validate_manifest()