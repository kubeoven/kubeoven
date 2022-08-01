from jinja2 import Environment, select_autoescape, FileSystemLoader
from kubeoven.constants import TEMPLATES_DIR
import json

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=False,
    # autoescape=select_autoescape(),
    extensions=['jinja2.ext.do']
)
jinja_env.filters['to_json'] = json.dumps


def render(name: str, **kwargs) -> str:
    template = jinja_env.get_template(name)
    return template.render(kwargs)


def render_string(source: str, **kwargs) -> str:
    template = jinja_env.from_string(source)
    return template.render(kwargs)

