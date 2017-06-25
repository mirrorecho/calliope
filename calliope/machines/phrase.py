from calliope import machines

class Phrase(machines.Machine):
    child_types = (machines.Cell, machines.Event)