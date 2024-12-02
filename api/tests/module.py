from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import BackgroundTasks
import os
import subprocess
from ansi2html import Ansi2HTMLConverter


router = APIRouter()
template_path = os.path.join(os.path.dirname(__file__), "templates")

templates = Jinja2Templates(directory=template_path)

def run_test():
    result = subprocess.run(["pytest", "tests", "--color=yes"], capture_output=True, text=True)
    conv = Ansi2HTMLConverter()
    html_logs = conv.convert(result.stdout)
    return html_logs

@router.get("/", response_class=HTMLResponse)
def tests(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "logs": ""}, media_type="text/html")

@router.get("/run")
def run_background(background_tasks: BackgroundTasks):
    logs = run_test()
    return {"logs": logs}



