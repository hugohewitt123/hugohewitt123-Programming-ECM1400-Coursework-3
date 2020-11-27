import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecm1400-coursework3-pkg-hhewitt",
    version="0.0.1",
    author="Hugo Hewitt",
    author_email="hh538@exeter.ac.uk",
    description="An alarm system that gives updates on covid stats, news and weather",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hugohewitt123/Programming-ECM1400-Coursework-3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)