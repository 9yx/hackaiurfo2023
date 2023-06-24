import cv2
import numpy as np

from event_presence_registrator import register_presence, print_presences, get_presences, deactivate_old_presence, \
    set_last_time_if_end_none_presence
from resource import get_model, get_video_path, save_as_json, to_event_json
from move_detector import move_detector
from bbox_contains import is_bbox_contained
from event_rest_registrator import register_rest, deactivate_old_rests, print_rests, get_rests, filler_small_event, \
    set_last_time_if_end_none_rest


def events_to_json():
    presence_events = get_presences()
    rest_events = filler_small_event(get_rests())

    presence_json_events = list(map(lambda e: to_event_json(e, "присутствие"), presence_events))
    rest_json_events = list(map(lambda e: to_event_json(e, "простой"), rest_events))

    result_list = presence_json_events + rest_json_events
    result_list.sort(key=lambda x: (x.start, x.id_object))
    save_as_json(result_list)

def start_track():
    model = get_model()
    video_path = get_video_path()
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
    cap.release()
    results = model.track(source=video_path, conf=0.1, stream=True, tracker="botsort.yaml", agnostic_nms=True)
    i = 0
    accum_image = np.zeros((int(height), int(width)), np.uint8)
    for r in results:

        time = i / fps
        frame = r.orig_img

        box_new_ids = []

        move_bbox = move_detector(frame, i, accum_image)

        for box in r.boxes:
            cords = box.xyxy[0]
            int_cords = [int(item) for item in cords]
            color_box = (0, 0, 255)

            is_moved_box = False
            if move_bbox is not None:
                for bbox in move_bbox:
                    x, y, w, h = bbox
                    if is_bbox_contained((x, y, x + w, y + h), (int_cords[0], int_cords[1], int_cords[2], int_cords[3])):
                        color_box = (36, 255, 12)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
                        is_moved_box = True

            box_id = int(box.id[0])
            sub_img_for_class = frame[int_cords[1]: int_cords[3], int_cords[0]: int_cords[2]]

            if 1 == int(box.cls[0]):
                box_class = "crane"
            else:
                box_class = None

            machine_class = register_presence(box_id, box_class, sub_img_for_class, time)
            register_rest(box_id, is_moved_box, machine_class, time)

            cv2.rectangle(frame, (int_cords[0], int_cords[1]), (int_cords[2], int_cords[3]), color_box, 2)
            cv2.putText(img=frame,
                        text="machine id : " + str(box_id) + " (" + machine_class + ")",
                        org=(int_cords[0], int_cords[1]),
                        fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1,
                        color=color_box, thickness=2
                        )

            box_new_ids.append(box_id)

        deactivate_old_presence(box_new_ids, time)
        deactivate_old_rests(box_new_ids, time)

        print_presences()
        print_rests()

        scale_percent = 60  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame, dim)

        cv2.imshow('frame', frame)

        i += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    set_last_time_if_end_none_presence(time)
    set_last_time_if_end_none_rest(time)

    events_to_json()


if __name__ == '__main__':
    start_track()
