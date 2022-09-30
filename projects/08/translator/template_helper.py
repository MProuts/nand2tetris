from path_helper import root_path
from mako.template import Template

def render(template, **locals):
    template = Template(filename=f'{root_path}/templates/{template}.mako')
    return template.render(**locals)

def render_test(template):
    template = Template(filename=f'{root_path}/test/templates/{template}.mako')
    return template.render()
