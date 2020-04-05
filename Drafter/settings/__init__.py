import os

env = os.environ.get('ENV') or 'development'
if env == 'development':
    from .dev import *
elif env == 'production':
    from .prod import *
