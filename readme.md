
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