from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bloomberg-python-interview",
    version="1.0.0",
    author="Bloomberg Engineering Interview Team",
    description="Bloomberg Python Technical Interview Practice Problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pytest>=6.2.0",
        "sortedcontainers>=2.4.0",
        "matplotlib>=3.3.0",
        "pandas>=1.3.0",
        "pytest-cov>=4.0.0",
    ],
    extras_require={
        "dev": [
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=0.950",
            "flake8>=4.0.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Software Development :: Testing",
    ],
)