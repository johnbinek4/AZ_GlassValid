import streamlit as st
from modelHandlers import front, leftSide, leftSideMirror, back, rightSide, rightSideMirror

# Setup
st.set_page_config(page_title="Car Angle Validator", layout="centered")
st.title("📷 Car Angle Validator")

# Define angles and model mapping
labels = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]
model_map = {
    "front": front,
    "leftSide": leftSide,
    "leftSideMirror": leftSideMirror,
    "back": back,
    "rightSide": rightSide,
    "rightSideMirror": rightSideMirror,
}

# Initialize session state
if "selected_label" not in st.session_state:
    st.session_state["selected_label"] = None
if "awaiting_photo" not in st.session_state:
    st.session_state["awaiting_photo"] = False
if "validation_results" not in st.session_state:
    st.session_state["validation_results"] = {}
if "photo_taken" not in st.session_state:
    st.session_state["photo_taken"] = {}

# Button + status icon layout
for label in labels:
    status = st.session_state["validation_results"].get(label)
    icon_html = ""

    if status == "accepted":
        icon_html = "<span style='font-size: 24px;'>✅</span>"
    elif status == "rejected":
        icon_html = "<span style='font-size: 24px;'>❌</span>"

    cols = st.columns([2, 1])
    with cols[0]:
        if st.button(label, use_container_width=True, key=f"btn_{label}"):
            st.session_state["selected_label"] = label
            st.session_state["awaiting_photo"] = True
            st.session_state["photo_taken"][label] = False  # reset camera for this label

    with cols[1]:
        st.markdown(icon_html, unsafe_allow_html=True)

# Handle camera input after button click
if st.session_state.get("awaiting_photo", False):
    label = st.session_state.get("selected_label")
    if label:
        st.subheader(f"Take a photo for: {label}")
        photo = st.camera_input("Capture Image", key=f"camera_{label}")

        if photo and not st.session_state["photo_taken"].get(label):
            st.session_state["photo_taken"][label] = True
            st.info("Processing image...")
            image_bytes = photo.getvalue()

            # Call model
            try:
                model = model_map[label]
                result = model.validate(image_bytes)
            except Exception as e:
                result = "rejected"

            # Save result
            st.session_state["validation_results"][label] = result
            st.session_state["awaiting_photo"] = False
