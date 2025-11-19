from setuptools import setup, find_packages

setup(
    name="grant-scholar-survival-kitchen",
    version="1.0.0",
    author="Xander-Lucien",
    description="A survival simulation game built with pygame",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Xander-Lucien/GrantScholarSurvivalKitchen",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["data/*.json"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Simulation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "grant-scholar=main:main",
        ],
    },
)
