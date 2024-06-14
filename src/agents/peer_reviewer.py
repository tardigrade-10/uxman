from src.agents.base import BaseAgent
from src.prompts.peer_review import DESIGN_PEER_REVIEW_PROMPT
from src.provider import async_creator, vision_model_defaults
from src.utils import addUsageDicts
import json
import asyncio


class PeerReviewerAgent(BaseAgent):

    def __init__(
        self, image_url, system_prompt=DESIGN_PEER_REVIEW_PROMPT, peers_count=5
    ) -> None:
        super(PeerReviewerAgent, self).__init__()
        self.image_url = image_url
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
        print(responses)
        reviews = []
        for response in responses:
            res_obj = response.dict()
            review = json.loads(res_obj["choices"][0]["message"]["content"])
            reviews.append(review)
            usage = res_obj["usage"]
            self.peer_review_token_usage = addUsageDicts(self.peer_review_token_usage, usage)
        return reviews, self.peer_review_token_usage

    async def gen(self):
        # messages =
        image_input = {
            "role": "user",
            "content": [{"type": "image_url", "image_url": self.image_url}],
        }
        self.messages.append(image_input)
        response = await async_creator(messages=self.messages, **vision_model_defaults)
        return response
