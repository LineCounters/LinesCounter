from uuid import uuid4


class Fruit:
    id: str
    color: str
    name: str

    def __init__(self, color: str, name: str):
        self.id = str(uuid4())
        self.color = color
        self.name = name
