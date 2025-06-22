import streamlit as st
from modelHandlers import front, leftSide, leftSideMirror, back, rightSide, rightSideMirror

st.set_page_config(page_title="Car Angle Validator", layout="centered")
st.title("📷 Car Angle Validator")

labels = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]

# === Initialize session state ===
if "selected_label" not in st.session_state:
    st.session_state["selected_label"] = None
if "awaiting_photo" not in st.session_state:
    st.session_state["awaiting_photo"] = False
if "validation_results" not in st.session_state:
    st.session_state["validation_results"] = {label: None for label in labels}
if "photo_uploaded" not in st.session_state:
    st.session_state["photo_uploaded"] = None
if "camera_key" not in st.session_state:
    st.session_state["camera_key"] = "default"

# === Selection logic ===
def select_label(label):
    st.session_state["selected_label"] = label
    st.session_state["awaiting_photo"] = True
    st.session_state["photo_uploaded"] = None
    st.session_state["camera_key"] = f"camera_{label}"

# === 6-row layout: 2 columns (button + status icon) ===
for label in labels:
    col_button, col_status = st.columns([5, 1])  # wide button, narrow status
    with col_button:
        if st.button(label, key=label, use_container_width=True):
            select_label(label)
    with col_status:
        result = st.session_state["validation_results"].get(label)
        if result == "accepted":
            st.markdown("✅")
        elif result == "rejected":
            st.markdown("❌")
        else:
            st.markdown(" ")  # maintain alignment

# === Camera input when label selected ===
if st.session_state["awaiting_photo"]:
    label = st.session_state["selected_label"]
    st.subheader(f"Take a photo for: **{label}**")
    photo = st.camera_input("Capture Image", key=st.session_state["camera_key"])

    if photo:
        image_bytes = photo.getvalue()
        st.session_state["photo_uploaded"] = image_bytes

        # Run matching model
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
            result = "❌ Unknown label."

        # Handle model result
        if "accepted" in result.lower():
            st.success(result)
            st.session_state["validation_results"][label] = "accepted"
            st.session_state["awaiting_photo"] = False
        elif "rejected" in result.lower():
            st.error(result)
            st.session_state["validation_results"][label] = "rejected"
            if st.button("🔄 Try Again"):
                st.session_state["awaiting_photo"] = True
                st.session_state["photo_uploaded"] = None
                st.session_state["camera_key"] = f"camera_retry_{label}"
            else:
                st.session_state["awaiting_photo"] = False
        else:
            st.error("❌ Error during validation.")
            st.session_state["awaiting_photo"] = False
