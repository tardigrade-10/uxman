
Reqs - 
parameters to identify design evaluation
how other people are doing it?
manually doing the design - peer review - criteria
evaluate other such tools


Flow - 
1. User will input an image (a screenshot of the web page or app screenshot), along with a context to aid the design report, it can be focus areas, background info about the app, target users etc.
2. Input Validate - checks if the input is actually a web page, not a poster, or a generic image. also the context is something relevant the the input design and not some trash
3. Optional - Basic Info Extractor - Extract basic info about the app - page type, theme, industry etc. 
4. Peer Review - Identical reviewer agents review the input design and provide reviews on 5 UI and 5 UX parameters. Provide score out of 10 and comment for each paramter
5. Report Generation - Summarize all the reviews and provide a final report along with the average score of all peer reviewers
6. Optional - Report Validation - Further validate the report if it had missed something! 


to run 
python -m uvicorn main:app --reload