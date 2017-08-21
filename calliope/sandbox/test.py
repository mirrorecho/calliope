

class YoA(object):
    def __init__(self):
        print("YoA")

class YoB(object):
    def __init__(self):
        print("YoB")

class YoC(object):
    def __init__(self):
        print("YoC")


class Yo(YoB, YoA):
    def __init__(self):
        super().__init__()
        print("Yo")

y = Yo()