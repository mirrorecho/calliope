import calliope


class TreeLeaf(calliope.Tree):
    select_property = "leaves"

# eventually, try this:
# class TreeBud(calliope.Tree):
#     select_property = "buds"

class TreeTwig(calliope.Tree):
    select_property = "twigs"
    child_types = (TreeLeaf,)

class TreeBranch(calliope.Tree): 
    select_property = "branches"
TreeBranch.child_types = (TreeBranch, TreeTwig,)

class TreeTrunk(calliope.Tree): 
    select_property = "trunks"
TreeTrunk.child_types = (TreeBranch,TreeTwig,)

class TreeRoot(calliope.Tree):
    child_types = (TreeTrunk,)

TreeRoot.startup_root()

class Day(TreeTwig):
    class Morning(TreeLeaf): pass
    class Afternoon(TreeLeaf): pass
    class Evening(TreeLeaf): pass


class Week(TreeBranch):
    class Saturday(Day): pass
    class Sunday(Day): pass
    class Monday(Day): pass
    class Tuesday(Day): pass
    class Wednesday(Day): pass
    class Thursday(Day): pass
    class Friday(Day): pass

t = TreeRoot("year_end",
    TreeTrunk("december_trunk",
        Week("week0_branch",
            ),
        Week("week1_branch",
            ),
        Week("week2_branch",
            ),
        Week("week3_branch",
            ),
        ),
    )

print(calliope.SELECTION_COUNTER)

b = t.branches
# print(len(b))
# print(calliope.SELECTION_COUNTER)
# print(b[-1])

print(calliope.SELECTION_COUNTER)

b2 = b(0,2,3)
b3 = b2.depth_first(top_down=False)

for bb in b3:
    print(bb)


print(len(b2))
print(b2)
print(len(b2))

print(calliope.SELECTION_COUNTER)


# print(t.twigs[2].parentage)
# print(t.twigs[24].graph_order)


# print(calliope.SELECTION_COUNTER)
# print(t.branches[-1])
# print(calliope.SELECTION_COUNTER)
