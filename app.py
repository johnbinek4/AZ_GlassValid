import streamlit as st
from modelHandlers import front, leftSide, leftSideMirror, back, rightSide, rightSideMirror

# Setup
st.set_page_config(page_title="Car Angle Validator", layout="centered")
st.title("📷 Car Angle Validator")

labels = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]

# === Session state init ===
if "selected_label" not in st.session_state:
    st.session_state["selected_label"] = None
if "awaiting_photo" not in st.session_state:
    st.session_state["awaiting_photo"] = False
if "validation_results" not in st.session_state:
    st.session_state["validation_results"] = {label: None for label in labels}
if "photo_uploaded" not in st.session_state:
    st.session_state["photo_uploaded"] = None

# === Clear photo when switching angles ===
def select_label(label):
    st.session_state["selected_label"] = label
    st.session_state["awaiting_photo"] = True
    st.session_state["photo_uploaded"] = None  # Clear old image

# === Styled buttons with status ===
columns = st.columns(3)
for i, label in enumerate(labels):
    with columns[i % 3]:
        result = st.session_state["validation_results"][label]
        if result == "accepted":
            btn_style = f"background-color: #4CAF50; color: white; font-weight: bold;"
        else:
            btn_style = ""

        if st.button(label, key=label, help="Tap to take a photo", use_container_width=True):
            select_label(label)

        # Optional: apply inline CSS for color if needed (Streamlit default buttons don’t support background easily)

# === Camera input ===
if st.session_state["awaiting_photo"]:
    label = st.session_state["selected_label"]
    st.subheader(f"Take a photo for: **{label}**")
    photo = st.camera_input("Capture Image")

    if photo:
        image_bytes = photo.getvalue()
        st.session_state["photo_uploaded"] = image_bytes

        # Call the correct model handler
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

        # Handle response
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
            else:
                st.session_state["awaiting_photo"] = False
        else:
            st.error("❌ Error during validation.")
            st.session_state["awaiting_photo"] = False
