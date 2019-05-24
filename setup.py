import setuptools

long_description = """
#qucs2gerber Package

Installation:

**python3 -m pip install --user qucs2gerber**

Usage:

**python3 -m qucs2gerber**

Project Website:

[qucs2gerber GitHub Project](https://github.com/rccarroll654/qucs2gerber)
"""

setuptools.setup(
    name="qucs2gerber",
    version="0.0.3",
    author="Russell Carroll",
    author_email="russell_carroll@carrelec.com",
    description="A Qucs to Gerber generation tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rccarroll654/qucs2gerber",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
