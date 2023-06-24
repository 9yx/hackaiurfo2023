from ultralytics import YOLO
import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
os.environ["OMP_NUM_THREADS"] = "4"

import torch
torch.cuda.empty_cache()

if __name__ == '__main__':
#    model = YOLO("yolov8n.pt")  # загрузка предобученной модели
    model = YOLO("runs/detect/train29/weights/best.pt")
    model.train(
        data="datasets/data.yaml",
        device='0',
        epochs=300,
        verbose=True,
        imgsz=640,
#        pretrained="runs/detect/train5/weights/best.pt",
#        workers=20,
#        single_cls=True,
        batch=25
    )  # обучение модели
    model.val()  # оцените производительность модели на наборе проверки
