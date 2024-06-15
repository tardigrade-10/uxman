from src.provider import (
    async_client,
    async_creator,
    vision_model_defaults,
    text_model_defaults,
)
from fastapi import HTTPException
from src.prompts import IMAGE_VALIDATOR_PROMPT, CONTEXT_VALIDATOR_PROMPT
import json

EMPTY_USAGE = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }


async def imageValidator(image_url):
    # check whether the image is a valid app ui image and not some generic image
    # return {valid: bool, reason: str}
    # try:
    messages = [
        {"role": "system", "content": [{"type": "text", "text": IMAGE_VALIDATOR_PROMPT}]},
        {"role": "user", "content": [{"type": "image_url", "image_url": image_url}]},
    ]
    response = await async_creator(messages=messages, **vision_model_defaults)
    res_obj = json.loads(response.choices[0].message.content)
    usage = response.usage.dict()
    if res_obj.get("valid"):
        return res_obj, usage
    else:
        # raise_http_exception(detail=f"invalid output {res_obj}", status_code=500)
        raise ValueError(res_obj)
    # except:
    #     raise SystemError()


async def contextValidator(context):
    # use openai moderation api + some other jailbreak detection technique
    # return {valid: bool, reason: str}
    # try: 
    resp = await async_client.moderations.create(input=context)
    if resp.results[0].flagged:
        return {"valid": 0, "reason": "openai_moderation"}, EMPTY_USAGE
    messages = [
        {"role": "system", "content": [{"type": "text", "text": CONTEXT_VALIDATOR_PROMPT}]},
        {"role": "user", "content": [{"type": "text", "text": context}]},
    ]
    response = await async_creator(messages=messages, **text_model_defaults)
    res_obj = json.loads(response.choices[0].message.content)
    usage = response.usage.dict()
    if res_obj.get("valid"):
        return res_obj, usage
    else:
        # raise_http_exception(detail=f"invalid output {res_obj}", status_code=500)
        raise ValueError(res_obj)
    # except:
    #     raise SystemError()


def basicInfoExtractor(img, ins):
    # return {theme, }
    return


def addUsageDicts(a, b):
    a["prompt_tokens"] += b["prompt_tokens"]
    a["completion_tokens"] += b["completion_tokens"]
    a["total_tokens"] += b["total_tokens"]
    return a


def calculate_cost_gpt4_omni(token_usage):
    prompt = token_usage["prompt_tokens"]
    completion = token_usage["completion_tokens"]
    cost = (prompt * 0.005 + completion * 0.015) / 1000
    rate = 83.55

    return {"usd": cost, "inr": cost * rate}


def raise_http_exception(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)
