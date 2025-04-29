# Requirements
1. pandoc
2. https://raw.githubusercontent.com/pandoc-ext/include-files/refs/heads/main/include-files.lua
3. python
4. jinja2, pyyaml, re, os, shutil
5. apt install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra

# Render
``` shell
pandoc -o report.html --highlight-style=tango --lua-filter=/root/Downloads/include-files.lua 000_Report.md
```
1. process vault with custom python script (jinja templating)
2. render with pandoc via latex to pdf
## Python Skript init
```python
import re
import yaml
from jinja2 import Template

def load_md_file(file_path):
    """ Load a Markdown file and return its content and properties. """
    with open(file_path, 'r') as file:
        content = file.read()

    # Assuming the properties are in YAML format at the beginning of the file
    properties_match = re.search(r'---\s*([\s\S]*?)\s*---', content)
    
    if properties_match:
        properties_str = properties_match.group(1)
        properties = yaml.safe_load(properties_str)
        
    else:
        properties = {}

    return content, properties

def render_markdown_with_properties(file_path):
    """ Load, parse properties and render Markdown file using Jinja2. """
    content, properties = load_md_file(file_path)
    
    # Create a Jinja2 Template
    template = Template(content)
    
    # Render the Markdown content by replacing keys with their values
    rendered_content = template.render(properties)

    return rendered_content

# Example usage:
if __name__ == "__main__":
    file_path = 'example.md'  # Your markdown file path
    rendered_markdown = render_markdown_with_properties(file_path)
    print(rendered_markdown)
```

## LaTeX template init

```latex
\documentclass[11pt]{article}
\usepackage{geometry}

\geometry{margin=1in}

\title{{\Huge \textbf{$title$}}}   % Reference to title
\author{$author$}                  % Reference to author
\date{$date$}                      % Reference to date

\begin{document}

\maketitle
\tableofcontents

\section{Introduction}

% Body content will be added here
$BODY$

\end{document}
```

# Deployment
- [ ] #someday install all in a container on iyzlw.de
# TODOS
- [ ] latex template erstellen
- [ ] hyperlinks? 
- [ ] imagecaptions?
- [ ] #idea auto ms summary table
- [ ] #idea use LLM to generate Summary
