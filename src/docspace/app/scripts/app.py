from pathlib import Path 
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))
import django
from django.conf import settings
import docspace.app.project.settings as project_settings

def module_to_dict(module):
    context = {}
    for var in dir(module):
        if not var.startswith('__') and var.isupper():
            if var == 'INSTALLED_APPS':
                context[var] = getattr(module, var) + ['core']
            context[var] = getattr(module, var)
    return context

settings.configure(**module_to_dict(project_settings))
django.setup()

from docspace.app.core.models import *
