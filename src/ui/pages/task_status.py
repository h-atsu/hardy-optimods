from typing import Any

import streamlit as st

from ui.api import delete_bmi_task, fetch_bmi_tasks


POLL_INTERVAL = "2s"
TABLE_COLUMNS = [4, 1, 1, 1.2, 1.2, 3, 1]


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


def format_cell(value: Any) -> str:
    if value is None:
        return "-"
    return str(value)


def render_rows(api_base_url: str, rows: list[dict[str, Any]]) -> None:
    header = st.columns(TABLE_COLUMNS)
    header[0].markdown("**ID**")
    header[1].markdown("**Weight**")
    header[2].markdown("**Height**")
    header[3].markdown("**Status**")
    header[4].markdown("**Result**")
    header[5].markdown("**Created**")
    header[6].markdown("**Action**")

    for row in rows:
        task_id = row["id"]
        cols = st.columns(TABLE_COLUMNS)
        cols[0].write(format_cell(task_id))
        cols[1].write(format_cell(row["weight"]))
        cols[2].write(format_cell(row["height"]))
        cols[3].write(format_cell(row["status"]))
        cols[4].write(format_cell(row["result"]))
        cols[5].write(format_cell(row["created_at"]))

        if cols[6].button("Delete", key=f"delete-{task_id}", disabled=not task_id):
            try:
                delete_bmi_task(api_base_url, task_id)
            except RuntimeError as error:
                st.error(str(error))
            else:
                st.success("Task deleted.")
                st.rerun()


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
    render_rows(api_base_url, rows)


def render(api_base_url: str) -> None:
    st.subheader("Task status")
    st.caption(f"Polling every {POLL_INTERVAL}.")
    render_task_table(api_base_url)
