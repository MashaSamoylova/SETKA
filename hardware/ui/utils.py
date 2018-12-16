colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red" : (232, 16, 16),
    "green" : (16, 232, 16),
    "orange": (252, 139, 10),
    "purple" : (151, 15, 242),
    "light_green": (108, 191, 98)
}

def zfill(s, width):
    return '{:0>{w}}'.format(s, w=width)

def to_float(s):
    return '{0:0>5.1f}'.format(float(s))

def time_to_timestamp(t):
    return 60 * (60 * (24 * (30 * (t[0]) + t[1]) + t[2]) + t[3]) + t[4]

def count_time_diff(t1, t2):
    return abs(time_to_timestamp(t1) - time_to_timestamp(t2))

def chunkstring(string, length):
    return (string[i:length+i] for i in range(0, len(string), length))

def zip_longest(*args, fillvalue=None):
    iterators = [iter(it) for it in args]
    num_active = len(iterators)
    if not num_active:
        return
    while True:
        values = []
        for i, it in enumerate(iterators):
            try:
                value = next(it)
            except StopIteration:
                num_active -= 1
                if not num_active:
                    return
                iterators[i] = repeat(fillvalue)
                value = fillvalue
            values.append(value)
        yield tuple(values)

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def islice_first(iterable, n):
    first_n = list()
    try:
        for _ in range(n):
            first_n.append(next(iterable))
    except StopIteration:
        pass
    return first_n

def bytefile(f):
    b = f.read(1)
    while len(b):
        yield ord(b)
        b = f.read(1)

def file_iter(filename):
    with open(filename, 'r') as fd:
        yield from bytefile(fd)

def file_len(filename):
    with open(filename) as fd:
        length = 0
        for b in bytefile(fd): length += 1
    return length
