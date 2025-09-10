"""
Tests for Flask-React extension.
"""

import pytest
import os
import tempfile
from flask import Flask
from flask_react import FlaskReact
from flask_react.exceptions import ComponentNotFoundError, RenderError


class TestFlaskReact:
    """Test Flask-React extension functionality."""
    
    @pytest.fixture
    def app(self):
        """Create a test Flask app."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def temp_components_dir(self):
        """Create a temporary directory for test components."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    @pytest.fixture
    def flask_react(self, app, temp_components_dir):
        """Create a FlaskReact instance with temporary components directory."""
        app.config['FLASK_REACT_COMPONENTS_DIR'] = temp_components_dir
        return FlaskReact(app)
    
    def test_extension_initialization(self, app):
        """Test extension initialization."""
        react = FlaskReact(app)
        assert 'flask-react' in app.extensions
        assert app.extensions['flask-react'] == react
    
    def test_config_defaults(self, app):
        """Test default configuration values."""
        FlaskReact(app)
        assert app.config['FLASK_REACT_COMPONENTS_DIR'] == 'components'
        assert app.config['FLASK_REACT_CACHE_COMPONENTS'] is True
        assert app.config['FLASK_REACT_BABEL_PRESETS'] == ['@babel/preset-react']
    
    def test_render_simple_component(self, flask_react, temp_components_dir):
        """Test rendering a simple React component."""
        # Create a simple test component
        component_code = '''
        function HelloWorld({ name }) {
            return React.createElement('div', {}, 
                React.createElement('h1', {}, 'Hello ' + (name || 'World') + '!')
            );
        }
        '''
        
        component_file = os.path.join(temp_components_dir, 'HelloWorld.jsx')
        with open(component_file, 'w') as f:
            f.write(component_code)
        
        # Render the component
        result = flask_react.render_component('HelloWorld', {'name': 'Flask'})
        
        # Check the result contains expected content
        assert 'Hello Flask!' in result
        assert '<h1>' in result
        assert '<div>' in result
    
    def test_component_not_found(self, flask_react):
        """Test error handling when component is not found."""
        with pytest.raises(ComponentNotFoundError):
            flask_react.render_component('NonExistentComponent')
    
    def test_list_components(self, flask_react, temp_components_dir):
        """Test listing available components."""
        # Create test components
        components = ['Component1.jsx', 'Component2.js', 'Component3.jsx']
        for comp in components:
            comp_file = os.path.join(temp_components_dir, comp)
            with open(comp_file, 'w') as f:
                f.write('function Component() { return React.createElement("div"); }')
        
        # List components
        available = flask_react.list_components()
        
        # Should return component names without extensions
        expected = ['Component1', 'Component2', 'Component3']
        assert sorted(available) == sorted(expected)
    
    def test_clear_cache(self, flask_react, temp_components_dir):
        """Test cache clearing functionality."""
        # Create a test component
        component_code = 'function Test() { return React.createElement("div", {}, "Test"); }'
        component_file = os.path.join(temp_components_dir, 'Test.jsx')
        with open(component_file, 'w') as f:
            f.write(component_code)
        
        # Render component (this should cache it)
        flask_react.render_component('Test')
        
        # Verify cache has the component
        assert 'Test' in flask_react.renderer._component_cache
        
        # Clear cache
        flask_react.clear_cache()
        
        # Verify cache is empty
        assert len(flask_react.renderer._component_cache) == 0
    
    def test_template_globals(self, app, flask_react):
        """Test template global functions."""
        with app.app_context():
            # Test react_component template global
            assert 'react_component' in app.jinja_env.globals
            
            # Test to_react_props filter
            assert 'to_react_props' in app.jinja_env.filters
    
    def test_props_processing(self, flask_react, temp_components_dir):
        """Test props processing with different data types."""
        # Create a component that uses props
        component_code = '''
        function PropsTest({ name, age, items, active }) {
            var itemsList = items ? items.map(function(item, i) {
                return React.createElement('li', {key: i}, item);
            }) : [];
            
            return React.createElement('div', {},
                React.createElement('h1', {}, name),
                React.createElement('p', {}, 'Age: ' + age),
                React.createElement('p', {}, 'Active: ' + (active ? 'Yes' : 'No')),
                React.createElement('ul', {}, itemsList)
            );
        }
        '''
        
        component_file = os.path.join(temp_components_dir, 'PropsTest.jsx')
        with open(component_file, 'w') as f:
            f.write(component_code)
        
        # Test with various prop types
        props = {
            'name': 'John Doe',
            'age': 30,
            'items': ['Item 1', 'Item 2', 'Item 3'],
            'active': True
        }
        
        result = flask_react.render_component('PropsTest', props)
        
        # Verify props are properly rendered
        assert 'John Doe' in result
        assert 'Age: 30' in result
        assert 'Active: Yes' in result
        assert 'Item 1' in result
        assert 'Item 2' in result
        assert 'Item 3' in result


class TestReactRenderer:
    """Test ReactRenderer class functionality."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for components."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    def test_renderer_initialization(self, temp_dir):
        """Test renderer initialization."""
        from flask_react.renderer import ReactRenderer
        
        renderer = ReactRenderer(components_dir=temp_dir)
        assert renderer.components_dir.name == os.path.basename(temp_dir)
        assert renderer.cache_enabled is True
    
    def test_load_component(self, temp_dir):
        """Test component loading."""
        from flask_react.renderer import ReactRenderer
        
        renderer = ReactRenderer(components_dir=temp_dir)
        
        # Create a test component
        component_code = 'function Test() { return React.createElement("div"); }'
        component_file = os.path.join(temp_dir, 'Test.jsx')
        with open(component_file, 'w') as f:
            f.write(component_code)
        
        # Load the component
        loaded_code = renderer._load_component('Test')
        assert loaded_code == component_code
    
    def test_component_caching(self, temp_dir):
        """Test component caching."""
        from flask_react.renderer import ReactRenderer
        
        renderer = ReactRenderer(components_dir=temp_dir, cache_enabled=True)
        
        # Create a test component
        component_code = 'function Test() { return React.createElement("div"); }'
        component_file = os.path.join(temp_dir, 'Test.jsx')
        with open(component_file, 'w') as f:
            f.write(component_code)
        
        # Load component twice
        code1 = renderer._load_component('Test')
        code2 = renderer._load_component('Test')
        
        # Should be the same and cached
        assert code1 == code2
        assert 'Test' in renderer._component_cache
    
    def test_list_components_functionality(self, temp_dir):
        """Test component listing functionality."""
        from flask_react.renderer import ReactRenderer
        
        renderer = ReactRenderer(components_dir=temp_dir)
        
        # Create test components
        components = ['Comp1.jsx', 'Comp2.js', 'NotAComponent.txt']
        for comp in components:
            comp_file = os.path.join(temp_dir, comp)
            with open(comp_file, 'w') as f:
                f.write('test content')
        
        # List components
        available = renderer.list_components()
        
        # Should only include .jsx and .js files
        expected = ['Comp1', 'Comp2']
        assert sorted(available) == sorted(expected)


if __name__ == '__main__':
    pytest.main([__file__])
