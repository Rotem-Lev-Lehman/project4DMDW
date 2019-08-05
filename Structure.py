import Attribute


class Structure:
    def __init__(self,path):
        self.classAttribute = None
        self.attributes = []
        self.readFile(path)
        if len(self.attributes) == 0:
            raise Exception("There must be attributes")
        if self.classAttribute is None:
            raise Exception("There must be a class attribute")

    def readFile(self,path):
        lines = [line.rstrip('\n') for line in open(path)]
        for line in lines:
            tokens = line.split(' ')
            if len(tokens) < 3:
                raise Exception("There are not enough information about an certain attribute")
            if tokens[0] != "@ATTRIBUTE":
                raise Exception("First token in each line must be <@ATTRIBUTE>")
            name = tokens[1]
            last_token = tokens[len(tokens)-1]
            if tokens[2] == "NUMERIC":
                newAttribute = Attribute.Numeric(name)
            elif tokens[2][0] == '{' and last_token[len(last_token)-1] == '}':
                categoriesLine = line.split('{')[1].split('}')[0]
                categories = []
                for x in categoriesLine.split(','):
                    categories.append(Attribute.Value(x))
                if len(categories) < 2:
                    raise Exception("Each categorical attribute must have at least 2 categories")
                newAttribute = Attribute.Category(name,categories)
            else:
                raise Exception("Invalid structure")
            if newAttribute.name != "class":
                self.attributes.append(newAttribute)
            else:
                if self.classAttribute is not None:
                    raise Exception("There can not be more than 1 class attribute")
                self.classAttribute = newAttribute

#x = Structure("testStructure.txt")
#y = 5
