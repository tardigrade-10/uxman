# from pydantic import BaseModel

from typing import Any


class BaseAgent:
    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def step():
        pass

    @property
    def role():
        pass
