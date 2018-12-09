def to_float(s):
    return '{0:0>5.1f}'.format(float(s))
def chunkstring(string, length):
    return (string[i:length+i] for i in range(0, len(string), length))
