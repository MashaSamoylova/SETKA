colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red" : (232, 16, 16),
    "green" : (16, 232, 16)
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

def file_iter(filename):
    fd = open(filename)
    buf = []
    for i, line in enumerate(fd):
        buf.append(line)
        if not i % 10:
            yield from (ord(x) for y in buf for x in y)
            buf.clear()
    if buf:
        yield from (ord(x) for y in buf for x in y)
