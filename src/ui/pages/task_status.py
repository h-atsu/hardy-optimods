from typing import Any

import pandas as pd
import streamlit as st

from ui.api import fetch_bmi_tasks


POLL_INTERVAL = "2s"


def build_rows(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for task in tasks:
        rows.append(
            {
                "id": task.get("id"),
                "weight": task.get("weight"),
                "height": task.get("height"),
                "status": task.get("status"),
                "result": task.get("result"),
                "created_at": task.get("created_at"),
            }
        )
    return rows


@st.fragment(run_every=POLL_INTERVAL)
def render_task_table(api_base_url: str) -> None:
    try:
        tasks = fetch_bmi_tasks(api_base_url)
    except RuntimeError as error:
        st.error(str(error))
        return

    if not tasks:
        st.info("No BMI jobs yet.")
        return

    rows = build_rows(tasks)
    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        use_container_width=True,
        column_order=["id", "weight", "height", "status", "result", "created_at"],
    )


def render(api_base_url: str) -> None:
    st.subheader("Task status")
    st.caption(f"Polling every {POLL_INTERVAL}.")
    render_task_table(api_base_url)
