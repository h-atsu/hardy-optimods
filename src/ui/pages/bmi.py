import streamlit as st

from ui.api import create_bmi_task


def render(api_base_url: str) -> None:
    st.subheader("BMI job")

    with st.form("bmi-form"):
        weight = st.number_input("Weight (kg)", min_value=0.1, value=65.0, step=0.5)
        height = st.number_input("Height (m)", min_value=0.1, value=1.8, step=0.01)
        submitted = st.form_submit_button("Submit job", type="primary")

    if submitted:
        try:
            response = create_bmi_task(api_base_url, weight, height)
        except RuntimeError as error:
            st.error(str(error))
        else:
            st.session_state["bmi_task_id"] = response["id"]
            st.success("Job submitted.")
            st.json(response)
