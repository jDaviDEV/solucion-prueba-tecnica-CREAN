from setuptools import setup, find_packages

setup(
    name="solucion",
    version="1.0.0",
    description="Propuesta para la prueba técnica de la vacante Analítico I CREAN",
    author="Juan David Correa Franco",

    package_dir={"": "src"},
    packages=find_packages(where="src"),

    python_requires=">=3.9.12",

    install_requires=[
        "pandas",
        "pyodbc",
        "numpy",
        "matplotlib",
        "scikit-learn"
    ],
)