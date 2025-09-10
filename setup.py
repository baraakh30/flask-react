from setuptools import setup, find_packages

setup(
    name='flask-react',
    version='0.1.0',
    description='A Flask extension for server-side React component rendering using Node.js',
    author='Baraa Khanfar',
    author_email='baraa60@icloud.com',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0.0',
        'Jinja2>=3.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
            'black>=21.0.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'flask-react=flask_react.cli:main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
