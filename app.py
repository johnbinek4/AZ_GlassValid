import streamlit as st
from modelHandlers import front, leftSide, leftSideMirror, back, rightSide, rightSideMirror

st.set_page_config(page_title="Car Angle Validator", layout="centered")
st.markdown("<h1 style='text-align: center;'>📷 Car Angle Validator</h1>", unsafe_allow_html=True)

labels = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]

# Initialize session
if "selected_label" not in st.session_state:
    st.session_state["selected_label"] = None
if "awaiting_photo" not in st.session_state:
    st.session_state["awaiting_photo"] = False
if "validation_results" not in st.session_state:
    st.session_state["validation_results"] = {label: None for label in labels}
if "camera_key" not in st.session_state:
    st.session_state["camera_key"] = "default"

# Custom button layout using HTML
for label in labels:
    status = st.session_state["validation_results"].get(label)
    status_icon = ""
    if status == "accepted":
        status_icon = "✅"
    elif status == "rejected":
        status_icon = "❌"

    button_html = f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <form action="" method="post">
                <button name="button" value="{label}" style="
                    padding: 10px 20px;
                    font-size: 16px;
                    width: 70vw;
                    max-width: 300px;
                    border-radius: 8px;
                    background-color: #262730;
                    color: white;
                    border: 1px solid #444;
                ">{label}</button>
            </form>
            <span style="font-size: 20px; margin-left: 10px;">{status_icon}</span>
        </div>
    """
    st.markdown(button_html, unsafe_allow_html=True)

    # Detect if form button was clicked
    if st.session_state.get("button") == label:
        st.session_state["selected_label"] = label
        st.session_state["awaiting_photo"] = True
        st.session_state["camera_key"] = f"camera_{label}"
        st.session_state["button"] = None  # Reset to avoid re-trigger

# Camera and model evaluation
if st.session_state.get("awaiting_photo", False):
    label = st.session_state["selected_label"]
    st.subheader(f"Take a photo for: **{label}**")
    st.caption("📱 If the front camera opens, switch to the back one manually.")

    photo = st.camera_input("Capture Image", key=st.session_state["camera_key"])

    if photo:
        image_bytes = photo.getvalue()

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

        # Save validation state
        if "accepted" in result.lower():
            st.success(result)
            st.session_state["validation_results"][label] = "accepted"
        elif "rejected" in result.lower():
            st.error(result)
            st.session_state["validation_results"][label] = "rejected"
        else:
            st.error("❌ Unable to validate image.")
        st.session_state["awaiting_photo"] = False
