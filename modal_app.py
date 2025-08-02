import modal
from fastapi import UploadFile, File
from keras.models import load_model as keras_load_model
from PIL import Image
import numpy as np
import io

app = modal.App(name="image-classifier-app")

image = (
    modal.Image.debian_slim()
    .pip_install("tensorflow", "pillow", "python-multipart", "fastapi")
    .add_local_dir("model", remote_path="/model")
)

MODEL_PATH = "/model/best_model.keras"

@app.function(image=image, min_containers=1)
def get_model():
    return keras_load_model(MODEL_PATH)

@app.function(image=image)
@modal.fastapi_endpoint(method="POST")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).resize((224, 224)).convert("RGB")
    img_array = np.array(img) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)

    model = get_model.remote()
    preds = model.predict(img_batch)

    label = "Dog" if preds[0][0] > 0.5 else "Cat"
    confidence = preds[0][0] if preds[0][0] > 0.5 else 1 - preds[0][0]

    print(f"✅ Predicted Class: ({confidence:.2f})")


    return {"class": label}
