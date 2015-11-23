import sys
from _crc32c.lib import sse4_crc32c
from cffi import FFI
ffi = FFI()

def crc32c_for_file(f, block_size=64*1024):
	assert block_size >= 1, "block_size must be >= 1, was %r" % (block_size,)
	mem = ffi.new('char[%d]' % block_size)
	arr = ffi.buffer(mem)
	c = 0
	while True:
		num_bytes_read = f.readinto(arr)
		if not num_bytes_read:
			break
		c = sse4_crc32c(c, mem, num_bytes_read)
	return c


if __name__ == '__main__':
	print crc32c_for_file(sys.stdin)
