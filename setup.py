"""Setup configuration for create-fastapi-boilerplate."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="create-fastapi-boilerplate",
    version="1.0.0",
    author="Parth Joshi",
    author_email="parthjoshi.1618@gmail.com",
    description="Production-grade FastAPI project generator with enterprise features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parth1618/fastapi-boilerplate",
    project_urls={
        "Bug Tracker": "https://github.com/parth1618/fastapi-boilerplate/issues",
        "Documentation": "https://github.com/parth1618/fastapi-boilerplate#readme",
        "Source Code": "https://github.com/parth1618/fastapi-boilerplate",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No runtime dependencies needed - just uses git
    ],
    entry_points={
        "console_scripts": [
            "create-fastapi-boilerplate=create_fastapi_boilerplate.cli:main",
        ],
    },
    keywords="fastapi boilerplate template generator cli project-generator",
    include_package_data=True,
    zip_safe=False,
)