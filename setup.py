import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fbgs",
    version="1.0.0",
    description="Python and selenium based (mobile) Facebook groups scraper, independent of obfuscated css selectors.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lesander/facebook-group-scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
