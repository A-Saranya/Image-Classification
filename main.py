from taipy.gui import Gui
from tensorflow.keras import models
from PIL import Image
import numpy as np

class_names = {
    0: 'airplane',
    1: 'car',
    2: 'bird',
    3: 'cat',
    4: 'deer',
    5: 'dog',
    6: 'frog',
    7: 'horse',
    8: 'ship',
    9: 'truck',
}

model = models.load_model("ml_gui_app-main/finishedProject/baseline_mariya.keras")

def predict_image(model, path_to_img):
    img = Image.open(path_to_img)
    img = img.convert("RGB")
    img = img.resize((32,32))
    data = np.asarray(img)
    data = data / 255
    probs = model.predict(np.array([data])[:1])
    top_prob = probs.max()
    top_pred = class_names[np.argmax(probs)]

    return top_prob,top_pred

content = ""
img_path = r"ml_gui_app-main/starterFiles/placeholder_image.png"
prob = 0
pred = ""

index = """
<|text-center|
<|{"ml_gui_app-main/starterFiles/logo.png"}|image|width=25vw|>

<|{content}|file_selector|extensions =.png|>
select an image from your file system

<|{pred}|>

<|{img_path}|image|>

<|{prob}|indicator|value={prob}|min=0|max=100|width=25vw|>

<|Accuracy rate indicator|>
>
"""

def on_change(state, var_name,var_val):
    if var_name == "content":
        state.img_path = var_val
        top_prob, top_pred = predict_image(model, var_val)
        state.prob = round(top_prob * 100)
        state.pred = "This is a " + top_pred
        state.img_path = var_val


app = Gui(page = index)

if __name__ == "__main__":
    app.run(use_reloader=True)
