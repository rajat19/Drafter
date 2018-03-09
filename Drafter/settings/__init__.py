import os

env = os.environ.get('ENV') or 'Dev'
if env == 'Dev':
	from .dev import *
elif env == 'Prod':
	from .prod import *