import os
from django import template
from profiler import settings

register = template.Library()

@register.simple_tag
def get_envids():
    return range(1, 101)

@register.simple_tag
def get_tests():
    files = os.listdir(settings.BASE_DIR+'/tests')
    return [os.path.splitext(i)[0] for i in files 
                if i.startswith('test') and i.endswith('.py')]