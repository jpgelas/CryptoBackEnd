
# TODO === This function is inefficient on large file. MUST be changed. =======================
def readLastLine(filename):
    with open(filename) as f:
        return (list(f)[-1])

# TODO === This function is inefficient on large file. MUST be changed. =======================
def readOneLineOverN(filename, N = 1):
    with open(filename) as f:
        counter = 0
        data = []
        for line in f:
            counter += 1
            if (counter % N == 0):
                data.append(line)
        return data


def tail(filename, window=20):
    """Returns the last `window` lines of file `filename` as a list.
    """
    with open(filename, 'rb') as f:
        if window == 0:
            return []

        BUFSIZ = 1024
        f.seek(0, 2)
        remaining_bytes = f.tell()
        size = window + 1
        block = -1
        data = []

        while size > 0 and remaining_bytes > 0:
            if remaining_bytes - BUFSIZ > 0:
                # Seek back one whole BUFSIZ
                f.seek(block * BUFSIZ, 2)
                # read BUFFER
                bunch = f.read(BUFSIZ)
            else:
                # file too small, start from beginning
                f.seek(0, 0)
                # only read what was not read
                bunch = f.read(remaining_bytes)

            bunch = bunch.decode('utf-8')
            data.insert(0, bunch)
            size -= bunch.count('\n')
            remaining_bytes -= BUFSIZ
            block -= 1

        return ''.join(data).splitlines()[-window:]


