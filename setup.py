import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="zip3",
    version="1.0.1",
    description="A package to create a ZIP archive of all your files on S3",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/marcotroisi/zip3",
    author="Marco Troisi",
    author_email="hello@marcotroisi.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["zip3"],
    install_requires=["boto3"],
)