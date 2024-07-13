# ------ string -----
def merge_str(*args, dividing=':'):
    return dividing.join([str(_) for _ in args])
