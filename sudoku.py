import re

class Cell :
    def __init__ (self, inx) :
        self.inx = inx
        self.val = 0            # unoccupied
        self.tag = ""           # with no special tag
        self.error = ""         # set when updating
        self.pvals =set(range(1, 10))   # 1-9 till further notice

        self.row = row = inx/9      # row 0 - 8
        self.col = col = inx%9      # column 0=8
        boxrow = (row/3) *3; boxcol=(col/3) *3
        crn=boxrow*9+boxcol

        sameBox = range (crn,crn+3)+range(crn+9,crn+12)+range(crn+18,crn+21)
        sameRow = range(row*9,row*9+9)
        sameCol = range(col, 81, 9)
        sameBox.remove(inx); self.sameBox = tuple(sameBox)
        sameRow.remove(inx); self.sameRow = tuple(sameRow)
        sameCol.remove(inx); self.sameCol = tuple(sameCol)

    def update_pvals(self, cells) :
        allvals = set([1, 2, 3, 4, 5, 6, 7, 8, 9]); self.error = ""
        for friends in (self.sameBox,self.sameRow,self.sameCol) :
            discards = {}       # what may be removed from self.pvals
            grpvals = set([])   # as a group what vals are possible
            friends = map(lambda x: cells[x], friends)  # list of cell objs
            for other in friends :
                key = tuple(other.pvals)    # its possible value(s)
                discards[key] = discards.get(key,0) + 1
                grpvals.update(other.pvals)
            if grpvals.union(self.pvals) != allvals :
                self.error = "Not all values 1-9 possible in %s" % friends
                return False
            uncovered = allvals.difference(grpvals)
            if len(uncovered) == 1 :    # only possibility
                self.pvals = uncovered
            else :
                for key in discards.keys() :
                    if len(key) == discards[key] :
                        for used in key :
                            self.pvals.discard(used)
            if len(self.pvals) == 1 :
                self.val=tuple(self.pvals)[0]
        return True

    def __str__(s) :
        return "(%s,%s)=%s" %(s.row+1, s.col+1, s.val)

    __repr__ = __str__

#------------------------------------------------------------------------------------------


