from src.prompts.peer_review import UI_DESIGN_PEER_REVIEW_PROMPT, UX_DESIGN_PEER_REVIEW_PROMPT
from src.prompts.report_generator import GENERATE_UI_DESIGN_REPORT, GENERATE_UX_DESIGN_REPORT
from src.prompts.image_validator import IMAGE_VALIDATOR_PROMPT
from src.prompts.context_validator import CONTEXT_VALIDATOR_PROMPT


VALIDATE_IMAGE_INPUT = "is input image valid app page and not a generic image or poster"
VALIDATE_INPUT_CONTEXT = "is input ins a valid context relevant to the tool and not some trash or a jailbreak attempt"
OPTIONAL_IMAGE_CONTEXT_GENERATOR = "in case the input contexts are missing, this fill in the gaps to provide some basic information about the image and app theme"
EXTRACT_BASIC_INFO = "extract basic info like type of app, page type, industry and theme of the app etc. design aesthetics, industry, target audience, main sections, all the buttons, conversion elements, company information."



REVIEW_DESIGN_REPORT = "finally, review the design report generate and score it as well. does not change the report, just review it."

BASIC_INFO_PARAMETERS = {
    "design_aesthetics": "",
    "industry": "",
    "target_audience": "",
    "main_sections": "",
    "all_the_buttons": "",
    "conversion_elements": "",
    "company_information": ""
}