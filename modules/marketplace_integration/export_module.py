import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "02_export")
CSV_HEADERS = ["SKU", "Title", "Description", "Price", "Status"]


def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise EnvironmentError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment."
        )
    return create_client(url, key)


def fetch_ready_for_export(client: Client) -> list[dict]:
    response = client.table("items").select("*").eq("status", "ready_for_export").execute()
    return response.data


def transform_to_rows(items: list[dict]) -> list[list]:
    return [
        [
            item.get("sku", ""),
            item.get("title", ""),
            item.get("description", ""),
            item.get("price", ""),
            item.get("status", ""),
        ]
        for item in items
    ]


def save_csv(rows: list[list], export_dir: str) -> str:
    os.makedirs(export_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"export_{timestamp}.csv"
    filepath = os.path.join(export_dir, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)
        writer.writerows(rows)
    return filepath


def run_export() -> str:
    try:
        client = get_supabase_client()
    except EnvironmentError as e:
        raise RuntimeError(f"Database configuration error: {e}") from e

    try:
        items = fetch_ready_for_export(client)
    except Exception as e:
        raise RuntimeError(f"Failed to query Supabase: {e}") from e

    rows = transform_to_rows(items)
    filepath = save_csv(rows, EXPORT_DIR)
    return filepath


if __name__ == "__main__":
    try:
        output_path = run_export()
        print(f"Export complete: {output_path}")
    except RuntimeError as e:
        print(f"Export failed: {e}")
