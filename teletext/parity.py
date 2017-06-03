def genpar(bits):
	"""
	Count all the bits in a number, and return 1 if the number of bits set is odd, 0 if it's even

	>>> genpar( 0b00000000 )
	0
	>>> genpar( 0b00000001 )
	1
	>>> genpar( 0b00100000 )
	1
	>>> genpar( 0b10101010 )
	0
	>>> genpar( 0b00111110 )
	1
	"""
	par = 0
	while bits:
		par ^= bits & 1
		bits >>= 1
	return par

def enc_odd(bits):
	"""
	Generate a vector of one byte contianing the bits 0-6 from input byte, and bit 7 to generate odd parity

	>>> type(enc_odd(0))
	<type 'bytearray'>
	>>> list(enc_odd( 0b00000000 ))
	[128]
	>>> list(enc_odd( 0b00010000 ))
	[16]
	>>> list(enc_odd( 0b01010101 ))
	[213]
	>>> list(enc_odd( 0b10010000 ))
	[16]
	"""
	bits &= 0b01111111
	if not genpar(bits):
		bits |= 0b10000000
	return bytearray([ bits ])
		

def enc_ham_8_4(bits):
	"""
	Generate hamming 8/4 code of input bits 0-3, outputted as an array of one byte

	>>> type(enc_ham_8_4(0))
	<type 'bytearray'>
	>>> [enc_ham_8_4(i)[0]&0xaa for i in range(16)]
	[0, 2, 8, 10, 32, 34, 40, 42, 128, 130, 136, 138, 160, 162, 168, 170]
	>>> [enc_ham_8_4(i)[0] for i in range(16)]
	[21, 2, 73, 94, 100, 115, 56, 47, 208, 199, 140, 155, 161, 182, 253, 234]
	>>> list(enc_ham_8_4(0))
	[21]
	>>> list(enc_ham_8_4(1))
	[2]
	>>> list(enc_ham_8_4(15))
	[234]
	"""
	# Generate table that can be generated parity out of
	bits = ((bits&0x01)<<1) | ((bits&0x02)<<2) | ((bits&0x04)<<3) | ((bits&0x08)<<4)
	bits |= 0x01 if not genpar(bits & 0b10100010) else 0
	bits |= 0x04 if not genpar(bits & 0b10001010) else 0
	bits |= 0x10 if not genpar(bits & 0b00101010) else 0
	bits |= 0x40 if not genpar(bits & 0b10111111) else 0
	return bytearray([ bits ])

def enc_ham_24_18(bits):
	"""
	Generate hamming 24/18 code

	Some example values
	>>> type(enc_ham_24_18(0))
	<type 'bytearray'>
	>>> list(enc_ham_24_18(0))
	[139, 128, 0]
	>>> list(enc_ham_24_18(0x3ffff))
	[116, 127, 255]
	>>> list(enc_ham_24_18(1))
	[140, 128, 128]
	"""
	bits |= 0b1000000000000000000
	bytes = [
		(genpar(bits&0b1101010110101011011)<<0) |
		(genpar(bits&0b1110011011001101101)<<1) |
		(genpar(bits&0b0000000000000000001)<<2) |
		(genpar(bits&0b1111100011110001110)<<3) |
		(genpar(bits&0b0000000000000000010)<<4) |
		(genpar(bits&0b0000000000000000100)<<5) |
		(genpar(bits&0b0000000000000001000)<<6) |
		(genpar(bits&0b1000000011111110000)<<7),
		(genpar(bits&0b0000000000000010000)<<0) |
		(genpar(bits&0b0000000000000100000)<<1) |
		(genpar(bits&0b0000000000001000000)<<2) |
		(genpar(bits&0b0000000000010000000)<<3) |
		(genpar(bits&0b0000000000100000000)<<4) |
		(genpar(bits&0b0000000001000000000)<<5) |
		(genpar(bits&0b0000000010000000000)<<6) |
		(genpar(bits&0b1111111100000000000)<<7),
		(genpar(bits&0b0000000100000000000)<<0) |
		(genpar(bits&0b0000001000000000000)<<1) |
		(genpar(bits&0b0000010000000000000)<<2) |
		(genpar(bits&0b0000100000000000000)<<3) |
		(genpar(bits&0b0001000000000000000)<<4) |
		(genpar(bits&0b0010000000000000000)<<5) |
		(genpar(bits&0b0100000000000000000)<<6)
	]
	bytes[2] |= (1 ^ genpar(bytes[0]) ^ genpar(bytes[1]) ^ genpar(bytes[2])) << 7
	return bytearray(bytes)

def enc_string(string, length):
	"""
	Pack a string to a set of bytes, guaranteed length, odd parity added.
	Strings to long is truncated, strings to short is padded with space

	>>> type(enc_string("", 1))
	<type 'bytearray'>
	>>> list(enc_string("hej", 5))
	[104, 229, 234, 32, 32]
	>>> list(enc_string("badboll", 2))
	[98, 97]
	"""
	bytes = bytearray()
	for c in string:
		bytes += enc_odd(ord(c))
	while len(bytes) < length:
		bytes += enc_odd(ord(' '))
	return bytes[0:length]
