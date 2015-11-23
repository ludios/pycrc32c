from _crc32c.lib import sse4_crc32c as _sse4_crc32c

def sse4_crc32c(initial_crc, s):
	return _sse4_crc32c(initial_crc, s, len(s))
