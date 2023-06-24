import cv2
from machine_registrator import register_machine, print_machines, get_machines, deactivate_old_machines
from resource import get_model, get_video_path, save_as_json


def start_track():
    model = get_model()
    video_path = get_video_path()
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    results = model.track(source=video_path, conf=0.1, stream=True, tracker="botsort.yaml")
    i=0
    for r in results:

        time = i / fps
        frame = r.orig_img

        box_new_ids = []

        for box in r.boxes:
            cords = box.xyxy[0]
            int_cords = [int(item) for item in cords]

            box_id = int(box.id[0])
            sub_img_for_class = frame[int_cords[1]: int_cords[3], int_cords[0]: int_cords[2]]

            if 1 == int(box.cls[0]):
                machine_class = register_machine(box_id, "crane", None, time)
            else:
                machine_class = register_machine(box_id, None, sub_img_for_class, time)

            cv2.rectangle(frame, (int_cords[0], int_cords[1]), (int_cords[2], int_cords[3]), (0, 0, 255), 2)
            cv2.putText(img=frame,
                        text="machine id : " + str(box_id) + " (" + machine_class + ")",
                        org=(int_cords[0], int_cords[1]),
                        fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1,
                        color=(0, 0, 255), thickness=2
                        )

            box_new_ids.append(box_id)


        deactivate_old_machines(box_new_ids,time)
        print_machines()

        scale_percent = 60  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame, dim)

        cv2.imshow('frame', frame)
        # cv2.imshow('output', r.plot)

        i += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    save_as_json(get_machines())


if __name__ == '__main__':
    start_track()
