import streamlit as st
from modules.marketplace_integration.export_module import (
    get_supabase_client,
    fetch_ready_for_export,
)
from modules.marketplace_integration.automation_module import orchestrate_export


def render_export_button():
    try:
        client = get_supabase_client()
        ready_items = fetch_ready_for_export(client)
    except RuntimeError as e:
        st.error(f"Export unavailable: {e}")
        return

    count = len(ready_items)

    if count == 0:
        st.info("No items are currently ready for export.")
        return

    st.write(f"**{count} item(s)** ready for export.")

    if st.button("Export Ready Items to CSV"):
        with st.spinner("Exporting, archiving, and pushing…"):
            try:
                archived_path = orchestrate_export()
                st.success(f"Done. Archived and pushed: `{archived_path}`")
            except RuntimeError as e:
                st.error(f"Automation failed: {e}")
