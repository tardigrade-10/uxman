from src.agents.base import BaseAgent
from src.prompts import DESIGN_PEER_REVIEW_PROMPT, GENERATE_DESIGN_REPORT
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
        self.peers_count = peers_count
        self.messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]}
        ]
        self.peer_review_token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    async def step(self):
        tasks = [self.gen() for _ in range(self.peers_count)]
        responses = await asyncio.gather(*tasks)
        reviews = []
        for response in responses:
            res_obj = response.dict()
            review = json.loads(res_obj["choices"][0]["message"]["content"])
            reviews.append(review)
            usage = res_obj["usage"]
            self.peer_review_token_usage = addUsageDicts(self.peer_review_token_usage, usage)
        print("REVIEWS:", reviews)
        return reviews, self.peer_review_token_usage

    async def gen(self):
        # messages =
        print('gen')
        _input = {
            "role": "user",
            "content": [{"type": "image_url", "image_url": self.image_url}, {"type": "text", "text": self.context}],
        }
        self.messages.append(_input)
        response = await async_creator(messages=self.messages, **vision_model_defaults)
        return response
