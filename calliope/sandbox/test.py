

class YoA(object):
    def __init__(self):
        super().__init__()
        print("YoA")

class YoB(object):
    def __init__(self):
        super().__init__()
        print("YoB")

class YoC(object):
    def __init__(self):
        super().__init__()
        print("YoC")


class Yo(YoB, YoA):
    def __init__(self):
        super().__init__()
        print("Yo")

y = Yo()