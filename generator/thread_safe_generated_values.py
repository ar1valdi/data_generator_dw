import threading

__course_id = 0
__worker_id = 0
__student_id = 0
__faculty_names = set()
__study_names = set()
__contract_numbers = set()
__pesel_numbers = set()
__student_dropped_out = False

__course_id_lock = threading.Lock()
__worker_id_lock = threading.Lock()
__student_id_lock = threading.Lock()
__faculty_check_lock = threading.Lock()
__study_check_lock = threading.Lock()
__contract_check_lock = threading.Lock()
__drop_out_lock = threading.Lock()
__pesel_check_lock = threading.Lock()


def is_contract_number_unique(number):
    global __contract_numbers
    with __contract_check_lock:
        if number in __contract_numbers:
            return False
        __contract_numbers.add(number)
        return True


def is_faculty_name_unique(name):
    global __faculty_names
    with __faculty_check_lock:
        if name in __faculty_names:
            return False
        __faculty_names.add(name)
        return True


def is_study_name_unique(name):
    global __study_names
    with __study_check_lock:
        if name in __study_names:
            return False
        __study_names.add(name)
        return True


def get_course_id():
    global __course_id
    with __course_id_lock:
        __course_id += 1
        return __course_id


def get_worker_id():
    global __worker_id
    with __worker_id_lock:
        __worker_id += 1
        return __worker_id


def drop_out_used():
    global __student_dropped_out
    with __drop_out_lock:
        to_ret = __student_dropped_out
        __student_dropped_out = True
        return to_ret


def is_pesel_unique(pesel):
    global __pesel_check_lock
    with __pesel_check_lock:
        if pesel in __pesel_numbers:
            return False
        __pesel_numbers.add(pesel)
        return True


def get_student_id():
    global __student_id
    with __student_id_lock:
        __student_id += 1
        return __student_id
