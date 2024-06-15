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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class UXMan:
    def __init__(self, image: str, context: str, peer_count: int = 5) -> None:
        encoded_image = encode_image(image)
        self.image_url = {
            "url": f"data:image/jpeg;base64,{encoded_image}",
            "detail": "high",
        }
        self.image_url_low = {
            "url": f"data:image/jpeg;base64,{encoded_image}",
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
        await self.init()

    async def step(self):
        try:
            peer_reviewer = PeerReviewerAgent(image_url=self.image_url, peers_count=2, context=self.context)
            reviews, usage = await peer_reviewer.step()
            self.token_usage = addUsageDicts(self.token_usage, usage)
            self.stages["dpr"] = 1

            gpt_cost = calculate_cost_gpt4_omni(self.token_usage)

            ui_report, ui_usage = await self.generate_report(reviews["ui_reviews"], "ui")
            ux_report, ux_usage = await self.generate_report(reviews["ux_reviews"], "ux")
            
            self.token_usage = addUsageDicts(self.token_usage, ui_usage)
            self.token_usage = addUsageDicts(self.token_usage, ux_usage)

            self.stages["gdr"] = 1
            gpt_cost = calculate_cost_gpt4_omni(self.token_usage)

            return {
                "reviews": reviews,
                "report": {"ui_report": ui_report, "ux_report": ux_report},
                "usage": self.token_usage,
                "gpt_cost": gpt_cost,
                "stages": self.stages
            }
        except Exception as e:
            logger.error(f"Error in step: {e}")
            raise SystemError(detail=str(e), status_code=500)

    async def generate_report(self, peer_reviews, report_type):
        try:
            report_generator = ReportGeneratorAgent(image_url=self.image_url, context=self.context)
            report, usage = await report_generator.step(peer_reviews=peer_reviews, report_type=report_type)
            return report, usage
        except Exception as e:
            logger.error(f"Error in generate_report for {report_type}: {e}")
            raise SystemError(detail=str(e), status_code=500)

    async def _validate_image(self):
        try:
            status, usage = await imageValidator(self.image_url_low)
            logger.info(f"Image validation status: {status}")
            if status["valid"] == 0:
                reason = status.get("reason")
                raise_http_exception(detail=f"Image is not valid: {reason}", status_code=401)
            self.stages["vim"] = 1
            self.token_usage = addUsageDicts(self.token_usage, usage)
        except Exception as e:
            logger.error(f"Error in _validate_image: {e}")
            raise_http_exception(detail=str(e), status_code=500)

    async def _validate_context(self):
        try:
            status, usage = await contextValidator(self.context)
            logger.info(f"Context validation status: {status}")
            if status["valid"] == 0:
                reason = status.get("reason")
                raise_http_exception(detail=f"Context is not valid: {reason}", status_code=401)
            self.stages["vin"] = 1
            self.token_usage = addUsageDicts(self.token_usage, usage)
        except Exception as e:
            logger.error(f"Error in _validate_context: {e}")
            raise_http_exception(detail=str(e), status_code=500)

    async def validate_input(self):
        await self._validate_image()
        if not self.context:
            return
        await self._validate_context()

    # async def call_basic_info_extractor(self):
    #     try:
    #         info, usage = await basicInfoExtractor(self.image_url)
    #         self.basic_info = info
    #         self.token_usage = addUsageDicts(self.token_usage, usage)
    #     except Exception as e:
    #         logger.error(f"Error in call_basic_info_extractor: {e}")
    #         raise_http_exception(detail=str(e), status_code=500)

    async def init(self):
        await self.validate_input()
        response = await self.step()
        return response
