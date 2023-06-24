import json
import os
from ultralytics import YOLO


MODEL_PATH = 'model'
VIDEOS_PATH = 'videos'
TEMP_PATH = 'temp'

class JsonEvent:
    def __init__(self):
        self.id_object = None      #id трекера строительной техники
        self.class_object = None   #класс строительной техники
        self.id_event = None       #id события
        self.start = None          #кол-во секунд от старта видео (начало события)
        self.end = None            #кол-во секунд от старта видео (конец события)
        self.class_event = None    #тип события


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
    json_string = json.dumps(items, default=obj_dict,ensure_ascii=False )
    with open(TEMP_PATH + "/" + 'data.json', 'w') as f:
        f.write(json_string)


def to_event_json(event, class_event):
    json_event = JsonEvent()
    json_event.id_object = event.id_object
    json_event.class_object = event.class_object
    json_event.id_event = event.id_event
    json_event.start = event.start
    json_event.end = event.end
    json_event.class_event = class_event

    return json_event

