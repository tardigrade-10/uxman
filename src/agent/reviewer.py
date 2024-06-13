from __future__ import annotations
from base import BaseAgent
from PIL import Image


class Reviewer(BaseAgent):

    def __init__(self, img: str, ins: str) -> None:
        super(Reviewer, self).init()
        self.img = Image.open(img)
        self.ins = self.validate_instruction(ins)

    def step():

        pass

    def validate_instruction(ins: str):
        return ins
