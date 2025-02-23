from ..models import Fruit


class FruitRepository:
    """
    An abstract class to represent an interface for a fruit repository.

    This class is meant to be inherited by a concrete implementation of a fruit repository.
    Other classes can use this interface to interact with the fruit repository without knowing the concrete implementation.
    """

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
