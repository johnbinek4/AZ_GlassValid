import streamlit as st
from modelHandlers import front, leftSide, leftSideMirror, back, rightSide, rightSideMirror

st.set_page_config(page_title="Car Angle Validator", layout="centered")
st.markdown("<h1 style='text-align: center;'>📷 Car Angle Validator</h1>", unsafe_allow_html=True)

labels = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]

# Session setup
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

def select_label(label):
    st.session_state["selected_label"] = label
    st.session_state["awaiting_photo"] = True
    st.session_state["photo_uploaded"] = None
    st.session_state["camera_key"] = f"camera_{label}"

# === Inline button + status row ===
for label in labels:
    result = st.session_state["validation_results"].get(label)
    icon_html = ""
    if result == "accepted":
        icon_html = "<span style='font-size: 26px; margin-left: 12px;'>✅</span>"
    elif result == "rejected":
        icon_html = "<span style='font-size: 26px; margin-left: 12px;'>❌</span>"

    # Layout row using HTML
    st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 10px;'>
            <form action="" method="post">
                <button name="label" value="{label}" type="submit"
                    style='flex: 1; padding: 10px 16px; font-size: 16px; width: 100%; border-radius: 6px;'>
                    {label}
                </button>
            </form>
            {icon_html}
        </div>
    """, unsafe_allow_html=True)

    # Manually capture form click (HTML workaround)
    if st.session_state.get("label_submit", "") == label or st.experimental_get_query_params().get("label") == [label]:
        select_label(label)

# === Camera input logic ===
if st.session_state["awaiting_photo"]:
    label = st.session_state["selected_label"]
    st.subheader(f"Take a photo for: **{label}**")
    st.caption("📱 If the front camera opens, please switch to the back one manually.")
    photo = st.camera_input("Capture Image", key=st.session_state["camera_key"])

    if photo:
        image_bytes = photo.getvalue()
        st.session_state["photo_uploaded"] = image_bytes

        # Call correct validation model
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

        # Save result
        if "accepted" in result.lower():
            st.success(result)
            st.session_state["validation_results"][label] = "accepted"
        elif "rejected" in result.lower():
            st.error(result)
            st.session_state["validation_results"][label] = "rejected"
            if st.button("🔄 Try Again"):
                st.session_state["awaiting_photo"] = True
                st.session_state["photo_uploaded"] = None
                st.session_state["camera_key"] = f"camera_retry_{label}"
        else:
            st.error("❌ Validation error.")
        st.session_state["awaiting_photo"] = False
