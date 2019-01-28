

class CalliopeBase(object):
    print_kwargs = ()

    def __init__(self, **kwargs): 

        # TO DO: consider implementing set_... to auto-set properties based on class attributes

        for set_attr in filter(lambda x: x[:4]=="dub_", dir(self)):
            setattr(self, set_attr[4:], getattr(self, set_attr))

        for name, value in kwargs.items():
            setattr(self, name, value)




class Lobster(CalliopeBase):

    _legs = 6
    _eyes = 2
    _first_name = "Reynold"
    _last_name = "Hanks"
    _rating = 2

    @property
    def legs(self): return self._legs

    @legs.setter
    def legs(self, value): 
        self._legs = value

    @property
    def rating(self): return self._rating

    @rating.setter
    def rating(self, value): 
        self._rating = value


class MaineLobster(Lobster):
    set_rating = 3
    set_legs = 5


m = MaineLobster()
print(m.rating)
