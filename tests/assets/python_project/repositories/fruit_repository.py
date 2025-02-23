from ..models import Fruit


class FruitRepository:
    def get_by_id(self, id):
        raise NotImplementedError()

    def get_all(self):
        raise NotImplementedError()

    def save(self, fruit: Fruit):
        raise NotImplementedError()

    def update(self, fruit: Fruit):
        raise NotImplementedError()

    def delete_by_id(self, id):
        raise NotImplementedError()
