import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raph-compare-df",
    version="0.2.0",
    author="Raphael Bürki",
    author_email="r2d4@bluewin.ch",
    description="An App to Compare Data from the Command Line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rbuerki/compare_data_from_the_command_line/",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    entry_points={"console_scripts": ["compare_df = compare_df.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["pandas", "xlsxwriter"],
)
