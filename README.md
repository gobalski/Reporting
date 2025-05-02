# Install 
## Requirements
1. pandoc
2. texlive (pdf2latex)

```shell
git clone https://github.com/gobalski/Reporting.git
python -m venv .venv
source .venv/bin/activate
pip install -r requirements
python render.py Template
```
 
# how it works
Start by copying the Template folder. Then Edit the Report.md File for the sections other then Findings. Do not touch the jinja Templating in there.
Edit your Findings inside the Findings directory. Each finding is a Markdown file.

Render the report by
```shell
python render.py <path-to-report-directory>
```

It uses jinja and pandoc to generate the report. 

# Deployment
- [ ] #someday install as a microservice
# TODOS
- [x] latex template erstellen
- [x] #idea auto ms summary table
- [ ] #idea use LLM to generate Summary
