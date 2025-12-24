from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Ej2",
    ext_modules=cythonize("proc2_cython_mod.pyx", language_level="3", annotate=True),
)
