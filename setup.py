import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyanalysis",  # Replace with your own username
    version="version='0.0.1'",
    author="tk",
    author_email="",
    description="A package to retrieve data and store it in S3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tkeech1/pyanalysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["pyanalysis-retriever = pyanalysis.retriever:say_hi"]
    },
    python_requires=">=3.6",
)
