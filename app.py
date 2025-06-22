import streamlit as st
from modelHandlers import front, leftSide, leftSideMirror, back, rightSide, rightSideMirror

# Page setup
st.set_page_config(page_title="Car Angle Validator", layout="centered")
st.markdown("<h1 style='text-align: center;'>📷 Car Angle Validator</h1>", unsafe_allow_html=True)

# Angle labels
labels = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]

# Initialize session state
if "selected_label" not in st.session_state:
    st.session_state["selected_label"] = None
if "awaiting_photo" not in st.session_state:
    st.session_state["awaiting_photo"] = False
if "validation_results" not in st.session_state:
    st.session_state["validation_results"] = {label: None for label in labels}
if "camera_key" not in st.session_state:
    st.session_state["camera_key"] = "default"

# Global button style
st.markdown("""
    <style>
    button[kind="primary"] {
        height: 45px !important;
        font-size: 18px !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Display angle buttons with status icons
for label in labels:
    col_btn, col_status = st.columns([6, 1])
    with col_btn:
        if st.button(label, key=f"btn_{label}"):
            st.session_state["selected_label"] = label
            st.session_state["awaiting_photo"] = True
            st.session_state["camera_key"] = f"camera_{label}"  # Force camera reset
    with col_status:
        result = st.session_state["validation_results"].get(label)
        if result == "accepted":
            st.markdown("✅", unsafe_allow_html=True)
        elif result == "rejected":
            st.markdown("❌", unsafe_allow_html=True)
        else:
            st.markdown("&nbsp;", unsafe_allow_html=True)

# Camera and validation
if st.session_state["awaiting_photo"]:
    label = st.session_state["selected_label"]
    st.subheader(f"Take a photo for: **{label}**")
    st.caption("📱 If the front camera opens, switch to the back one manually.")

    photo = st.camera_input("Capture Image", key=st.session_state["camera_key"])

    if photo:
        st.info("Processing image...")
        image_bytes = photo.getvalue()

        # Model validation routing
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
            result = "Error: Unknown label."

        # Show result
        if "accepted" in result.lower():
            st.success(result)
            st.session_state["validation_results"][label] = "accepted"
        elif "rejected" in result.lower():
            st.error(result)
            st.session_state["validation_results"][label] = "rejected"
        else:
            st.error("❌ Unable to validate image.")
            st.session_state["validation_results"][label] = "rejected"

        # Reset camera state
        st.session_state["awaiting_photo"] = False
