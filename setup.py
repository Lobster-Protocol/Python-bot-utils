"""Python-bot-utils-Lobster package setup."""

from setuptools import find_packages, setup

setup(
    name="python_bot_utils",
    version="0.1.0",
    description="Python-bot-utils-Lobster package",
    author="Elli610",
    author_email="nathan@lobster-protocol.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pytest>=8.3.5",
        "web3==7.11.1",
        "eth-abi==5.2.0",
    ],
    extras_require={
        "dev": [],
        "test": [],
    },
)
