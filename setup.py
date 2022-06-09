from setuptools import setup, find_packages
from twave_client import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="twave-api-client",
    version=__version__,
    description="TWave API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twave-io/twave-api-client",
    packages=find_packages(),
    install_requires=['requests', 'numpy'],
    python_requires='>3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
