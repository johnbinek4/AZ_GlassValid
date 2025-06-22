import streamlit as st
from modelHandlers import front, leftSide, leftSideMirror, back, rightSide, rightSideMirror

# Streamlit setup
st.set_page_config(page_title="Car Angle Validator", layout="centered")
st.title("📷 Car Angle Validator")

# Labels
labels = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]

# Initialize session state
if "selected_label" not in st.session_state:
    st.session_state.selected_label = None
if "awaiting_photo" not in st.session_state:
    st.session_state.awaiting_photo = False
if "validation_results" not in st.session_state:
    st.session_state.validation_results = {label: None for label in labels}
if "camera_key" not in st.session_state:
    st.session_state.camera_key = "default"

# Render buttons with status icons
for label in labels:
    col_button, col_status = st.columns([5, 1])
    with col_button:
        if st.button(label, use_container_width=True):
            st.session_state.selected_label = label
            st.session_state.awaiting_photo = True
            st.session_state.camera_key = f"camera_{label}"  # resets camera

    with col_status:
        result = st.session_state.validation_results.get(label)
        if result == "accepted":
            st.markdown("✅")
        elif result == "rejected":
            st.markdown("❌")

# Show camera if needed
if st.session_state.awaiting_photo:
    label = st.session_state.selected_label
    st.subheader(f"Take a photo for: {label}")
    st.caption("📱 If the front camera opens, switch to the back one manually.")

    photo = st.camera_input("Capture Image", key=st.session_state.camera_key)

    if photo:
        st.info("Processing image...")

        image_bytes = photo.getvalue()

        # Route to the correct model
        if label == "front":
            result = front.validate(image_bytes)
        elif label == "leftSide":
            result = leftSide.validate(image_bytes)
        elif label == "leftSideMirror":
            result = leftSideMirror.validate(image_bytes)
        elif label == "back":
            result = back.validate(image_bytes)
        elif label == "rightSide":
            result = rightSide.validate(image_bytes)
        elif label == "rightSideMirror":
            result = rightSideMirror.validate(image_bytes)
        else:
            result = "No model available."

        # Set status
        if "accepted" in result.lower():
            st.success(result)
            st.session_state.validation_results[label] = "accepted"
        elif "rejected" in result.lower():
            st.error(result)
            st.session_state.validation_results[label] = "rejected"
        else:
            st.error("❌ Could not determine result.")

        st.session_state.awaiting_photo = False
