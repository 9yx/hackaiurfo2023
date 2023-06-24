import imgaug.augmenters as iaa
from PIL import Image

image = Image.open('/home/runx/Изображения/vlcsnap-2023-06-22-21h46m28s566.png')
crop_range = (0.1, 0.9)
augmentor = iaa.Crop(percent=crop_range, keep_size=False)
image_augmented = augmentor.augment_image(image)
image_augmented.save('/home/runx/Изображения/aug.png')
