import re
from filecmp import cmp


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

        sameBox = range(crn,crn+3)+range(crn+9,crn+12)+range(crn+18,crn+21)
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

class Game :
    def __init__ (self, file, track=False) :
        """Init game from file, one row per line
        return 81 elem list (internal rep of game)"""
        self.track = track      # show each update
        self.error = None
        fil = open(file)
        row = 0
        self.cells = [0]*81
        while 1 :
            lin = fil.readline()
            if not lin : break
            if lin[0] in '#-' : continue
            lin = re.sub("\|", "" ,lin)  # rem vert bars
            lin = re.sub(" ", "" ,lin)   # cells single letter
            lin = lin[:-1] + "."*9
            for col in range(9) :
                inx = row*9+col
                cell = Cell(inx)
                char = lin[col]
                try :
                    cell.val=int(char)
                    cell.pvals=set([cell.val])
                except:
                    if char >= 'A' :
                        cell.tag=char # A-z
                self.cells[inx] = cell
            row += 1
        if row != 9 : raise Exception("Not a full 9 rows in the game")

    def clone(self) :
        # return a clone of the game
        import copy
        return copy.deepcopy(self)

    def finished(self) :
        # return true if all cells have a value
        a = filter(lambda x: x.val==0, self.cells)
        return len(a) == 0

    def valid(self) :
        # return true if no cells have a error
        a = filter(lambda x: x.error > "", self.cells)
        return len(a) == 0

    def split(self) :
        # make list of cells that still have mult pvals
        b = filter(lambda x: len(x.pvals) > 1, self.cells)
        c = list(b)
        # sort list by length of pvals. Shortest to the front
        c.sort(lambda x,y: cmp(len(x.pvals),len(y.pvals)))
        kidgames = []
        if c :
            cell = c[0]                  # take front most. It will be shortest
            for val in cell.pvals :
                g = self.clone()         # completely independent
                cell = g.cells[cell.inx] # reach for the cloned cell
                cell.val = val           # hard set the value
                cell.pvals = set([val])  # and remove it from its pvals
                kidgames.append(g)
        return kidgames

    def iterate(self) :
        changed = False
        for cell in self.cells :
            earlier = cell.pvals.copy()
            cell.update_pvals(self.cells)
            if cell.error :
                self.error = cell.error
                return changed
            if cell.pvals != earlier :
                changed = True
                if self.track and len(cell.pvals) == 1 :
                    print("Set (%s, %s) to %s" % (cell.row + 1, cell.col + 1, list(cell.pvals)[0]))
        return changed

    def getTagged(self) :
        tagged = {}
        for cell in self.cells :
            if cell.tag : tagged[cell.tag] = cell
        return tagged

    def display(self) :
        "convert sudoku game to multiline string"
        span = range(9)
        out = ""
        for row in span :
            if row == 3 or row == 6 : out += "------+-------+------\n"
            for col in span :
                if col == 3 or col == 6 : out += "| "
                cell = self.cells[row*9+col]
                what = cell.val or cell.tag or "."
                out += "%s " % what
            out += '\n'
        return out
