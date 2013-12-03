"""
Utility script to display as json the django settings of wepbapp

Usage: `python scripts/print_django_settings`
"""
from types import ModuleType
from webapp import settings
from webapp.settings import *
import json

variables = {}
blacklist = ('__builtins__','__doc__','__file__','__name__','__package__')

def _set(k,_dict): 
	_dict[k]=eval(k)

def _var_filter(el):
	""" 
	Used to filter all method & submodules imported into settings. 
	Behavior: return True when process `el` is a variable defined in settings
	"""
	return 	hasattr(settings, el) and el not in blacklist \
			and not isinstance(getattr(settings, el), ModuleType)

# we loop over every valid variable to export them in a dictionnary (variables)
[_set(name, variables) for name in filter(_var_filter, dir())] 

print json.dumps(variables)