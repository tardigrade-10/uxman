from src.agents.base import BaseAgent
from src.prompts import UI_DESIGN_PEER_REVIEW_PROMPT, UX_DESIGN_PEER_REVIEW_PROMPT
from src.provider import async_creator, vision_model_defaults
from src.utils import addUsageDicts
import json
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PeerReviewerAgent(BaseAgent):
    def __init__(
        self,
        image_url,
        context,
        ui_review_prompt=UI_DESIGN_PEER_REVIEW_PROMPT,
        ux_review_prompt=UX_DESIGN_PEER_REVIEW_PROMPT,
        peers_count=5,
    ) -> None:
        super(PeerReviewerAgent, self).__init__()
        self.image_url = image_url
        self.context = context
        self.peers_count = peers_count
        self.ui_review_prompt = ui_review_prompt
        self.ux_review_prompt = ux_review_prompt
        self.peer_review_token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        self.ui_params = [
            "visual_hierarchy",
            "typography",
            "color_scheme",
            "call_to_actions",
            "navigation",
        ]
        self.ux_params = [
            "hicks_law",
            "fitts_law",
            "millers_law",
            "law_of_proximity",
            "aesthetic_usability_effect",
        ]

    async def gen_review(self, system_prompt):
        messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": self.image_url},
                    {"type": "text", "text": self.context},
                ],
            },
        ]
        tasks = [self.gen(messages) for _ in range(self.peers_count)]
        responses = await asyncio.gather(*tasks)
        reviews = []
        for response in responses:
            res_obj = response.dict()
            review = json.loads(res_obj["choices"][0]["message"]["content"])
            reviews.append(review)
            usage = res_obj["usage"]
            self.peer_review_token_usage = addUsageDicts(self.peer_review_token_usage, usage)
        return reviews

    def get_avg_scores(self, reviews, params):
        scores_dict = {param: {"score": 0, "comment": ""} for param in params}
        for review in reviews:
            for param in params:
                scores_dict[param]["score"] += review[param]["score"]
                scores_dict[param]["comment"] += f"\n\n{review[param]['comment']}"
        for key, val in scores_dict.items():
            scores_dict[key]["score"] = val["score"] / self.peers_count
        return scores_dict

    async def step(self):
        try:
            logger.info("Starting peer review step")
            ui_reviews, ux_reviews = await asyncio.gather(
                self.gen_review(system_prompt=self.ui_review_prompt),
                self.gen_review(system_prompt=self.ux_review_prompt),
            )
            logger.info("Received reviews from generation step")
            avg_ui_scores = self.get_avg_scores(ui_reviews, self.ui_params)
            avg_ux_scores = self.get_avg_scores(ux_reviews, self.ux_params)
            return {
                "ui_reviews": avg_ui_scores,
                "ux_reviews": avg_ux_scores,
            }, self.peer_review_token_usage
        except Exception as e:
            logger.error(f"Error in step: {e}")
            raise SystemError('Error inside PeerReviewerAgent.step', e)

    async def gen(self, messages):
        logger.info("Generating review")
        response = await async_creator(messages=messages, **vision_model_defaults)
        return response
