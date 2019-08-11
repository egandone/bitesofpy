class Animal:
    _id = 10000
    _zoo = []

    def __init__(self, name):
        Animal._id += 1
        self._id = Animal._id
        self._name = name.capitalize()
        Animal._zoo.append(str(self))

    def __str__(self):
        return f'{self._id}. {self._name}'

    @classmethod
    def zoo(cls):
        return Animal._zoo