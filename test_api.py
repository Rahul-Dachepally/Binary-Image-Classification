import requests

# Update this with your actual endpoint
url = "https://rahuldemo9014--image-classifier-app-fastapi-app-entry.modal.run/predict"

# Path to the image you want to test
image_path = "testing/2.jpg"  # make sure this path is correct

# Open and send the image as multipart/form-data
with open(image_path, "rb") as img_file:
    files = {"file": ("2.jpg", img_file, "image/jpeg")}
    response = requests.post(url, files=files)

# Check and print the response
if response.status_code == 200:
    print("✅ Prediction:", response.json())
else:
    print("❌ Error:", response.status_code)
    print("Response:", response.text)

