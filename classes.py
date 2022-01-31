class board:
    def __init__(self, gates, gatelocations):
        # Get max x and y values of outermost chips
        max_x, max_y = (0, 0)
        for gate in gates:
            x = gates[gate][0]
            y = gates[gate][1]
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        
        # set board dimensions according to max x & y, and set z equal to the
        # amount of layers, which is always 7
        # x & y + 2 to create extra ring of space around gates
        self.width = max_x + 2
        self.length = max_y + 2
        self.height = 7
        self.gates = gates
        self.gatelocations = gatelocations
        self.nets = {}
        self.cost = 0

class path:
    def __init__(self, nodes, score):
        self.nodes = nodes
        self.score = score

class node:
    def __init__(self, location, parent):
        self.location = location
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        self.intersection = False