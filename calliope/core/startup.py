import calliope

def set_select_properties(cls, parent_classes=set()):
    self_and_parent_classes = parent_classes | {cls}
    sub_classes = set(cls.child_types)

    # TO DO: extra recurion happening... WHY????

    for sub_class in sub_classes:
        if sub_class.select_property:
            for set_on_class in self_and_parent_classes:

                # print("setting", sub_class.select_property, "as", sub_class, "on", set_on_class)
                set_on_class.set_select_property(sub_class.select_property, sub_class)
                # setattr(set_on_class, sub_class.select_property, property(lambda x: x.by_type(sub_class)))

                # selections have ALL select properties
                calliope.Selection.set_select_property(sub_class.select_property, sub_class)

            # checking for infinite recursion!
            if sub_class not in self_and_parent_classes:
                set_select_properties(sub_class, self_and_parent_classes)
            
    return self_and_parent_classes

def startup():
    # set_select_properties(calliope.Bubble)
    calliope.Staff.child_types = (calliope.Segment, calliope.Cell) # TO DO ... FIX TREE hierarchy
    set_select_properties(calliope.Score)
    set_select_properties(calliope.Segment)