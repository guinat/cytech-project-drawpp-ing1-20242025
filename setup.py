from setuptools import setup, find_packages

setup(
    name="drawpp-compiler",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'drawpp=compiler.compiler:main',
            'drawpp-ide=ide.main:main',
        ],
    },
)