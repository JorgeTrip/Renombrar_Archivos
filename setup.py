from setuptools import setup, find_packages

setup(
    name="renombrar",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "renombrar=renombrar.main:main",
        ],
    },
    author="JOT",
    description="Herramienta para renombrar archivos de fotos y videos",
    python_requires=">=3.6",
) 