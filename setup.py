import os
import setuptools

from src.compare_df import __version__ as version

readme = os.path.join(os.path.dirname(__file__), "README.md")
with open(readme, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raph-compare-df",
    version=version,
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
