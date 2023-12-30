def matches_pattern(pattern, subject):
    pattern_length = len(pattern)
    pattern_index = 0

    for i in range(len(subject)):
        if pattern[pattern_index] == subject[i]:
            pattern_index += 1

            if pattern_length == pattern_index:
                return True

    return False


def index_of(array, predicate):
    for i, v in enumerate(array):
        if predicate(v):
            return i

    return None


def indexes_of(array, predicate) -> list[int]:
    return [i for i, v in enumerate(array) if predicate(v)]


COLOR_CYAN = "\u001b[36m"
COLOR_YELLOW = "\u001b[33;1m"
COLOR_RESET = "\u001b[0m"
def color(c: str, text) -> str:
    return c + str(text) + COLOR_RESET