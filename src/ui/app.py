import streamlit as st

from ui.api import DEFAULT_API_BASE_URL
from ui.pages import bmi, task_status


st.set_page_config(page_title="Hardy Optimods UI", page_icon=":material/functions:")

with st.sidebar:
    st.header("API")
    api_base_url = st.text_input("Base URL", value=DEFAULT_API_BASE_URL)
    st.caption(
        "FastAPI server: `uv run uvicorn hardy_optimods.server:app "
        "--host 0.0.0.0 --port 8000 --reload`"
    )


def render_bmi_page() -> None:
    bmi.render(api_base_url)


def render_task_status_page() -> None:
    task_status.render(api_base_url)


pages = {
    "Jobs": [
        st.Page(
            render_bmi_page,
            title="BMI",
            icon=":material/monitor_weight:",
            url_path="bmi",
        ),
        st.Page(
            render_task_status_page,
            title="Task Status",
            icon=":material/task_alt:",
            url_path="task-status",
        ),
    ],
}

navigation = st.navigation(pages)
navigation.run()
