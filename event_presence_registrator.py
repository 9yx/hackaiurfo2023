import uuid

from classificator import classification

presence_list = []


# Событие, описывающие присутствие техники
class PresenceItem:
    def __init__(self):
        self.id_object = None          #id трекера строительной техники
        self.class_object = None       #класс строительной техники
        self.id_event = None           #id события
        self.start = None              #кол-во секунд от старта видео (начало события)
        self.end = None                #кол-во секунд от старта видео (конец события)

    def __repr__(self):
        return f"<Presence id_object:{self.id_object}, id_event:{self.id_event}, start:{self.start}, end:{self.end}"


def deactivate_old_presence(ids, time):
    only_old_presence = get_old_presences(ids)
    for oldObject in only_old_presence:
        deactivate_presence(oldObject, time)


def register_presence(new_id, cls, img, time):
    presence = find_presence(new_id)

    if presence is None:
        presence = PresenceItem()
        presence.id_object = new_id
        presence.start = time
        presence.id_event = str(uuid.uuid4())

        if cls is not None:
            presence.class_object = cls
        else:
            presence.class_object = classification(img)

        presence_list.append(presence)
    else:
        presence.end = None

    return presence.class_object


def deactivate_presence(old_presence, time):
    old_presence.end = time


def get_old_presences(ids):
    old_presences = []
    presences_active_list = [m for m in presence_list if m.end is None]

    for presence in presences_active_list:
        if all(presence.id_object != new_id for new_id in ids):
            old_presences.append(presence)

    return old_presences


def find_presence(new_id):
    for presence in presence_list:
        if presence.id_object == new_id:
            return presence

    return None


def print_presences():
    print(presence_list)


def get_presences():
    return presence_list


def set_last_time_if_end_none_presence(last_time):
    for presence in presence_list:
        if presence.end is None:
            presence.end = last_time
