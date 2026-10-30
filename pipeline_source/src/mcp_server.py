import json,subprocess,os
from mcp.server.fastmcp import FastMCP
from validate import validate
BASE=os.path.dirname(os.path.abspath(__file__))+"/.."
mcp=FastMCP("ncert-bio-pipeline")
@mcp.resource("curriculum://ch8/spans")
def spans()->str:return open(f"{BASE}/source/ch8_spans.json").read()
@mcp.resource("style://biology/v1")
def style()->str:
    from style import STYLE;return json.dumps(STYLE)
@mcp.tool()
def validate_lesson(spec_file:str="specs/ch8_s82_demo.json")->dict:
    "Validate a lesson spec: schema, evidence spans, MCQ rules."
    e=validate(f"{BASE}/{spec_file}",f"{BASE}/source/ch8_spans.json");return {"valid":not e,"errors":e}
@mcp.tool()
def run_qa()->list:
    "Run the full QA gate and return the report."
    subprocess.run(["python3","qa.py"],cwd=BASE+"/src",capture_output=True);return json.load(open(f"{BASE}/build/qa_report.json"))
@mcp.tool()
def get_source_span(span_id:str)->dict:
    "Fetch an exact source span by ID."
    return next((s for s in json.load(open(f"{BASE}/source/ch8_spans.json"))["spans"] if s["id"]==span_id),{"error":"not found"})
if __name__=="__main__":mcp.run()
