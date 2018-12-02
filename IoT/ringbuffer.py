class RingBuffer:
    def __init__(self, size):
        self.buffer = [None for i in range(0, size)]
        self.start = 0
        self.end = 0

    def add(self, val):
        self.buffer[self.end] = val
        self.end = (self.end + 1) % len(self.buffer)

    def get(self):
        val = self.buffer[self.start]
        self.start = (self.start + 1) % len(self.buffer)
        return val

    def augment(self, size):
        if self.end == 0:
            self.end = len(self.buffer)
        for i in range(len(self.buffer), size + len(self.buffer)):
            self.buffer.insert(i, None)

    def __len__(self):
        return self.end - self.start
