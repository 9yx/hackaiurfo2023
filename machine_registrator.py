import datetime

from classificator import classification

machine_list = []


class MachineItem:
    def __init__(self):
        self.id_object = None
        self.object_class = "unknown"
        self.start = None
        self.end = None

    def __repr__(self):
        return f"<Machine id_object:{self.id_object} start:{self.start} end:{self.end}"


def deactivate_old_machines(ids,time):
    only_old_machines = get_old_machines(ids)
    for oldObject in only_old_machines:
        deactivate_machine(oldObject,time)


def register_machine(new_id, cls, img, time):
    machine = find_machine(new_id)

    if machine is None:
        machine = MachineItem()
        machine.id_object = new_id
        machine.start = time

        if cls is not None:
            machine.object_class = cls
        else:
            machine.object_class = classification(img)
        machine_list.append(machine)
    else:
        machine.end = None

    return machine.object_class


def deactivate_machine(old_machine, time):
    old_machine.end = time


def compare_ids(new_ids):
    old_ids = [m.id_object for m in machine_list if m.end is None]
    return list(set(new_ids) - set(old_ids))


def get_old_machines(ids):
    old_machines = []
    machine_active_list = [m for m in machine_list if m.end is None]

    for machine in machine_active_list:
        if all(machine.id_object != new_id for new_id in ids):
            old_machines.append(machine)

    return old_machines


def find_machine(new_id):
    for machine in machine_list:
        if machine.id_object == new_id:
            return machine

    return None


def print_machines():
    print(machine_list)


def get_machines():
    return machine_list
