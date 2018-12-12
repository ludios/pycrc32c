#!/usr/bin/env python3

from __future__ import print_function

import crc32c
import random

'''
Test vectors copied from https://github.com/edmonds/mtbl/blob/master/src/test-crc32c.c

Copyright (c) 2012 by Internet Systems Consortium, Inc. ("ISC")

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL ISC BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

test_vectors = [
	{"text": b"",
	"value": 0x00000000},

	{"text": b"\x61",
	"value": 0xc1d04330},

	{"text": b"\x66\x6f\x6f",
	"value": 0xcfc4ae1d},

	{"text": b"\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64",
	"value": 0xc99465aa},

	{"text": b"\x68\x65\x6c\x6c\x6f\x20",
	"value": 0x7e627e58},

	{"text": b"\x00\x00\x00\x00\x00\x00\x00\x00"
			b"\x00\x00\x00\x00\x00\x00\x00\x00"
			b"\x00\x00\x00\x00\x00\x00\x00\x00"
			b"\x00\x00\x00\x00\x00\x00\x00\x00",
	"value": 0x8a9136aa},

	{"text": b"\xff\xff\xff\xff\xff\xff\xff\xff"
			b"\xff\xff\xff\xff\xff\xff\xff\xff"
			b"\xff\xff\xff\xff\xff\xff\xff\xff"
			b"\xff\xff\xff\xff\xff\xff\xff\xff",
	"value": 0x62a8ab43},

	{"text": b"\x1f\x1e\x1d\x1c\x1b\x1a\x19\x18"
			b"\x17\x16\x15\x14\x13\x12\x11\x10"
			b"\x0f\x0e\x0d\x0c\x0b\x0a\x09\x08"
			b"\x07\x06\x05\x04\x03\x02\x01\x00",
	"value": 0x113fdb5c},

	{"text": b"\x01\xc0\x00\x00\x00\x00\x00\x00"
			b"\x00\x00\x00\x00\x00\x00\x00\x00"
			b"\x14\x00\x00\x00\x00\x00\x04\x00"
			b"\x00\x00\x00\x14\x00\x00\x00\x18"
			b"\x28\x00\x00\x00\x00\x00\x00\x00"
			b"\x02\x00\x00\x00\x00\x00\x00\x00",
	"value": 0xd9963a56},

	{"text": b"\x00\x01\x02\x03\x04\x05\x06\x07"
			b"\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
			b"\x10\x11\x12\x13\x14\x15\x16\x17"
			b"\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f",
	"value": 0x46dd794e},

	{"text": b"\x01\x02\x03\x04\x05\x06\x07\x08"
			b"\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
			b"\x11\x12\x13\x14\x15\x16\x17\x18"
			b"\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
			b"\x21\x22\x23\x24\x25\x26\x27\x28",
	"value": 0x0e2c157f},

	{"text": b"\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
			b"\x31\x32\x33\x34\x35\x36\x37\x38"
			b"\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
			b"\x41\x42\x43\x44\x45\x46\x47\x48"
			b"\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50",
	"value": 0xe980ebf6},

	{"text": b"\x51\x52\x53\x54\x55\x56\x57\x58"
			b"\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
			b"\x61\x62\x63\x64\x65\x66\x67\x68"
			b"\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
			b"\x71\x72\x73\x74\x75\x76\x77\x78",
	"value": 0xde74bded},

	{"text": b"\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
			b"\x81\x82\x83\x84\x85\x86\x87\x88"
			b"\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
			b"\x91\x92\x93\x94\x95\x96\x97\x98"
			b"\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0",
	"value": 0xd579c862},

	{"text": b"\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8"
			b"\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
			b"\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8"
			b"\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
			b"\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8",
	"value": 0xba979ad0},

	{"text": b"\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
			b"\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8"
			b"\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
			b"\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8"
			b"\xe9\xea\xeb\xec\xed\xee\xef\xf0",
	"value": 0x2b29d913},

	{"text": b"\x01\x02\x03\x04\x05\x06\x07\x08"
			b"\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
			b"\x11\x12\x13\x14\x15\x16\x17\x18"
			b"\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
			b"\x21\x22\x23\x24\x25\x26\x27\x28"
			b"\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
			b"\x31\x32\x33\x34\x35\x36\x37\x38"
			b"\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
			b"\x41\x42\x43\x44\x45\x46\x47\x48"
			b"\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
			b"\x51\x52\x53\x54\x55\x56\x57\x58"
			b"\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
			b"\x61\x62\x63\x64\x65\x66\x67\x68"
			b"\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
			b"\x71\x72\x73\x74\x75\x76\x77\x78"
			b"\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
			b"\x81\x82\x83\x84\x85\x86\x87\x88"
			b"\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
			b"\x91\x92\x93\x94\x95\x96\x97\x98"
			b"\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
			b"\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8"
			b"\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
			b"\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8"
			b"\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
			b"\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8"
			b"\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
			b"\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8"
			b"\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
			b"\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8"
			b"\xe9\xea\xeb\xec\xed\xee\xef\xf0",
	"value": 0x24c5d375},
]

def chunk_string(string, length):
	return (string[0+i:length+i] for i in range(0, len(string), length))


for v in test_vectors:
	c = crc32c.sse4_crc32c(0, v["text"])
	assert c == v["value"], c

	# Test with multiple calls
	chunks = list(chunk_string(v["text"], random.randint(1, 11)))
	c = 0
	for chunk in chunks:
		c = crc32c.sse4_crc32c(c, chunk)
	assert c == v["value"], c


print("OK")
