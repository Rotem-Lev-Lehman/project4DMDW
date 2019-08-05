import math


class Value:
    def __init__(self,name):
        self.name = name
        self.classQuantity = None
        self.appNum = None  # appearences

    def addClassQuantity(self,details):
        self.classQuantity = details

    def setAppNum(self,num):
        self.appNum = num


class Attribute:
    def __init__(self, name):
        self.name = name
        self.categories = []


class Category(Attribute):
    def __init__(self, name, categories):
        Attribute.__init__(self,name)
        self.categories = categories


class Numeric(Attribute):
    def __init__(self,name):
        self.bin_max = None
        self.bin_min = None
        self.bin_step = None
        Attribute.__init__(self,name)

    def set_bins_data(self, bin_min, bin_max, bin_step):
        self.bin_min = bin_min
        self.bin_max = bin_max
        self.bin_step = bin_step
        for i in range(self.getNumberOfBins()):
            self.categories.append(Value(str(i)))

    def get_bin_number(self, number):
        ans = int(math.floor((number - self.bin_min) / self.bin_step))
        if ans < 0:
            ans = 0
        elif ans > self.getNumberOfBins()-1:
            ans = self.getNumberOfBins() -1
        return str(ans)

    def getNumberOfBins(self):
        return int(math.floor((self.bin_max-self.bin_min)/self.bin_step))
