from setuptools import setup, find_packages

setup(
    name="ptcgp",
    version="0.1.2",
    url="https://github.com/fredericojordan/ptcgp.git",
    author="Frederico Jordan",
    author_email="fredericojordan@gmail.com",
    description="Pokémon TCG Pocket Explorer App",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "dash",
        "dash_mantine_components",
        "pydantic",
        "requests",
    ],
)
