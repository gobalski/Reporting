import re
import yaml
from jinja2 import Template
import sys,os
from tempfile import TemporaryDirectory
import shutil

def load_md_file(file_path):
    """ Load a Markdown file and return its content and properties. """
    with open(file_path, 'r') as file:
        content = file.read()

    # Assuming the properties are in YAML format at the beginning of the file
    properties_match = re.search(r'---\s*([\s\S]*?)\s*---', content)
    properties = None
    
    if properties_match:
        properties_str = properties_match.group(1)
        properties = yaml.safe_load(properties_str)
    if properties is None:
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

def render_report(report_path, working_path):
    for file in os.listdir(report_path):
        print(" [i] rendering " + file)
        if file[-2:] != 'md':
            continue
        file_path = os.path.join(report_path, file)
        content = render_markdown_with_properties(file_path)

        out_path = os.path.join(working_path, file)
        with open(out_path, 'w') as f:
            f.write(content)
    
    os.makedirs(working_path + "/Findings")
    for file in os.listdir(report_path + "/Findings"):
        print(" [i] rendering " + file)
        if file[-2:] != 'md':
            continue
        file_path = os.path.join(report_path + "/Findings", file)
        content = render_markdown_with_properties(file_path)

        out_path = os.path.join(working_path + "/Findings", file)
        with open(out_path, 'w') as f:
            f.write(content)

def compile_pdf(working_path, output_path, utils_path):
    print("compiling pdf")
    cmd = f"pandoc \
--standalone \
--verbose \
-o {output_path}/report.pdf \
--resource-path={output_path}/Res \
--lua-filter={utils_path}/include-files.lua \
--template={utils_path}/template.latex \
{working_path}/000_Report.md"
    print(cmd)
    os.chdir(working_path)
    print(os.system("ls"))
    os.system(cmd)

def compile_html(working_path, output_path, utils_path):
    print("compiling html")
    cmd = "pandoc --verbose -o " + output_path  + "/report.html --highlight-style=tango --lua-filter=" + utils_path  +  "/include-files.lua " + working_path +  "/000_Report.md"
    print(cmd)
    os.chdir(working_path)
    os.system(cmd)

    

# Example usage:
if __name__ == "__main__":
    report_path = sys.argv[1]
    report_path = os.path.abspath(report_path)
    utils_path = os.path.join(os.getcwd(), "utils")
    with TemporaryDirectory() as tmp:
        render_report(report_path, tmp)
        shutil.copytree(os.path.join(report_path, "Res"), os.path.join(tmp, "Res"))
        compile_html(tmp, report_path, utils_path)
        compile_pdf(tmp, report_path, utils_path)
        print("compiling done")
