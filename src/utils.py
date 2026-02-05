import os

# Try relative import first (for when imported as a module)
try:
    from .config import config
except ImportError:
    # Fallback to absolute import (if src is in path)
    import config

def load_config():
    """
    Returns the configuration dictionary.
    """
    return config
