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


