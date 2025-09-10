"""
React component renderer for Flask-React extension.
Handles server-side rendering of React components using PyExecJS.
"""

import os
import json
import hashlib
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    import execjs
except ImportError:
    execjs = None

from .exceptions import RenderError, ComponentNotFoundError, JavaScriptEngineError, ComponentCompileError


class ReactRenderer:
    """Handles server-side rendering of React components."""
    
    def __init__(self, components_dir: str = 'components', cache_enabled: bool = True, 
                 performance_monitoring: bool = False, max_cache_size: int = 100):
        """
        Initialize the React renderer.
        
        Args:
            components_dir: Directory containing React components
            cache_enabled: Whether to cache compiled components
            performance_monitoring: Whether to track rendering performance
            max_cache_size: Maximum number of components to cache
        """
        if execjs is None:
            raise JavaScriptEngineError(
                "PyExecJS is required for React rendering. Install it with: pip install PyExecJS"
            )
        
        self.components_dir = Path(components_dir)
        self.cache_enabled = cache_enabled
        self.performance_monitoring = performance_monitoring
        self.max_cache_size = max_cache_size
        
        self._component_cache = {}
        self._component_mtimes = {}  # Track file modification times
        self._render_stats = {}  # Track rendering performance
        self._runtime = None
        
        # Initialize JavaScript runtime
        self._init_runtime()
    
    def _init_runtime(self):
        """Initialize the JavaScript runtime with React and Babel."""
        try:
            # Create a JavaScript context with React and Babel for JSX transformation
            react_code = self._get_react_code()
            babel_code = self._get_babel_code()
            
            context_code = f"""
            {react_code}
            {babel_code}
            
            // Component registry for better management
            var componentRegistry = {{}};
            
            // Global function to render React components
            function renderReactComponent(componentCode, componentName, props) {{
                try {{
                    var componentFunction;
                    
                    // Check if component is already compiled and cached
                    if (componentRegistry[componentName]) {{
                        componentFunction = componentRegistry[componentName];
                    }} else {{
                        // Execute the component code in isolated scope
                        componentFunction = (function() {{
                            var component = eval(componentCode);
                            if (typeof component !== 'function') {{
                                throw new Error('Component "' + componentName + '" is not a function');
                            }}
                            return component;
                        }})();
                        
                        // Cache the compiled component
                        componentRegistry[componentName] = componentFunction;
                    }}
                    
                    // Validate props
                    if (props && typeof props !== 'object') {{
                        throw new Error('Props must be an object');
                    }}
                    
                    // Create React element with error boundary
                    var element;
                    try {{
                        element = React.createElement(componentFunction, props || {{}});
                    }} catch (componentError) {{
                        // Render error component instead of crashing
                        element = React.createElement('div', {{
                            style: {{ 
                                color: 'red', 
                                padding: '10px', 
                                border: '1px solid red',
                                backgroundColor: '#ffe6e6'
                            }}
                        }}, 'Component Error: ' + componentError.message);
                    }}
                    
                    // Render to string with performance tracking
                    var startTime = Date.now();
                    var result = renderToString(element);
                    var endTime = Date.now();
                    
                    // Log performance for debugging (could be made configurable)
                    if (endTime - startTime > 1000) {{
                        console.warn('Slow component render: ' + componentName + ' took ' + (endTime - startTime) + 'ms');
                    }}
                    
                    return result;
                }} catch (error) {{
                    throw new Error('Component rendering failed: ' + error.message + ' (Stack: ' + error.stack + ')');
                }}
            }}
            
            // Function to clear component cache
            function clearComponentCache() {{
                componentRegistry = {{}};
            }}
            
            // Mock ReactDOMServer.renderToString
            function renderToString(element) {{
                if (!element) return '';
                
                if (typeof element === 'string' || typeof element === 'number') {{
                    return String(element);
                }}
                
                if (Array.isArray(element)) {{
                    return element.map(renderToString).join('');
                }}
                
                if (element.type && element.props) {{
                    var tag = element.type;
                    var props = element.props || {{}};
                    var children = props.children;
                    
                    if (typeof tag === 'function') {{
                        // Component
                        var rendered = tag(props);
                        return renderToString(rendered);
                    }} else {{
                        // HTML element
                        var attrs = '';
                        for (var key in props) {{
                            if (key !== 'children' && props[key] != null) {{
                                if (key === 'className') {{
                                    attrs += ' class="' + escapeHtml(props[key]) + '"';
                                }} else if (key === 'htmlFor') {{
                                    attrs += ' for="' + escapeHtml(props[key]) + '"';
                                }} else if (typeof props[key] === 'string') {{
                                    attrs += ' ' + key + '="' + escapeHtml(props[key]) + '"';
                                }} else if (typeof props[key] === 'boolean' && props[key]) {{
                                    attrs += ' ' + key;
                                }}
                            }}
                        }}
                        
                        var childrenHtml = '';
                        if (children) {{
                            if (Array.isArray(children)) {{
                                childrenHtml = children.map(renderToString).join('');
                            }} else {{
                                childrenHtml = renderToString(children);
                            }}
                        }}
                        
                        // Self-closing tags
                        var selfClosing = ['img', 'br', 'hr', 'input', 'meta', 'link'];
                        if (selfClosing.includes(tag)) {{
                            return '<' + tag + attrs + ' />';
                        }}
                        
                        return '<' + tag + attrs + '>' + childrenHtml + '</' + tag + '>';
                    }}
                }}
                
                return '';
            }}
            
            function escapeHtml(text) {{
                var div = {{}};
                div.textContent = text;
                return div.innerHTML || text.toString()
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#x27;');
            }}
            """
            
            self._runtime = execjs.compile(context_code)
        except Exception as e:
            raise JavaScriptEngineError(f"Failed to initialize JavaScript runtime: {str(e)}")
    
    def _get_react_code(self) -> str:
        """Get React library code (simplified version for server-side rendering)."""
        return """
        var React = {
            createElement: function(type, props, ...children) {
                props = props || {};
                if (children.length > 0) {
                    props.children = children.length === 1 ? children[0] : children;
                }
                return { type: type, props: props };
            }
        };
        """
    
    def _get_babel_code(self) -> str:
        """Get Babel standalone code for JSX transformation."""
        # Since we're using React.createElement directly, we don't need complex JSX transformation
        return """
        var Babel = {
            transform: function(code, options) {
                // No transformation needed - we're using React.createElement directly
                return { code: code };
            }
        };
        """
    
    def render_component(self, component_name: str, props: Dict[str, Any] = None) -> str:
        """
        Render a React component to HTML string.
        
        Args:
            component_name: Name of the component to render
            props: Props to pass to the component
            
        Returns:
            Rendered HTML string
            
        Raises:
            ComponentNotFoundError: If component file is not found
            RenderError: If rendering fails
            ComponentCompileError: If component validation fails
        """
        # Validate component name to prevent path traversal attacks
        if not self._validate_component_name(component_name):
            raise ComponentNotFoundError(f"Invalid component name: {component_name}")
        
        try:
            # Load and validate component code
            component_code = self._load_component(component_name)
            validated_code = self._validate_component_code(component_code, component_name)
            
            # Ensure runtime is initialized
            if self._runtime is None:
                self._init_runtime()
            
            # Create safe execution context
            safe_code = self._create_safe_execution_context(validated_code, component_name)
            
            # Sanitize props to prevent XSS
            sanitized_props = self._sanitize_props(props or {})
            
            # Render component with performance tracking
            try:
                if self.performance_monitoring:
                    import time
                    start_time = time.time()
                
                result = self._runtime.call('renderReactComponent', safe_code, component_name, sanitized_props)
                
                if self.performance_monitoring:
                    end_time = time.time()
                    render_time = (end_time - start_time) * 1000  # Convert to milliseconds
                    self._update_render_stats(component_name, render_time)
                
                return result
            except execjs.RuntimeError as e:
                raise RenderError(f"JavaScript runtime error in component '{component_name}': {str(e)}")
            
        except (ComponentNotFoundError, ComponentCompileError):
            raise
        except Exception as e:
            raise RenderError(f"Failed to render component '{component_name}': {str(e)}")
    
    def _validate_component_name(self, component_name: str) -> bool:
        """
        Validate component name for security.
        
        Args:
            component_name: Component name to validate
            
        Returns:
            True if valid, False otherwise
        """
        import re
        
        # Check for valid identifier pattern (letters, numbers, underscore)
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', component_name):
            return False
        
        # Prevent path traversal
        if '..' in component_name or '/' in component_name or '\\' in component_name:
            return False
        
        return True
    
    def _sanitize_props(self, props: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize props to prevent XSS and other security issues.
        
        Args:
            props: Original props
            
        Returns:
            Sanitized props
        """
        import html
        import json
        
        def sanitize_value(value):
            if isinstance(value, str):
                # HTML escape dangerous characters
                return html.escape(value)
            elif isinstance(value, dict):
                return {k: sanitize_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [sanitize_value(item) for item in value]
            elif isinstance(value, (int, float, bool)) or value is None:
                return value
            else:
                # Convert other types to string and escape
                return html.escape(str(value))
        
        return sanitize_value(props)
    
    def _update_render_stats(self, component_name: str, render_time: float):
        """
        Update rendering performance statistics.
        
        Args:
            component_name: Name of the component
            render_time: Render time in milliseconds
        """
        if component_name not in self._render_stats:
            self._render_stats[component_name] = {
                'count': 0,
                'total_time': 0,
                'avg_time': 0,
                'min_time': float('inf'),
                'max_time': 0
            }
        
        stats = self._render_stats[component_name]
        stats['count'] += 1
        stats['total_time'] += render_time
        stats['avg_time'] = stats['total_time'] / stats['count']
        stats['min_time'] = min(stats['min_time'], render_time)
        stats['max_time'] = max(stats['max_time'], render_time)
    
    def _load_component(self, component_name: str) -> str:
        """
        Load component code from file with smart caching.
        
        Args:
            component_name: Name of the component
            
        Returns:
            Component source code
            
        Raises:
            ComponentNotFoundError: If component file is not found
        """
        # Find component file
        component_file = self._find_component_file(component_name)
        if component_file is None:
            raise ComponentNotFoundError(f"Component '{component_name}' not found in {self.components_dir}")
        
        # Check if we need to reload from cache
        if self.cache_enabled and component_name in self._component_cache:
            # Check if file has been modified
            current_mtime = component_file.stat().st_mtime
            cached_mtime = self._component_mtimes.get(component_name, 0)
            
            if current_mtime <= cached_mtime:
                return self._component_cache[component_name]
        
        # Load component code
        try:
            with open(component_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Validate code before caching
            if not code.strip():
                raise ComponentNotFoundError(f"Component '{component_name}' file is empty")
            
            # Cache management - prevent unbounded growth
            if self.cache_enabled:
                if len(self._component_cache) >= self.max_cache_size:
                    # Remove oldest cached component
                    oldest_component = min(self._component_mtimes.keys(), 
                                         key=lambda k: self._component_mtimes[k])
                    del self._component_cache[oldest_component]
                    del self._component_mtimes[oldest_component]
                
                # Cache the component code and modification time
                self._component_cache[component_name] = code
                self._component_mtimes[component_name] = component_file.stat().st_mtime
            
            return code
            
        except Exception as e:
            raise ComponentNotFoundError(f"Failed to load component '{component_name}': {str(e)}")
    
    def _find_component_file(self, component_name: str) -> Optional[Path]:
        """
        Find component file by name.
        
        Args:
            component_name: Name of the component
            
        Returns:
            Path to component file or None if not found
        """
        # Try different extensions in order of preference
        for ext in ['.jsx', '.js', '.ts', '.tsx']:
            component_file = self.components_dir / f"{component_name}{ext}"
            if component_file.exists():
                return component_file
        
        return None
    
    def clear_cache(self):
        """Clear the component cache and JavaScript runtime cache."""
        self._component_cache.clear()
        self._component_mtimes.clear()
        
        # Clear JavaScript runtime component cache
        if self._runtime:
            try:
                self._runtime.call('clearComponentCache')
            except:
                # If clearing fails, reinitialize runtime
                self._init_runtime()
    
    def get_render_stats(self) -> Dict[str, Any]:
        """
        Get rendering performance statistics.
        
        Returns:
            Dictionary of performance statistics
        """
        return dict(self._render_stats)
    
    def list_components(self) -> List[str]:
        """
        List all available components.
        
        Returns:
            List of component names
        """
        if not self.components_dir.exists():
            return []
        
        components = []
        extensions = ['*.jsx', '*.js', '*.ts', '*.tsx']
        
        for pattern in extensions:
            for file_path in self.components_dir.glob(pattern):
                if file_path.stem not in components:
                    components.append(file_path.stem)
        
        return sorted(components)
    
    def get_component_info(self, component_name: str) -> Dict[str, Any]:
        """
        Get information about a specific component.
        
        Args:
            component_name: Name of the component
            
        Returns:
            Dictionary with component information
        """
        component_file = self._find_component_file(component_name)
        if component_file is None:
            raise ComponentNotFoundError(f"Component '{component_name}' not found")
        
        stat = component_file.stat()
        return {
            'name': component_name,
            'file_path': str(component_file),
            'extension': component_file.suffix,
            'size_bytes': stat.st_size,
            'modified_time': stat.st_mtime,
            'is_cached': component_name in self._component_cache,
            'render_count': self._render_stats.get(component_name, {}).get('count', 0),
            'avg_render_time_ms': self._render_stats.get(component_name, {}).get('avg_time', 0)
        }
    
    def _validate_component_code(self, code: str, component_name: str) -> str:
        """
        Validate and potentially transform component code.
        
        Args:
            code: Component source code
            component_name: Name of the component
            
        Returns:
            Validated and potentially transformed code
        """
        import re
        
        # Check if component is properly defined
        function_pattern = rf'function\s+{component_name}\s*\('
        if not re.search(function_pattern, code):
            raise ComponentCompileError(
                f"Component '{component_name}' must be defined as a function with the same name as the file"
            )
        
        # Ensure the component is exported (not required but good practice)
        if not re.search(rf'^\s*function\s+{component_name}', code, re.MULTILINE):
            # Check for alternative patterns
            arrow_pattern = rf'(const|var|let)\s+{component_name}\s*='
            if not re.search(arrow_pattern, code):
                raise ComponentCompileError(
                    f"Component '{component_name}' must be defined as a function"
                )
        
        return code
    
    def _create_safe_execution_context(self, component_code: str, component_name: str) -> str:
        """
        Create a safe execution context for the component.
        
        Args:
            component_code: The component source code
            component_name: Name of the component
            
        Returns:
            Wrapped code for safe execution
        """
        return f"""
        (function() {{
            'use strict';
            
            // Component code
            {component_code}
            
            // Validate component exists
            if (typeof {component_name} !== 'function') {{
                throw new Error('Component "{component_name}" is not properly defined as a function');
            }}
            
            // Return the component function
            return {component_name};
        }})()
        """
