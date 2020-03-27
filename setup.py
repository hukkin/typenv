from os import path

from setuptools import setup

EXTRAS_REQUIRE = {
    "tests": ["pytest", "pytest-cov", "pytest-mock"],
    "lint": ["isort", "black", "flake8", "flake8-bugbear", "mypy", "docformatter", "pre-commit"],
    "tools": ["codecov", "bump2version"],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"] + EXTRAS_REQUIRE["tools"]


def read(file_name: str) -> str:
    """Helper to read README."""
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, file_name), encoding="utf-8") as f:
        return f.read()


setup(
    name="typenv",
    version="0.1.0",  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT
    author="hukkinj1",
    author_email="hukkinj1@users.noreply.github.com",
    description="Typed environment variable parsing for Python",
    url="https://github.com/hukkinj1/typenv",
    project_urls={"Changelog": "https://github.com/hukkinj1/typenv/blob/master/CHANGELOG.md"},
    packages=["typenv"],
    package_data={"typenv": ["py.typed"]},
    zip_safe=False,  # For mypy to be able to find the installed package
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=["python-dotenv>=0.10.3,<0.13.0"],
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.6",
    keywords="environment variables typed configuration",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
)
