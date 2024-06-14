from __future__ import annotations
from src.agents import PeerReviewerAgent, ReportGeneratorAgent, ReportReviewerAgent
from PIL import Image
from src.utils import imageValidator, contextValidator, basicInfoExtractor, addUsageDicts
import base64


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class UXMan:
    def __init__(self, image: str, context: str, peer_count: int = 5) -> None:
        # self.image = encode_image(image)
        self.image_url = {
            "url": f"data:image/jpeg;base64,{encode_image(image)}",
            "detail": "high",
        }
        self.context = context.strip()
        self.stages = {
            "vim": 0,
            "vin": 0,
            "icg": 0,
            "ebi": 0,
            "dpr": 0,
            "gdr": 0,
            "rdr": 0,
        }
        self.token_usage = {}
        self.peer_count = peer_count
        self.basic_info = ""
        self.peer_reviews = {}
        self.final_review = {}

    async def __call__(self):
        pass

    async def step(self):
        # peer review
        peer_reviewer = PeerReviewerAgent(image_url=self.image_url)
        reviews, usage = await peer_reviewer.step()
        self.token_usage += usage
        self.stages['dpr'] = 1

        # conclude peer review
        # review final report
        return {"reviews": reviews, "usage": self.token_usage, "stages": self.stages}

    def _validate_image(self):

        try:
            # image validation - checks if the image is a valid app image or not a generic image
            valid, usage = imageValidator(self.image)
            if not valid:
                raise ValueError("Image is not valid")
            self.stages["vim"] = 1
            self.token_usage += usage
        except Exception as e:
            raise e

    def _validate_context(self):
        # context validation - checks if the context is valid and not a trash or jailbreak attempt
        valid, usage = contextValidator(self.context)
        if not valid:
            raise ValueError("context is not valid")
        self.stages["vin"] = 1
        self.token_usage += usage

    def validate_input(self):
        self._validate_image()
        if not self.context or self.context == "":
            self.call_context_generator()  # generate new context of the image and assign it to self.context
        self._validate_context()

    def call_basic_info_extractor(self):
        info, usage = basicInfoExtractor(self.img)
        self.basic_info = info
        self.token_usage += usage
        return

    def init(self):

        # self.validate_input()
        # self.call_basic_info_extractor()

        response = self.step()

        # validate inputs
        # opt: generate background knowledge
        # generate basic info about the provided image
        # generate reviews * 10
        # conclude reviews
        # review the final review

        return response
