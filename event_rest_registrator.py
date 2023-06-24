import uuid

# Погрешность, при которой считается событие непрерывным
# (если "моргнул" фрейм, или ложно сработало движение)
exp_time_second = 3
# измеряется в секундах, минимальное значение простоя
# события с меньшим временем жизни фльтруются
minimum_lifetime_event = 3

small_ = 3
rest_list = []


# Событие, описывающие простой техники
class RestEvent:
    def __init__(self):
        self.id_object = None         #id трекера строительной техники
        self.class_object = None      #класс строительной техники
        self.id_event = None          #id события
        self.start = None             #кол-во секунд от старта видео (начало события)
        self.end = None               #кол-во секунд от старта видео (конец события)

    def __repr__(self):
        return f"<Rest id_object:{self.id_object}, id_event:{self.id_event}, start:{self.start}, end:{self.end}"


def deactivate_old_rests(ids, time):
    only_old_rests = get_old_rest(ids)
    for old_rest in only_old_rests:
        closed_rest(old_rest, time)


def get_old_rest(ids):
    old_rests = []
    rest_active_list = [r for r in rest_list if r.end is None]

    for rest in rest_active_list:
        if all(rest.id_object != new_id for new_id in ids):
            old_rests.append(rest)

    return old_rests


def register_rest(new_id, is_moved, cls, time):
    last_rest = find_last_rest(new_id)
    if last_rest is None and is_moved is False:
        add_rest(new_id, cls, time)

    if last_rest is not None and is_moved is False:
        add_or_reopen_rest(last_rest, new_id, time)

    if last_rest is not None and is_moved is True:
        closed_rest(last_rest, time)


def add_rest(new_id, cls, time):
    rest = RestEvent()
    rest.id_object = new_id
    rest.start = time
    rest.class_object = cls
    rest.id_event = str(uuid.uuid4())
    rest_list.append(rest)


def add_or_reopen_rest(last_rest, new_id, time):
    if last_rest.end is None:
        return

    if time - last_rest.end > exp_time_second:
        add_rest(new_id, time)
    else:
        reopen_rest(last_rest)


def reopen_rest(last_rest):
    last_rest.end = None


def closed_rest(last_rest, time):
    if last_rest.end is None:
        last_rest.end = time


def find_last_rest(new_id):
    rests_by_id = [rest for rest in rest_list if rest.id_object == new_id]
    if not rests_by_id:
        return None

    rests_by_id.sort(key=lambda x: x.start, reverse=True)

    return rests_by_id[0]


def print_rests():
    print(rest_list)


def filler_small_event(event_list):
    result = []
    for rest in event_list:
        if (rest.end - rest.start) >= minimum_lifetime_event:
            result.append(rest)

    return result


def get_rests():
    return rest_list


def set_last_time_if_end_none_rest(last_time):
    for rest in rest_list:
        if rest.end is None:
            rest.end = last_time
