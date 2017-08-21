# TO DO: used? remove?
class CalliopeBaseMixin(object):


    # NOTE: __init__ should NOT be called here, because other base classes will need to to __init_called for them instead
    
    def setup(self, *args, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def _feedback(self, msg_prefix, msg="(no message)", msg_data=None, **kwargs):
        print("%s - %s/%s: %s" % (msg_prefix, self.__class__.__name__, self.name, msg)  )
        if msg_data is not None:    
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