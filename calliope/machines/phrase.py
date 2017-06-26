from calliope import machines

class Phrase(machines.EventMachine):
    child_types = (machines.Cell, machines.Event)