# file "example_build.py"

from cffi import FFI
ffi = FFI()

ffi.cdef("uint32_t sse4_crc32c(uint32_t, const char *, size_t);")

# C code copied from https://github.com/Voxer/sse4_crc32/blob/master/src/crc32c_sse42.cpp
ffi.set_source("crc32c",
"""
	#include <nmmintrin.h>

	// Byte-boundary alignment issues
	#define ALIGN_SIZE 0x08UL // Align at an 8-byte boundary
	#define ALIGN_MASK (ALIGN_SIZE - 1) // Bitmask for 8-byte bound addresses

	// Performs H/W CRC operations
	#define CALC_CRC(op, crc, type, buf, len) \
		do { \
			for (; (len) >= sizeof(type); (len) -= sizeof(type), buf += sizeof(type)) { \
				(crc) = op((crc), *(type *) (buf)); \
			} \
		} while(0)

	/**
	 * Calculates CRC-32C using hardware support
	 *
	 * @param initial_crc The initial CRC to use for the operation
	 * @param buf The buffer that stores the data whose CRC is to be calculated
	 * @param len The size of the buffer
	 * @return The CRC-32C of the data in the buffer
	 */
	static uint32_t sse4_crc32c(uint32_t initial_crc, const char *buf, size_t len) {
		uint32_t crc = initial_crc;

		// If the string is empty, return the initial crc
		if (len == 0) return crc;

		// XOR the initial CRC with INT_MAX
		crc ^= 0xFFFFFFFF;

		// Align the input to the word boundary
		for (; (len > 0) && ((size_t)buf & ALIGN_MASK); len--, buf++) {
			crc = _mm_crc32_u8(crc, *buf);
		}

		// Blast off the CRC32 calculation on hardware
	#if defined(__x86_64__) || defined(_M_X64)
		CALC_CRC(_mm_crc32_u64, crc, uint64_t, buf, len);
	#endif
		CALC_CRC(_mm_crc32_u32, crc, uint32_t, buf, len);
		CALC_CRC(_mm_crc32_u16, crc, uint16_t, buf, len);
		CALC_CRC(_mm_crc32_u8, crc, uint8_t, buf, len);

		// XOR again with INT_MAX
		return (crc ^= 0xFFFFFFFF);
	}
""")

if __name__ == "__main__":
	ffi.compile()
