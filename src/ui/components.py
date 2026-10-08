from typing import Any

import streamlit as st


def show_task_status(status: dict[str, Any]) -> None:
    task_status = status.get("status")
    result = status.get("result")

    cols = st.columns(3)
    cols[0].metric("Task ID", status.get("id", "-"))
    cols[1].metric("Status", task_status or "-")
    cols[2].metric("BMI", f"{result:.2f}" if isinstance(result, int | float) else "-")

    with st.expander("Raw response"):
        st.json(status)
