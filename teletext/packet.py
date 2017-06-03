from parity import enc_odd, enc_ham_8_4, enc_ham_24_18, enc_string

def packet_header(magazine, packet_num):
	"""
	Generate a 2 byte packet header

	>>> type(packet_header(0,0))
	<type 'bytearray'>
	"""
	return \
		enc_ham_8_4( (magazine&0x07) | (packet_num&0x01)<<3 ) + \
		enc_ham_8_4( (packet_num&0x1e)>>1 )

def packet_page_header( magazine, page_num, subcode, data, \
	erase=False, \
	newsflash=False, \
	subtitle=False, \
	supress_header=False, \
	update_indicator=False, \
	interrupted_sequence=False, \
	inhibit_display=False, \
	magazine_serial=False, \
	national_option_character=0):
	"""
	Generate a page header packet

	>>> type(packet_page_header(0,0,0,""))
	<type 'bytearray'>
	>>> len(packet_page_header(0,0,0,""))
	42
	"""
	return \
		packet_header(magazine, 0) + \
		enc_ham_8_4(page_num&0x0f) + \
		enc_ham_8_4((page_num&0xf0) >> 4) + \
		enc_ham_8_4((subcode&0x000f) >> 0) + \
		enc_ham_8_4((subcode&0x0070) >> 4 | \
			(0x8 if erase else 0) \
		) + \
		enc_ham_8_4((subcode&0x0f00) >> 8) + \
		enc_ham_8_4((subcode&0x3000) >> 12 | \
			(0x4 if newsflash else 0) | \
			(0x8 if subtitle else 0) \
		) + \
		enc_ham_8_4( \
			(0x1 if supress_header else 0) | \
			(0x2 if update_indicator else 0) | \
			(0x4 if interrupted_sequence else 0) | \
			(0x8 if inhibit_display else 0) \
		) + \
		enc_ham_8_4( \
			(0x1 if magazine_serial else 0) | \
			(national_option_character&0x7) << 1 \
		) + \
		enc_string(data, 32)

def packet_direct_display( magazine, packet_num, data ):
	"""
	Generate a packet intended for direct display

	>>> type(packet_direct_display(0,0,""))
	<type 'bytearray'>
	>>> len(packet_direct_display(0,0,""))
	42
	"""
	return packet_header(magazine, packet_num) + enc_string(data, 40)
