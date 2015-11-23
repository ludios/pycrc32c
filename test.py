import crc32c

assert crc32c.sse4_crc32c(0, 'SSE4-CRC32: A hardware accelerated CRC32 implementation for node.js') == 3039989317
assert crc32c.sse4_crc32c(crc32c.sse4_crc32c(0, 'SSE4-CRC32: A hardware accelerated'), ' CRC32 implementation for node.js') == 3039989317

print "OK"
