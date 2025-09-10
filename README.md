# Flask-React

A Flask extension for server-side React component rendering with template-like functionality.

## Features

- 🚀 Server-side React component rendering
- 🎯 Flask template integration (like Jinja2)
- 🔄 Support for conditions, loops, and data binding
- 📦 Component management system
- 🎨 Props passing and state management
- 🔧 Easy Flask integration

## Installation

```bash
pip install flask-react
```

## Quick Start

```python
from flask import Flask
from flask_react import FlaskReact

app = Flask(__name__)
react = FlaskReact(app)

@app.route('/')
def home():
    return react.render_component('HelloWorld', {
        'name': 'Flask React',
        'items': ['Feature 1', 'Feature 2', 'Feature 3']
    })
```

## Usage

### Creating Components

Create React components in your `components/` directory:

```jsx
// components/HelloWorld.jsx
function HelloWorld({ name, items }) {
    return (
        <div>
            <h1>Hello {name}!</h1>
            {items && items.length > 0 && (
                <ul>
                    {items.map((item, index) => (
                        <li key={index}>{item}</li>
                    ))}
                </ul>
            )}
        </div>
    );
}
```

### Template-like Rendering

```python
@app.route('/user/<username>')
def user_profile(username):
    user_data = get_user(username)
    return react.render_component('UserProfile', {
        'user': user_data,
        'is_authenticated': current_user.is_authenticated,
        'permissions': get_user_permissions(username)
    })
```

### Conditional Rendering

```jsx
// components/UserProfile.jsx
function UserProfile({ user, is_authenticated, permissions }) {
    return (
        <div>
            <h1>{user.name}</h1>
            {is_authenticated && (
                <div className="authenticated-content">
                    <p>Welcome back!</p>
                    {permissions.includes('admin') && (
                        <button>Admin Panel</button>
                    )}
                </div>
            )}
            {!is_authenticated && (
                <div>
                    <p>Please log in to see more content.</p>
                </div>
            )}
        </div>
    );
}
```

## Configuration

```python
app.config['FLASK_REACT_COMPONENTS_DIR'] = 'components'
app.config['FLASK_REACT_BABEL_PRESETS'] = ['@babel/preset-react']
app.config['FLASK_REACT_CACHE_COMPONENTS'] = True
```

## License

MIT License
