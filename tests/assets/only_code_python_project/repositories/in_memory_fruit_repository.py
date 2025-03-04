from ..models.fruit import Fruit


class InMemoryFruitRepository:
    def __init__(self):
        self.fruits: list[Fruit] = []

    def get_by_id(self, id) -> Fruit | None:
        for fruit in self.fruits:
            if fruit.id == id:
                return fruit

        return None

    def get_all(self) -> list[Fruit]:
        return self.fruits

    def save(self, fruit: Fruit) -> Fruit:
        self.fruits.append(fruit)

        return fruit

    def update(self, fruit: Fruit) -> Fruit | None:
        for existing_fruit in self.fruits:
            if fruit.id == existing_fruit.id:
                existing_fruit.name = fruit.name
                existing_fruit.color = fruit.color

                return existing_fruit

        return None

    def delete_by_id(self, id) -> None:
        self.fruits = [fruit for fruit in self.fruits if fruit.id != id]
