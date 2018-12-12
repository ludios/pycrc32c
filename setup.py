#!/usr/bin/env python3

import os
import sys
from setuptools import setup

os.environ["CFLAGS"] = " ".join(["-O3", "-msse4.2", "-Wall"])

setup(
	name="pycrc32c",
	version="2.0.2",
	description="crc32c for Python; uses the Intel CRC32 instruction and thus requires SSE4.2",
	url="https://github.com/ludios/pycrc32c",
	author="Ivan Kozik",
	author_email="ivan@ludios.org",
	classifiers=[
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
		"Development Status :: 5 - Production/Stable",
		"Operating System :: POSIX :: Linux",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
	],
	py_modules=["crc32c"],
	setup_requires=["cffi"],
	cffi_modules=["build_crc32c.py:ffibuilder"],
	install_requires=["cffi"]
)
