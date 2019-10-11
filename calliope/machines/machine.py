import abjad, calliope


class Machine(calliope.Bubble, calliope.TagSet):
    """
    Base class for machines
    """
    create_container = False 

    can_have_children = True # TO DO: should be on tree? used?
    must_have_children = True # TO DO: should be on tree? used?
    transforms = () # can be set to any iterable
    factory = None
    respell = None # set to "sharps" or "flats"  to force respelling

    def __init__(self, *args, **kwargs):

        if isinstance(self, calliope.Factory):
            self.factory = self
        
        # TO DO: this is odd...
        calliope.Bubble.__init__(self, *args, **kwargs)
        calliope.TagSet.__init__(self)

        for transform in self.get_transforms():
            transform(self)

    def set_children_from_class(self, *args, **kwargs):
        """ overrides Tree's set_children_from_class in order call fabricate on factory instance """
        if self.factory is not None:
            self.factory.fabricate(self, *args, **kwargs) # TO DO... remove args/kwargs here?
        else:
            super().set_children_from_class(*args, **kwargs)

    def get_transforms(self, *args, **kwargs):
        my_transforms = []
        for transform_class_name in type(self).class_sequence( child_types=(calliope.Transform,) ): 
            my_transforms.append( getattr(self, transform_class_name)() )
        my_transforms.extend(self.transforms)
        return my_transforms
                                                            
    # TO DO... apply this same idea more generally for fragments inside of 
    # blocks for things like time_signature
    # TO DO... CONSIDER AS TAG INSTEAD?
    def get_respell(self):
        if self.respell:
            return self.respell
        elif self.parent and isinstance(self.parent, Machine):
            return self.parent.get_respell()

    @property
    def beats(self):
        return self.ticks / calliope.MACHINE_TICKS_PER_BEAT


