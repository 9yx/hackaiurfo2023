import cv2
import numpy as np

from machine_registrator import register_machine, print_machines, get_machines, deactivate_old_machines
from resource import get_model, get_video_path, save_as_json
from move_detector import move_detector
from bbox_contains import is_bbox_contained


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


            if move_bbox is not None:
                for bbox in move_bbox:
                    x, y, w, h = bbox
                    if is_bbox_contained((x, y, x + w, y + h), (int_cords[0], int_cords[1], int_cords[2], int_cords[3])):
                        color_box = (36, 255, 12)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)

            box_id = int(box.id[0])
            sub_img_for_class = frame[int_cords[1]: int_cords[3], int_cords[0]: int_cords[2]]

            if 1 == int(box.cls[0]):
                machine_class = register_machine(box_id, "crane", None, time)
            else:
                machine_class = register_machine(box_id, None, sub_img_for_class, time)

            cv2.rectangle(frame, (int_cords[0], int_cords[1]), (int_cords[2], int_cords[3]), color_box, 2)
            cv2.putText(img=frame,
                        text="machine id : " + str(box_id) + " (" + machine_class + ")",
                        org=(int_cords[0], int_cords[1]),
                        fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1,
                        color=color_box, thickness=2
                        )

            box_new_ids.append(box_id)

        deactivate_old_machines(box_new_ids, time)
        print_machines()

        scale_percent = 60  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame, dim)

        cv2.imshow('frame', frame)

        i += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    save_as_json(get_machines())


if __name__ == '__main__':
    start_track()
