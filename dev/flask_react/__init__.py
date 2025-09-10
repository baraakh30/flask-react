"""
Flask-React Extension
A Flask extension for server-side React component rendering.
"""

from .extension import FlaskReact
from .renderer import ReactRenderer
from .exceptions import FlaskReactError, ComponentNotFoundError, RenderError

__version__ = '0.1.0'
__all__ = ['FlaskReact', 'ReactRenderer', 'FlaskReactError', 'ComponentNotFoundError', 'RenderError']
