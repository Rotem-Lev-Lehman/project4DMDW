class Instance:
    def __init__(self):
        self.attributes = {}

    def add_attribute(self, attribute_name, value):
        if attribute_name in self.attributes:
            raise Exception("Tried to add an existing attribute")
        self.attributes[attribute_name] = value
