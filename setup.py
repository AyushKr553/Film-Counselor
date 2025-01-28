from setuptools import setup, find_packages

with open("C:/Users/KIIT01/Desktop/project/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

AUTHOR_NAME = 'Ayush Kumar'
SRC_REPO = 'src'
LIST_OF_REQUIREMENTS = ['streamlit']

setup(
    name=SRC_REPO,
    version='0.0.1',
    author=AUTHOR_NAME,
    author_email='ayushkr0535@gmail.com',
    description='A basic Python package to develop a web app that recommends films',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(where=SRC_REPO),  # Automatically finds subpackages
    package_dir={'': SRC_REPO},             # Maps the SRC_REPO folder to the root
    python_requires='>=3.7',
    install_requires=LIST_OF_REQUIREMENTS,
)
