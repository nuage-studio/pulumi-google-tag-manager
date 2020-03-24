from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pulumi_google_tag_manager",
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nuage-studio/pulumi-google-tag-manager",
    packages=find_packages(exclude=('example')),
    python_requires='>=3.7',
    install_requires=[
        'google-api-python-client>=1.7.11',
        'pulumi>=1.8.1',
        'pulumi_aws>=1.17.0',
        'oauth2client>=4.1.3',
        'Jinja2>=2.11.1',
    ]
)