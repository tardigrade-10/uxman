from __future__ import annotations
from src.agents import PeerReviewerAgent, ReportGeneratorAgent, ReportReviewerAgent
from PIL import Image
from src.utils import (
    imageValidator,
    contextValidator,
    basicInfoExtractor,
    addUsageDicts,
    calculate_cost_gpt4_omni,
    raise_http_exception
)
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
        self.image_url_low = {
            "url": f"data:image/jpeg;base64,{encode_image(image)}",
            "detail": "low",
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
        self.token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        self.peer_count = peer_count
        self.basic_info = ""
        self.peer_reviews = {}
        self.final_review = {}

    async def __call__(self):
        pass

    async def step(self):

        # try:
        # peer review
        peer_reviewer = PeerReviewerAgent(image_url=self.image_url, peers_count=2, context=self.context)
        reviews, usage = await peer_reviewer.step()
        self.token_usage = addUsageDicts(self.token_usage, usage)
        self.stages["dpr"] = 1
        gpt_cost = calculate_cost_gpt4_omni(self.token_usage)

        # ui report generator
        report_generator = ReportGeneratorAgent(image_url=self.image_url, context=self.context)
        ui_report, usage = await report_generator.step(peer_reviews=reviews["ui_reviews"], report_type="ui")
        self.token_usage = addUsageDicts(self.token_usage, usage)

        # ux report generator
        report_generator = ReportGeneratorAgent(image_url=self.image_url, context=self.context)
        ux_report, usage = await report_generator.step(peer_reviews=reviews["ux_reviews"], report_type="ux")
        self.token_usage = addUsageDicts(self.token_usage, usage)

        self.stages["gdr"] = 1
        gpt_cost = calculate_cost_gpt4_omni(self.token_usage)

        # review final report
        return {
            "reviews": reviews,
            "report": {"ui_report": ui_report, "ux_report": ux_report},
            "usage": self.token_usage,
            "gpt_cost": gpt_cost,
            "stages": self.stages
        }
        # except Exception as e:
        #     raise SystemError(detail=e, status_code=500)

    async def _validate_image(self):
            # image validation - checks if the image is a valid app image and not a generic image
        # try:
        status, usage = await imageValidator(self.image_url_low)
        print("image validation", status)
        if status["valid"]==0:
            reason = status.get("reason")
            raise_http_exception(detail=f"Image is not valid: {reason}", status_code=401)
        self.stages["vim"] = 1
        self.token_usage = addUsageDicts(self.token_usage, usage)
        # except Exception as e:
        #     raise_http_exception(detail=e, status_code=500)


    async def _validate_context(self):
        # context validation - checks if the context is valid and not a trash or jailbreak attempt
        # try:
        status, usage = await contextValidator(self.context)
        print("context validation", status)
        if status["valid"]==0:
            reason = status.get("reason")
            raise_http_exception(detail=f"Context is not valid: {reason}", status_code=401)
        self.stages["vin"] = 1
        self.token_usage = addUsageDicts(self.token_usage, usage)
        # except Exception as e:
        #     raise_http_exception(detail=e, status_code=500)


    async def validate_input(self):
        await self._validate_image()
        if not self.context or self.context == "":
            # self.call_context_generator()  # generate new context of the image and assign it to self.context
            return
        await self._validate_context()


    async def call_basic_info_extractor(self):
        info, usage = basicInfoExtractor(self.img)
        self.basic_info = info
        self.token_usage = addUsageDicts(self.token_usage, usage)
        return


    async def init(self):
        await self.validate_input()
        # await self.call_basic_info_extractor()
        response = await self.step()
        return response
