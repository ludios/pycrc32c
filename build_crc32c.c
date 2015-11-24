/*
The code below was copied from
https://github.com/Voxer/sse4_crc32/blob/master/src/crc32c_sse42.cpp

The MIT License (MIT)

Copyright (c) 2013-2015 Anand Suresh

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

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
