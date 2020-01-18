import re

class Cell :
    def __init__ (self, inx) :
        self.inx = inx
        self.val = 0            # unoccupied
        self.tag = ""           # with no special tag
