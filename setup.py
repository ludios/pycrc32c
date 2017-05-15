#!/usr/bin/env python

import os
import sys
from distutils.core import setup
from distutils.extension import Extension

import build_crc32c

os.environ['CFLAGS'] = " ".join(["-O3", "-march=native", "-Wall"])

setup(
	name='pycrc32c',
	version='1.0.0',
	description="crc32c for Python; uses the Intel CRC32 instruction and thus requires SSE4.2",
	url="https://github.com/ludios/pycrc32c",
	author="Ivan Kozik",
	author_email="ivan@ludios.org",
	classifiers=[
		'Development Status :: 4 - Beta',
		'Operating System :: POSIX :: Linux',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
	],
	py_modules=['crc32c'],
	ext_modules=[build_crc32c.ffibuilder.distutils_extension()]
)
