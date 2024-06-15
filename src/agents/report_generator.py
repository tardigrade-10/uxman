from src.agents.base import BaseAgent
from src.prompts import GENERATE_DESIGN_REPORT
from src.provider import async_creator, vision_model_defaults
from src.utils import addUsageDicts
import json
import asyncio


class ReportGeneratorAgent(BaseAgent):

    #  checks the peer reviews generator and summarize all the reviews

    def __init__(
        self, image_url, context, system_prompt=GENERATE_DESIGN_REPORT, peers_count=5
    ) -> None:
        super(ReportGeneratorAgent, self).__init__()
        self.image_url = image_url
        self.context = context
        self.system_prompt = system_prompt
        self.peers_count = peers_count
        self.peer_review_token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    async def step(self):
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": self.system_prompt}],
            },
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": self.image_url},
                    {"type": "text", "text": self.context},
                ],
            },
        ]
        response = await self.gen(messages)
        res_obj = response.dict()
        review = json.loads(res_obj["choices"][0]["message"]["content"])
        usage = res_obj["usage"]
        self.peer_review_token_usage = addUsageDicts(
            self.peer_review_token_usage, usage
        )
        return review, self.peer_review_token_usage

    async def gen(self, messages):
        print("gen")
        response = await async_creator(messages=messages, **vision_model_defaults)
        return response
