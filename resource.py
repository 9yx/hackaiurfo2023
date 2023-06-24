import json
import os
from ultralytics import YOLO


MODEL_PATH = 'model'
VIDEOS_PATH = 'videos'
TEMP_PATH = 'temp'


def get_model():
    file_names = [f for f in os.listdir(MODEL_PATH) if os.path.isfile(os.path.join(MODEL_PATH, f))]
    return YOLO(MODEL_PATH + '/' + file_names[0])


def get_video_path():
    file_names = [f for f in os.listdir(VIDEOS_PATH) if os.path.isfile(os.path.join(VIDEOS_PATH, f))]

    if len(file_names) == 0:
        raise Exception("video is empty")

    if len(file_names) == 1:
        return VIDEOS_PATH + '/' + file_names[0]

    print('Видео:')
    for n, item in enumerate(file_names):
        print(f'{n + 1}: {item}')
    n = int(input('Выбери пункт: ')) - 1

    return VIDEOS_PATH + "/" + file_names[n]

def obj_dict(obj):
    return obj.__dict__
def save_as_json(items):
    json_string = json.dumps(items, default=obj_dict)
    with open(TEMP_PATH + "/" + 'data.json', 'w') as f:
        json.dump(json_string, f)


