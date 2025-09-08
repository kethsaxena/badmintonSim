from setuptools import setup, find_packages

setup(
    name="simengine",                 # install name
    version="0.1.0",
    description="Simulation engine utilities",
    packages=find_packages(where="src"),   # discover packages under src/
    package_dir={"": "src"},               # map package root to src
    python_requires=">=3.9",
    install_requires=[
        # "numpy>=1.26",   # add if you have deps
    ],
    include_package_data=True,
)
