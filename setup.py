# python3 imports
from setuptools import setup, find_packages

# project imports
import wintersdeep_postcode

# read in the project README.md file for the long description
with open("README.md", "r") as file_handle:
    long_description_md = file_handle.read()

# setup this project.
setup(
    name="wintersdeep_postcode",
    version=wintersdeep_postcode.__version__,
    author=wintersdeep_postcode.__author__,
    author_email=wintersdeep_postcode.__email__,
    description="Python3.6+ library for working with British postcodes.",
    long_description=long_description_md,
    long_description_content_type="text/markdown",
    url="https://www.github.com/wintersdeep/wintersdeep_postcode",
    packages=find_packages(),
    include_package_data=True,
    classifiers= [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)

