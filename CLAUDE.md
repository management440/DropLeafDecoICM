*"I am building a marketplace export module. Please create a new script at modules/marketplace_integration/export_module.py.

The script should:

Use the existing Supabase client to query all items where status equals 'ready_for_export'.

Transform the data into a flat CSV format with headers: [SKU, Title, Description, Price, Status].

Save the resulting CSV into a new directory at ./02_export/ named export_[timestamp].csv.

Ensure it includes basic error handling for database connectivity.

Do not execute the script yet, just create the module."*