from setuptools import setup, find_packages

setup(
    name="wvvortex",
    version="1.0.0",
    description="WVVortex - Web Vulnerability Scanner",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm",
        "colorama",
        "beautifulsoup4",
        "reportlab"
    ],
    entry_points={
        "console_scripts": [
            "wvvortex=wvvortex.scanner:main",
        ],
    },
)