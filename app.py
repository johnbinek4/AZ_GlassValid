import streamlit as st
from model_handlers import front, leftSide, leftSideMirror, back, rightSide, rightSideMirror

# Setup
st.set_page_config(page_title="Image Validator", layout="centered")
st.title("📷 Car Angle Validator")

# New Labels
labels = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]
columns = st.columns(3)

# Clickable buttons
for i, label in enumerate(labels):
    with columns[i % 3]:
        if st.button(label, use_container_width=True):
            st.session_state["selected_label"] = label
            st.session_state["awaiting_photo"] = True

# Camera input logic
if st.session_state.get("awaiting_photo", False):
    label = st.session_state["selected_label"]
    st.subheader(f"Take a photo for: {label}")
    photo = st.camera_input("Capture Image")

    if photo:
        st.info("Processing image...")

        label_lower = label.lower()
        image_bytes = photo.getvalue()

        if label_lower == "front":
            result = front.validate(image_bytes)
        elif label_lower == "leftside":
            result = leftSide.validate(image_bytes)
        elif label_lower == "leftsidemirror":
            result = leftSideMirror.validate(image_bytes)
        elif label_lower == "back":
            result = back.validate(image_bytes)
        elif label_lower == "rightside":
            result = rightSide.validate(image_bytes)
        elif label_lower == "rightsidemirror":
            result = rightSideMirror.validate(image_bytes)
        else:
            result = "No model available for this label."

        st.success(result)
        st.session_state["awaiting_photo"] = False
