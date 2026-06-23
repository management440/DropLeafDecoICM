import os
import base64
import json
from openai import OpenAI
from supabase import create_client
from dotenv import load_dotenv

# Setup
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))

# Generate Next SKU
def get_next_sku():
    response = supabase.table("items").select("sku").execute()
    existing_skus = [item['sku'] for item in response.data if item['sku'].startswith("SKU-")]
    if not existing_skus: return "SKU-0001"
    nums = [int(s.split("-")[1]) for s in existing_skus]
    return f"SKU-{max(nums) + 1:04d}"

# Expert AI Researcher Prompt with Chain-of-Thought
def get_ai_metadata(base64_image):
    prompt = """
    You are an expert antique and vintage design historian. Analyze this item carefully.
    
    1. VISUAL SCAN: Identify the material, shape, and notable markings or design motifs.
    2. HYPOTHESIS: Based on visual cues, identify the most likely Maker, Designer, or Factory. Estimate the Era/Period.
    3. VERIFICATION: If you are not confident in the identification, you MUST return "UNCONFIRMED" as the title.
    4. FINAL OUTPUT: Return ONLY a JSON object:
    {
        "title": "Title (e.g., 'Art Glass Vase by Keith Murray, 1940s' OR 'UNCONFIRMED')",
        "description": "2-sentence appraisal of condition and design history.",
        "category": "Broad category",
        "suggested_price": "Single number only (no range)"
    }
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

# Logic Loop
assets_dir = "01_ingest/assets"
for filename in os.listdir(assets_dir):
    if filename.endswith((".jpg", ".png")):
        path = os.path.join(assets_dir, filename)
        base64_image = base64.b64encode(open(path, "rb").read()).decode('utf-8')
        
        data = get_ai_metadata(base64_image)
        new_sku = get_next_sku()
        
        # Price Cleaning
        raw_price = str(data.get('suggested_price', '0'))
        if '-' in raw_price: raw_price = raw_price.split('-')[0]
        price_clean = float(raw_price.replace('$', '').replace(',', '').strip())
        
        # Logic to route unconfirmed items
        status = "manual_review_required" if data['title'] == "UNCONFIRMED" else "draft"
        
        item = {
            "sku": new_sku,
            "title": data['title'],
            "description": data['description'],
            "price": price_clean,
            "status": status
        }
        
        supabase.table("items").insert(item).execute()
        os.rename(path, os.path.join(assets_dir, f"{new_sku}.jpg"))
        print(f"✅ Cataloged {new_sku}: {data['title']} (Status: {status})")