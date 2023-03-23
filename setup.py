from setuptools import setup, find_packages

setup(
    name="azmdlog",
    version="0.1.0",
    author="Karsten Eckhardt",
    author_email="karsten.eckhardt@gmail.com",
    description="Azure Monitor Custom Logger for Databricks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/r4h4/cldx",
    packages=find_packages(),
    package_dir={"azmdlog": "azmdlog"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
    tests_require=[
        "pytest",
    ],
)
