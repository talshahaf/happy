from . import utils, bridge, java, state, widgets, configs
from . import widget_manager #must be after widgets
from .__version__ import __version__

widget_manager.init()
