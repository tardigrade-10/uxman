
Reqs - 
- parameters to identify design evaluation
- how other people are doing it?
- manually doing the design evaluation - peer review - criteria
- evaluate other such tools

## Solution - UXMan 😎 

Flow - 
1. User will input an image (a screenshot of the web page or app screenshot), along with a context to aid the design report, it can be focus areas, background info about the app, target users etc.
2. Input Validate - checks if the input is actually a web page, not a poster, or a generic image. also the context is something relevant the the input design and not some trash
3. Optional - Basic Info Extractor - Extract basic info about the app - page type, theme, industry etc. 
4. Peer Review - Identical reviewer agents review the input design and provide reviews on 5 UI and 5 UX parameters. Provide score out of 10 and comment for each paramter
5. Report Generation - Summarize all the reviews and provide a final report along with the average score of all peer reviewers
6. Optional - Report Validation - Further validate the report if it had missed something! 


Setup instructions
1. if you have conda installed and setup, the best way is to create a conda environment using environment.yml file

```bash
conda env create -f environment.yml
```
Otherwise, create a virtual env and install deps using requirements.txt

```bash
pip install -r requirements
```


2. How to run

```bash
python -m uvicorn main:app --reload
```

3. Head over to http://127.0.0.1:8000/docs and use the /review endpoint


### Sample Response Body 

