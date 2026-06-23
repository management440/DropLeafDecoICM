import csv
import os
import sys
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))

def get_marketplace_data(target):
    response = supabase.table("items").select("*").execute()
    df = pd.DataFrame(response.data)
    
    # Transformation Logic
    if target == "Etsy":
        # Rename columns to Etsy requirements
        return df.rename(columns={'title': 'Listing Title', 'price': 'Price (USD)'})
    elif target == "Vinterior":
        return df[['sku', 'title', 'price', 'condition']]
    return df # Default

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "General"
    df = get_marketplace_data(target)
    df.to_csv(f"02_export/{target}_export.csv", index=False)
    print(f"✅ Generated {target} export.")