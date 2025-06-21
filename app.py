import streamlit as st
from model_handlers import apple, banana, orange, tomato, lemon, grape

# Setup
st.set_page_config(page_title="Image Validator", layout="centered")
st.title("📷 Image Validator")

# Need Each Angle of Car Title
labels = ["Apple", "Banana", "Orange", "Tomato", "Lemon", "Grape"]
columns = st.columns(3)

# Clickable buttons
for i, label in enumerate(labels):
    with columns[i % 3]:
        if st.button(label, use_container_width=True):
            st.session_state["selected_label"] = label
            st.session_state["awaiting_photo"] = True

# Camera input
if st.session_state.get("awaiting_photo", False):
    label = st.session_state["selected_label"]
    st.subheader(f"Take a photo for: {label}")
    photo = st.camera_input("Capture Image")

    if photo:
        st.info("Processing image...")

        # Route to model based on label
        label_lower = label.lower()
        image_bytes = photo.getvalue()

        if label_lower == "apple":
            result = apple.validate(image_bytes)
        elif label_lower == "banana":
            result = banana.validate(image_bytes)
        elif label_lower == "orange":
            result = orange.validate(image_bytes)
        elif label_lower == "tomato":
            result = tomato.validate(image_bytes)
        elif label_lower == "lemon":
            result = lemon.validate(image_bytes)
        elif label_lower == "grape":
            result = grape.validate(image_bytes)
        else:
            result = "No model available for this label."

        st.success(result)
        st.session_state["awaiting_photo"] = False
