import json
import re

__author__ = 'lordgal'


def build_call_tree(func_tuples, list_of_interest, stack_by_functions):
    """
    :type func_dict: dict
    :type list_of_interest: list
    :return:
    """
    result_tree = {}
    top_level_functions = {}

    for caller, calle in func_tuples:
        top_level_functions.setdefault(caller, []).append(calle)

    for function in list_of_interest:
        result_tree["{}:{}".format(function, stack_by_functions.setdefault(function, 0))] = \
            traverse_func_list(top_level_functions, function, stack_by_functions)

    return result_tree

def traverse_func_list(functions, function_of_interest, stack_sizes):

    result = {}
    for func in functions.setdefault(function_of_interest, []):
        result["{}:{}".format(func, stack_sizes.setdefault(func, -1))] = traverse_func_list(functions, func, stack_sizes)
    return result

def parse_su_file(path):
    su_file = open(path, 'r')
    pattern = re.compile(".*:(.*)\s(\d+)\s(static|dynamic)$")
    for line in su_file:
        pattern.match(line)



if __name__ == '__main__':

    func_tuples = [
        ("chSemSignalWait", "chSchReadyI"),
        ("chSemSignalWait", "dbg_check_lock"),
        ("chSemSignalWait", "chSchGoSleepS"),
        ("chSemSignalWait", "chSchRescheduleS"),
        ("chSchReadyI", "chDbgCheckClassI"),
        ("chSchReadyI", "imaginary_func"),
        ("chDbgCheckClassI", "chDbgPanic"),
        ("chDbgCheckClassI", "fifo_remove")]

    stack = {"chSemSignalWait": 1, "chSchReadyI": 2, "dbg_check_lock": 1, "chSchGoSleepS": 1, "chSchRescheduleS": 1,
             "chDbgCheckClassI": 1, "imaginary_func": 1, "chDbgPanic": 1, "fifo_remove": 1,}


    print(json.dumps(build_call_tree(func_tuples, ["chSemSignalWait"], stack), indent=2, sort_keys=True))