import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opylib",
    version="0.0.1",
    author="c-git",
    author_email="one.bgz1@gmail.com",
    description="My frequently used classes and functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/c-git/opylib",
    project_urls={
        "Bug Tracker": "https://github.com/c-git/opylib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
