from .parity import *
from .settings import *

def packet_header(packet_num, **settings):
	"""
	Generate a 2 byte packet header

	>>> type(packet_header(0, page_num=0))
	<type 'bytearray'>
	"""
	magazine = (settings["page_num"] & 0x700) >> 8
	page_num = settings["page_num"] & 0xff
	return \
		enc_ham_8_4( magazine | (packet_num&0x01)<<3 ) + \
		enc_ham_8_4( (packet_num&0x1e)>>1 )

def packet_page_header( data, **settings ):
	"""
	Generate a page header packet

	>>> type(packet_page_header("", page_num=0, sub_code=0))
	<type 'bytearray'>
	>>> len(packet_page_header("", page_num=0, sub_code=0))
	42
	"""
	settings = defaults(settings,
			erase=False,
			newsflash=False,
			subtitle=False,
			supress_header=False,
			update_indicator=False,
			interrupted_sequence=False,
			inhibit_display=False,
			magazine_serial=False,
			national_option_character=0
	)
	return \
		packet_header(0, **settings) + \
		enc_ham_8_4(settings['page_num']&0x0f) + \
		enc_ham_8_4((settings['page_num']&0xf0) >> 4) + \
		enc_ham_8_4((settings["sub_code"]&0x000f) >> 0) + \
		enc_ham_8_4((settings["sub_code"]&0x0070) >> 4 | \
			(0x8 if settings["erase"] else 0) \
		) + \
		enc_ham_8_4((settings["sub_code"]&0x0f00) >> 8) + \
		enc_ham_8_4((settings["sub_code"]&0x3000) >> 12 | \
			(0x4 if settings["newsflash"] else 0) | \
			(0x8 if settings["subtitle"] else 0) \
		) + \
		enc_ham_8_4( \
			(0x1 if settings["supress_header"] else 0) | \
			(0x2 if settings["update_indicator"] else 0) | \
			(0x4 if settings["interrupted_sequence"] else 0) | \
			(0x8 if settings["inhibit_display"] else 0) \
		) + \
		enc_ham_8_4( \
			(0x1 if settings["magazine_serial"] else 0) | \
			(settings["national_option_character"]&0x7) << 1 \
		) + \
		enc_string(data, 32)

def packet_direct_display( packet_num, data, **settings ):
	"""
	Generate a packet intended for direct display

	>>> type(packet_direct_display(0,""))
	<type 'bytearray'>
	>>> len(packet_direct_display(0,""))
	42
	"""
	return packet_header(packet_num, **settings) + enc_string(data, 40)
