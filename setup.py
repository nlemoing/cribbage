from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cribbage",
    version="0.0.1",
    author="Nick Lemoing",
    author_email="nlemoing@uwaterloo.ca",
    description="Play, simulate and analyze cribbage games and strategies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nlemoing/cribbage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        "console_scripts": ["cribbage=cribbage.main:main"]
    }
)