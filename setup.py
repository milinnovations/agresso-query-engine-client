import re
from codecs import open
from os import path
from setuptools import setup

# Get the long description from the README file.
with open(path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
    readme = f.read()

# Get version from the main project file.
with open(path.join(path.abspath(path.dirname(__file__)), "agresso_query_engine_client.py"), encoding="utf-8") as f:
    match = re.search('__version__ = "(.*?)"', f.read())
    version = match.group(1) if match else "0.0.0"

# Requirements.
requirements = [
    "requests",
]

setup(
    name="agresso-query-engine-client",
    version=version,
    description="Python client for Agresso query engine service.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/milinnovations/agresso-query-engine-client",
    author="Peter Volf",
    author_email="do.volfp@gmail.com",
    license="MIT",
    classifiers=[],
    keywords="Unit4 Agresso query-engine SOAP",
    py_modules=["agresso_query_engine_client"],
    python_requires=">=3.7",
    install_requires=requirements,
)