```json
{
  "reviews": {
    "ui_reviews": {
      "visual_hierarchy": {
        "score": 9,
        "comment": "\n\nThe visual hierarchy is well-defined with clear distinctions between different sections. The use of large, bold headings and categorized sections helps users quickly find the necessary information.\n\nThe visual hierarchy is well-structured, with prominent positioning of key elements such as the tracking bar and major services. The use of large images and bold headers effectively guide the user's attention."
      },
      "typography": {
        "score": 8,
        "comment": "\n\nThe typography is clean and legible. There is good use of font sizes and weights to differentiate between headers, subheaders, and body text, making it easy to read and navigate.\n\nThe typography is clear and readable, with a good use of different font sizes to differentiate between headers and body text. However, there could be slight room for improvement in varying weights to emphasize certain content."
      },
      "color_scheme": {
        "score": 8.5,
        "comment": "\n\nThe color scheme is consistent with DHL's branding, predominantly using yellow, red, and white. This strengthens brand identity and makes the important elements stand out, though the predominant yellow background in the navigation bar might be slightly overpowering for some users.\n\nThe color scheme is consistent with DHL's branding, using their recognizable yellow and red colors. This not only reinforces brand identity but also highlights key actions and areas effectively."
      },
      "call_to_actions": {
        "score": 9.5,
        "comment": "\n\nThe call-to-action buttons are prominently displayed in red, making them stand out against the other colors. They are clearly labeled and strategically placed, guiding users toward key actions like tracking shipments, requesting quotes, and exploring services.\n\nThe call-to-actions (CTAs) are highly visible and strategically placed throughout the page. The use of red buttons ensures they stand out and the text on the buttons clearly indicates the expected action."
      },
      "navigation": {
        "score": 8,
        "comment": "\n\nNavigation is straightforward with a top bar containing primary categories and quick links at the bottom. The drop-down menus provide easy access to sub-categories, and the overall layout ensures users can move through the site efficiently.\n\nNavigation is straightforward with a clear, top-level menu that includes dropdowns for sub-categories. However, the sheer amount of information might be slightly overwhelming for a first-time user. Consider simplifying or categorizing further for ease of access."
      }
    },
    "ux_reviews": {
      "hicks_law": {
        "score": 7.5,
        "comment": "\n\nThe website provides clear and distinct options without overwhelming the user. Main actions such as tracking, shipping, and getting a quote are prominently displayed, making decision-making straightforward.\n\nThe design categorizes services effectively which aids decision-making, but there are still several options on the main page which may be overwhelming for some users."
      },
      "fitts_law": {
        "score": 8.5,
        "comment": "\n\nClickable elements such as buttons are large and well-spaced, ensuring ease of targeting. The primary 'Track' button is prominently placed and easy to click.\n\nClickable elements are large and well-spaced, making them easy to target, although some buttons could be slightly larger."
      },
      "millers_law": {
        "score": 8,
        "comment": "\n\nInformation is well-chunked into manageable sections, reducing cognitive load. Users can easily absorb the content related to different services without feeling overwhelmed.\n\nInformation is broken down into manageable chunks, but some sections have slightly more text which could affect quick comprehension."
      },
      "law_of_proximity": {
        "score": 9,
        "comment": "\n\nRelated items are grouped together effectively, enhancing the understanding and navigation through the services. The proximity of elements within sections like 'Document and Parcel Shipping' & 'Cargo Shipping' is well-executed.\n\nRelated items are grouped well, both by proximity and visual design, helping users to easily identify sections relevant to their needs."
      },
      "aesthetic_usability_effect": {
        "score": 8.5,
        "comment": "\n\nThe website is visually appealing with a professional design that inspires confidence. The use of images, icons, and colors is aesthetically pleasing, contributing to perceived usability.\n\nThe visual design is clean, professional, and engaging, which enhances the perceived usability of the site."
      }
    }
  },
  "report": {
    "ui_report": {
      "visual_hierarchy": "The visual hierarchy is well-defined with clear distinctions between different sections. The use of large, bold headings and categorized sections helps users quickly find the necessary information. Key elements such as the tracking bar and major services are prominently positioned. The use of large images and bold headers effectively guides the user's attention.",
      "typography": "The typography is clean and legible, with good use of font sizes and weights to differentiate between headers, subheaders, and body text. This makes the text easy to read and navigate. However, there could be slight room for improvement in varying font weights to emphasize certain content more.",
      "color_scheme": "The color scheme is consistent with DHL's branding, predominantly using yellow, red, and white. This strengthens brand identity and makes the important elements stand out. However, the predominant yellow background in the navigation bar might be slightly overpowering for some users.",
      "call_to_actions": "The call-to-action buttons are prominently displayed in red, making them stand out against the other colors. They are clearly labeled and strategically placed, guiding users toward key actions like tracking shipments, requesting quotes, and exploring services. The CTAs are highly visible and effectively encourage user interaction.",
      "navigation": "Navigation is straightforward with a top bar containing primary categories and quick links at the bottom. The drop-down menus provide easy access to sub-categories, ensuring users can move through the site efficiently. However, the sheer amount of information might be slightly overwhelming for a first-time user, suggesting a need for further simplification or categorization for ease of access."
    },
    "ux_report": {
      "hicks_law": "The website provides clear and distinct options without overwhelming the user. Main actions such as tracking, shipping, and getting a quote are prominently displayed, which simplifies decision-making. The categorization of services aids in decision-making, but the main page still has several options that might be overwhelming for some users.",
      "fitts_law": "Clickable elements, like buttons, are large and well-spaced, which ensures ease of targeting. The primary 'Track' button is prominently placed and easy to click. Overall, clickable elements are designed to be user-friendly, though some buttons might benefit from being slightly larger.",
      "millers_law": "Information is well-chunked into manageable sections, which reduces cognitive load, making it easier for users to absorb the content related to various services without feeling overwhelmed. However, some sections contain slightly more text which might affect quick comprehension.",
      "law_of_proximity": "Related items are effectively grouped together, which enhances understanding and navigation through the services. The proximity of elements within specific sections like 'Document and Parcel Shipping' and 'Cargo Shipping' is well-executed, helping users to easily identify relevant sections.",
      "aesthetic_usability_effect": "The website is visually appealing with a professional design that inspires confidence. The use of images, icons, and colors is aesthetically pleasing, which contributes positively to perceived usability. Overall, the visual design is clean, professional, and engaging, enhancing the site's perceived usability."
    }
  },
  "usage": {
    "prompt_tokens": 12282,
    "completion_tokens": 1697,
    "total_tokens": 13979
  },
  "gpt_cost": {
    "usd": 0.08686500000000001,
    "inr": 7.257570750000001
  },
  "stages": {
    "vim": 1,
    "vin": 1,
    "icg": 0,
    "ebi": 0,
    "dpr": 1,
    "gdr": 1,
    "rdr": 0
  }
}
```