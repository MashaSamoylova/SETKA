class Error:

    primary_handler = lambda: 1
    notify_handler = lambda: 1
    check = lambda: 1

    def __init__(self, code):
        self.code = code


hot_melt_error = Error(1)
hot_melt_error.check = hot_melt_check

def hot_melt_check(temperature):
    if temperature > 100:
        return True
    return False
