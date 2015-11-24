from cffi import FFI
ffi = FFI()
ffi.cdef("uint32_t sse4_crc32c(uint32_t, const char *, size_t);")
ffi.set_source("_crc32c", open('build_crc32c.c', 'r').read())

if __name__ == "__main__":
	ffi.compile()
