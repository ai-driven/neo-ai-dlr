import os
from setuptools import setup, find_packages
from subprocess import check_output
from setuptools.dist import Distribution
from platform import system

data_files = []
for path, dirnames, filenames in os.walk('python'):
    for filename in filenames:
        data_files.append(os.path.join(path, filename))

# Use libpath.py to locate libdlr.so
LIBPATH_PY = os.path.abspath('./dlr/libpath.py')
LIBPATH = {'__file__': LIBPATH_PY}
exec(compile(open(LIBPATH_PY, "rb").read(), LIBPATH_PY, 'exec'),
     LIBPATH, LIBPATH)
LIB_PATH = LIBPATH['find_lib_path']()

LIB_PATH = []
CURRENT_DIR = os.path.dirname(__file__)
for libfile in LIBPATH['find_lib_path']():
    try:
        relpath = os.path.relpath(libfile, CURRENT_DIR)
        LIB_PATH.append(relpath)
        break  # need only one
    except ValueError:
        continue

if not LIB_PATH:
    raise RuntimeError('libdlr.so missing. Please compile first using CMake')

setup(
    name="dlr",
    version="1.0",

    zip_safe=False,
    install_requires=['numpy', 'decorator'],

    # declare your packages
    packages=find_packages(),

    # include data files
    include_package_data=True,
    data_files=[('dlr', LIB_PATH)],
)
