from src.provider import async_client, async_creator

def imageValidator(img):
    # check whether the image is a valid app ui image and not some generic image 
    # return {valid: bool, reason: str}
    return

def contextValidator(ins):
    # use openai moderation api + some other jailbreak detection technique
    # return {valid: bool, reason: str}
    return

def basicInfoExtractor(img, ins):
    # return {theme, }
    return

def addUsageDicts(a, b):
    a["prompt_tokens"] += b["prompt_tokens"]
    a["completion_tokens"] += b["completion_tokens"]
    a["total_tokens"] += b["total_tokens"]
    return a

