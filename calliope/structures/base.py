# TO DO: used? remove?
class CalliopeBase(object):

    def __init__(self, **kwargs):
        super().__init__()
        for name, value in kwargs.items():
            setattr(self, name, value)

    def _feedback(self, msg_prefix, msg="(no message)", msg_data=None, **kwargs):
        print("%s - %s/%s: %s" % (msg_prefix, self.__class__.__name__, self.name, msg)  )
        if data is not None:    
            print(msg_data)
        for name, value in kwargs.items():
            print(name + ": " + str(value) )
        print("------------------------------------------------------------")        

    def warn(self, *args, **kwargs):
        self._feedback("WARNING", *args, **kwargs)

    def info(self, *args, **kwargs):
        self._feedback("INFO", *args, **kwargs)

    def verify(self, condition, *args, **kwargs):
        if not condition:
            self.warn(*args, **kwargs)
        return condition