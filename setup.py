import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="honeybee-schema",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Ladybug Tools",
    author_email="info@ladybug.tools",
    description="Honeybee Data-Model Objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ladybug-tools-in2/honeybee-schema",
    packages=setuptools.find_packages(exclude=["tests", "scripts", "samples"]),
    install_requires=requirements,
    include_package_data=True,
    extras_require={
        'cli': ['click>=7.1.2']
    },
    entry_points={
        "console_scripts": ["honeybee-schema = honeybee_schema.cli:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent"
    ],
    license="BSD-3-Clause"
)
