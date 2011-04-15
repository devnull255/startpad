class Cell:
    def __init__(self, xy):
        self.xy = xy
        self.csums = []
        self.digits = [1,2,3,4,5,6,7,8,9]

class CSum:
    stDirName = ["Col", "Row"]
    def __init__(self, sum, xy, fRow):
        self.cells = []
        self.sum = sum
        self.xy = xy
        self.fRow = fRow

    def AddCell(self, cell):
        self.cells.append(cell)
        cell.csums.append(self)

class CrossSum:
    def __init__(self):
        self.cells = {}
        self.csums = []

    def GetCell(self, xy):
        if xy in self.cells:
            return self.cells[xy]
        self.cells[xy] = Cell(xy)
        return self.cells[xy]

    def Sums(self, spec, fRow):
        xy = (0,0)
        for rw in spec:
            for part in rw:
                if type(part) == int:
                    xy = (xy[0]+part, xy[1])
                else:
                    if fRow:
                        xyT = xy
                    else:
                        xyT = (xy[1],xy[0])
                    csum = CSum(part[0], xyT, fRow)
                    self.csums.append(csum)
                    for xyT in [(x, xy[1]) for x in range(xy[0],xy[0]+part[1])]:
                        if fRow:
                            csum.AddCell(self.GetCell(xyT))
                        else:
                            csum.AddCell(self.GetCell((xyT[1],xyT[0])))
                    xy = (xy[0]+part[1]+1, xy[1])
            xy = (0,xy[1]+1)
 

    def RowSums(self, spec):
        self.Sums(spec, True)

    def ColSums(self, spec):
        self.Sums(spec, False)

    def DumpSums(self):
        for csum in self.csums:
            print "%s %s cells at %s sums to %d" % (len(csum.cells), CSum.stDirName[csum.fRow], csum.xy, csum.sum)
        


