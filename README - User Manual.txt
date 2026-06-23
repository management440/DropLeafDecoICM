ICM README

### Your Project Runbook

This is your official "User Manual" to keep the system running smoothly. Save this as `README.txt` in your `C:\icm_project\` folder.

#### 1. Daily Startup

Always ensure you are operating inside your virtual environment to keep dependencies isolated:

```powershell
cd C:\icm_project
.\venv\Scripts\activate

```

#### 2. Workflow Order

1. **Ingest Data**: Drop your CSV into `01_ingest/manifests/`, then run `python ingest_manifest.py`.
2. **Ingest Assets**: Drop your images into `01_ingest/assets/` (ensure filenames match the SKU), then run `python ingest_assets.py`.
3. **Generate Export**: Run `python export_marketplace.py` to create the final file in `02_export/`.

#### 3. Maintenance & Troubleshooting

* **Check Logs**: If anything feels "off," open `logs/process_log.txt`. It will show you exactly what occurred.
* **Archive**: Check `01_ingest/archive/` if you ever need to retrieve a previously processed manifest.
* **Database**: Your "Brain" is managed via the Supabase Dashboard. If you ever need to manually fix a record, the database will automatically handle the constraints we set up.
