import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

dependency_links = []
for req in requirements:
    if req.startswith('git+'):
        dependency_links.append(req)
        requirements.remove(req)

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
    dependency_links=dependency_links,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent"
    ],
)
