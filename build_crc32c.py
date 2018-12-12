#!/usr/bin/env python3

from cffi import FFI
ffibuilder = FFI()
ffibuilder.cdef("uint32_t sse4_crc32c(uint32_t, const char *, size_t);")
ffibuilder.set_source("_crc32c", open('build_crc32c.c', 'r').read())

if __name__ == "__main__":
	ffibuilder.compile()
