from PIL import Image
import os

files = [file for file in os.listdir() if os.path.isfile(file)]

for image in files:
    if image == "towebp.py":
        continue
    else:
        img = Image.open(image).convert("RGB")
        newname = image.replace("jpg", "webp")
        img.save(newname, "webp")
