class Iter:
    def __init__(self, c):
        self._c = c
        self._index = -1

    def next(self):
        self._index += 1
        if self._index>=len(self._c):
            self._index = 0
        return self._c[self._index]

    def previous(self):
        self._index -= 1
        if self._index < 0:
            self._index = len(self._c)-1
        return self._c[self._index]