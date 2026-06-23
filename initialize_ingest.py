import os

# Define the ingestion topology
base_path = "01_ingest"
subfolders = ["manifests", "assets", "archive"]

def initialize_topology():
    try:
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            print(f"✅ Created base: {base_path}")
        
        for folder in subfolders:
            folder_path = os.path.join(base_path, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                # Create .gitkeep to ensure empty folders are tracked
                with open(os.path.join(folder_path, ".gitkeep"), 'w') as f:
                    pass
                print(f"✅ Initialized: {folder_path}")
            else:
                print(f"ℹ️ Folder already exists: {folder_path}")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")

if __name__ == "__main__":
    initialize_topology()