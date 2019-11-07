import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ids-lib",
    version="0.0.4",
    author="dnk0 <Dennis Kreußel>",
    author_email="dnk0@protonmail.com",
    description="Common functionality and preprocessing for intrusion detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
