import streamlit as st
import requests

st.title("Binary Image Classifier 🌐")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.button("Predict"):
        with st.spinner("Sending to cloud model..."):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("https://rahuldemo9014--image-classifier-app-predict.modal.run", files=files)

            if response.status_code == 200:
                result = response.json()
                class_id = result.get("class", None)
                label = "cat" if class_id == 1 else "dog"
                st.success(f"The predicted Image is : {class_id}")
            else:
                st.error(f"Error: {response.status_code}")
