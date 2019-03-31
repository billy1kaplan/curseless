from typing import TypeVar, Generic, Tuple


T = TypeVar('T')


class Message(Generic[T]):
    """
    Helper class for making and passing around messages.
    TODO: Add unique id to each message generator to ensure
          that it's the only one that can read the message
    """
    def __init__(self, id) -> None:
        self.id: str = id

    def make_message(self, payload: T = None) -> Tuple[str, T]:
        return (self.id, payload)

    def matches(self, data: Tuple[str, any]) -> bool:
        key, _ = data
        return key == self.id

    def retrieve_payload(self, data: Tuple[str, T]) -> T:
        _, payload = data
        return payload
