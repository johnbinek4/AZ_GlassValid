import streamlit as st
from modelHandlers import front, leftSide, leftSideMirror, back, rightSide, rightSideMirror

# === Config and setup ===
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

# === Show buttons with color status ===
columns = st.columns(3)

for i, label in enumerate(labels):
    with columns[i % 3]:
        # Determine color status
        result = st.session_state["validation_results"][label]
        color = "#DDDDDD"  # default grey
        if result == "accepted":
            color = "#4CAF50"  # green
        elif result == "rejected":
            color = "#FF4B4B"  # red

        # Render button
        if st.button(label, use_container_width=True):
            st.session_state["selected_label"] = label
            st.session_state["awaiting_photo"] = True

        # Colored bar under button
        st.markdown(
            f"<div style='background-color:{color}; height:5px; margin-top:4px; border-radius:4px'></div>",
            unsafe_allow_html=True
        )

# === Camera input + model validation ===
if st.session_state["awaiting_photo"]:
    label = st.session_state["selected_label"]
    st.subheader(f"Take a photo for: **{label}**")
    photo = st.camera_input("Capture Image")

    if photo:
        st.info("Processing image...")
        image_bytes = photo.getvalue()

        # Run validation using correct handler
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

        # Interpret result and give feedback
        if "accepted" in result.lower():
            st.session_state["validation_results"][label] = "accepted"
            st.success(result)
            st.session_state["awaiting_photo"] = False
        elif "rejected" in result.lower():
            st.session_state["validation_results"][label] = "rejected"
            st.error(result)
            if st.button("🔄 Try Again"):
                st.session_state["awaiting_photo"] = True
            else:
                st.session_state["awaiting_photo"] = False
        else:
            st.error("❌ Error occurred during validation.")
            st.session_state["awaiting_photo"] = False
