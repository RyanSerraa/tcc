from typing_extensions import TypedDict


class State(TypedDict):
    question: str
    isEUA: bool
    query: str
    result: str
    answer: str
