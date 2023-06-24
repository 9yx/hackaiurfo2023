from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import numpy as np
import cv2


def classification(img):
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # scale_percent = 60  # percent of original size
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # frame = cv2.resize(img, dim)

    im_pil = Image.fromarray(img)


    inputs = processor(text=["truck", "tractor", "excavator"], images=im_pil, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1).detach().numpy()

    idx = np.argmax(probs[0])

    if idx == 0:
        print("truck: " + probs[0][0].astype('str'))
        return "truck"
    if idx == 1:
        print("tractor: " + probs[0][1].astype('str'))
        return "tractor"
    if idx == 2:
        print("excavator: " + probs[0][2].astype('str'))
        return "excavator"
    if idx == 3:
        print("forklift: " + probs[0][2].astype('str'))
        return "forklift"
