from setuptools import find_packages, setup


def get_readme_content():
    with open("README.md", "r") as readme_file:
        return readme_file.read()


setup(
    name="lines-counter",
    author="LineCounters - UADY",
    description="A logical & physical lines counter for Python files",
    long_description=get_readme_content(),
    long_description_content_type="text/markdown",
    version="1.0.2",
    packages=find_packages(),
    url="https://github.com/LineCounters/LinesCounter",
)
