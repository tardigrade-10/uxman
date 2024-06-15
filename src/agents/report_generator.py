from src.agents.base import BaseAgent
from src.prompts import GENERATE_UX_DESIGN_REPORT, GENERATE_UI_DESIGN_REPORT
from src.provider import async_creator, vision_model_defaults
from src.utils import addUsageDicts, raise_http_exception
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGeneratorAgent(BaseAgent):

    def __init__(
        self,
        image_url,
        context,
        ui_report_prompt=GENERATE_UI_DESIGN_REPORT,
        ux_report_prompt=GENERATE_UX_DESIGN_REPORT,
    ) -> None:
        super(ReportGeneratorAgent, self).__init__()
        self.image_url = image_url
        self.context = context
        self.ui_report_prompt = ui_report_prompt
        self.ux_report_prompt = ux_report_prompt
        self.report_gen_token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    async def step(self, peer_reviews: dict, report_type: str):

        try:
            logger.info(f"Generating report for type: {report_type}")

            if report_type == "ui":
                system_prompt = self.ui_report_prompt
            elif report_type == "ux":
                system_prompt = self.ux_report_prompt
            else:
                raise ValueError(f"Invalid report type: {report_type}")

            messages = [
                {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": self.image_url},
                        {"type": "text", "text": self.context},
                        {"type": "text", "text": str(peer_reviews)},
                    ],
                },
            ]
            response = await self.gen(messages)
            assistant_content = response.choices[0].message.content
            usage = response.usage.dict()
            self.report_gen_token_usage = addUsageDicts(self.report_gen_token_usage, usage)
            logger.info("Initial report content received")

            if response.choices[0].finish_reason == "length":
                logger.info("Handling 'length' finish reason")
                messages.append(
                    {"role": "assistant", "content": [{"type": "text", "text": assistant_content}]}
                )
                response = await self.gen(messages)
                new_content = response.choices[0].message.content
                assistant_content += new_content
                usage = response.usage.dict()
                self.report_gen_token_usage = addUsageDicts(self.report_gen_token_usage, usage)

            report = json.loads(assistant_content)
            return report, self.report_gen_token_usage
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise_http_exception(status_code=500, detail=str(e))

    async def gen(self, messages):
        response = await async_creator(messages=messages, **vision_model_defaults)
        return response

