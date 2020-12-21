#!/usr/bin/env python3

from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="UTF-8") as f:
    long_description = f.read()

setup(
    name="feature-dtw",
    description="Feature DTW",
    long_description=long_description,
    author="Ondrej Kurák",
    author_email="ondrej.kurak.h@gmail.com",
    url="https://github.com/H00N24/visual-analysis-of-big-time-series-datasets",
    packages=find_packages("src"),
    package_dir={"": "src"},
    use_scm_version={"write_to": ".version", "write_to_template": "{version}\n"},
    setup_requires=["setuptools_scm"],
    install_requires=["cython", "numpy", "scikit-learn", "tslearn", "fastdtw"],
    entry_points={"console_scripts": []},
    package_data={"feature_dtw": ["py.typed"]},
    include_package_data=True,
    license="MIT",
    platforms=["platform-independent"],
)
