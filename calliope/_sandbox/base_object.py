

class CalliopeBase(object):
    print_kwargs = ()

    def __init__(self, **kwargs): 

        # TO DO: consider implementing set_... to auto-set properties based on class attributes

        for dub_attr in filter(lambda x: x[:5]=="init_", dir(self)):
            setattr(self, dub_attr[4:], getattr(self.__class__, dub_attr))

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
    init_rating = 3
    init_legs = 5

class AlaskanLobster(MaineLobster):
    init_rating = 1
    pass

l = Lobster()
m = MaineLobster(rating=4)
a = AlaskanLobster(rating=0)
print(l.rating, m.rating, a.rating)

