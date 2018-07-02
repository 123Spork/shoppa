from collections import namedtuple
from importlib import import_module
import os

settings_module_name = os.environ.get('KANGA_SETTINGS', "shoppa.settings.base")
settings_module = import_module("{0}".format(settings_module_name))
settings_values = {x: y for x, y in settings_module.__dict__.items() if x.isupper()}
settings_values["module_name"] = settings_module_name
Settings = namedtuple('Settings', settings_values.keys())
settings = Settings(**settings_values)
