class Attribute:
    def __init__(self, name):
        self.name = name

class Category(Attribute):
    def __init__(self, name, categories):
        Attribute.__init__(self,name)
        self.categories = categories

class Numeric(Attribute):
    def __init__(self,name):
        Attribute.__init__(self,name)
