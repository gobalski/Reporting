from jinja2 import Template
import sys,os
from tempfile import TemporaryDirectory
import shutil
import frontmatter

def load_md_file(file_path):
    """ Load a Markdown file and return its content and properties. """
    with open(file_path, 'r') as file:
        content = file.read()
    properties = frontmatter.load(file_path).metadata
    return content, properties

def render_markdown_with_properties(file_path, findings = None):
    """ Load, parse properties and render Markdown file using Jinja2. """
    content, properties = load_md_file(file_path)
    if findings is not None:
        properties = {'findings': findings, **properties}
    template = Template(content)
    rendered_content = template.render(properties)
    return rendered_content

def render_report(report_path, working_path):
    # render Findings
    findings_metadata = load_findings_metadata(report_path)
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

    print(" [i] rendering report")

    file_path = os.path.join(report_path, '000_Report.md')
    content = render_markdown_with_properties(file_path, findings_metadata)
    out_path = os.path.join(working_path, '000_Report.md')

    with open(out_path, 'w') as f:
        f.write(content)

def load_findings_metadata(report_path):
    findings_folder = os.path.join(report_path, 'Findings')
    findings = []
    for filename in os.listdir(findings_folder):
        if filename.endswith('.md'):
            file_path = os.path.join(findings_folder, filename)
            post = frontmatter.load(file_path)
            findings_dict = post.metadata
            findings_dict['filename'] = filename
            findings.append(findings_dict)
    # replace Severity by severity_score
    for f in findings:
        sscore = float(f['severity_score'])
        if sscore >= 10:
            f['Severity'] = "Critical"
        elif sscore >= 7 and sscore < 10:
            f['Severity'] = "High"
        elif sscore >= 4 and sscore < 7:
            f['Severity'] = "Medium"
        elif sscore >= 1 and sscore < 4:
            f['Severity'] = "Low"
        elif sscore < 1:
            f['Severity'] = "Info"
    findings = sorted(findings, key=lambda x: float(x.get('severity_score', 0)), reverse=True)
    return findings

def compile_pdf(working_path, output_path, utils_path):
    print("compiling pdf")
    cmd = f"pandoc \
--verbose \
-o {output_path}/report.pdf \
--resource-path={output_path}/Res \
--lua-filter={utils_path}/include-files.lua \
--template={utils_path}/template.latex \
{working_path}/000_Report.md"
    print(cmd)
    os.chdir(working_path)
    os.system(cmd)

def compile_html(working_path, output_path, utils_path):
    print("compiling html")
    cmd = "pandoc --verbose -o " + output_path  + "/report.html --highlight-style=tango --lua-filter=" + utils_path  +  "/include-files.lua " + working_path +  "/000_Report.md"
    print(cmd)
    os.chdir(working_path)
    os.system(cmd)

    
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
