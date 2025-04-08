from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "chatbot",  # Not "chatbot_bindings"
        ["chatbot.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
    )
]

setup(
    name="chatbot",
    ext_modules=ext_modules,
)

