import io
import sys


def decode_imsi(imsi):
	new_imsi = ''
	for a in imsi:
		c = hex(a)
		if len(c) == 4:
			new_imsi += str(c[3])+str(c[2])
		else:
			new_imsi += str(c[2])+"0"
	mcc = new_imsi[1:4]
	mnc = new_imsi[4:6]
	newimsi = new_imsi[1:]
	return newimsi

def find_imsi(data):
		p = bytearray(data)
		tmsi1 = ""
		tmsi2 = ""
		imsi1 = ""
		imsi2 = ""
		if p[0x2] == 0x21:  # Message Type: Paging Request Type 1
			# Channel 1: TCH/F (Full rate) (2)
			if p[0x4] == 0x08 and (p[0x5] & 0x1) == 0x1:
				# Mobile Identity 1 Type: IMSI (1)
				"""
				        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
				0000   00 00 00 00 00 00 00 00 00 00 00 00 08 00 45 00
				0010   00 43 1c d4 40 00 40 11 1f d4 7f 00 00 01 7f 00
				0020   00 01 c2 e4 12 79 00 2f fe 42 02 04 01 00 00 00
				0030   c9 00 00 16 21 26 02 00 07 00 31 06 21 00 08 XX
				0040   XX XX XX XX XX XX XX 2b 2b 2b 2b 2b 2b 2b 2b 2b
				0050   2b
				XX XX XX XX XX XX XX XX = IMSI
				"""
				imsi1 = p[0x5:][:8]
				# p[0x10] == 0x59 = l2 pseudo length value: 22
				# Channel 2: TCH/F (Full rate) (2)
				if p[0x0] == 0x59 and p[0xE] == 0x08 and (p[0xF] & 0x1) == 0x1:
					# Mobile Identity 2 Type: IMSI (1)
					"""
				        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
				0000   00 00 00 00 00 00 00 00 00 00 00 00 08 00 45 00
				0010   00 43 90 95 40 00 40 11 ac 12 7f 00 00 01 7f 00
				0020   00 01 b4 1c 12 79 00 2f fe 42 02 04 01 00 00 00
				0030   c8 00 00 16 51 c6 02 00 08 00 59 06 21 00 08 YY
				0040   YY YY YY YY YY YY YY 17 08 XX XX XX XX XX XX XX
				0050   XX
				YY YY YY YY YY YY YY YY = IMSI 1
				XX XX XX XX XX XX XX XX = IMSI 2
					"""
					imsi2 = p[0xF:][:8]
					print decode_imsi(imsi1)
					print decode_imsi(imsi2)
				# Channel 2: TCH/F (Full rate) (2)
				elif p[0x0] == 0x4d and p[0xE] == 0x05 and p[0xF] == 0xf4:
					# Mobile Identity - Mobile Identity 2 - IMSI
					"""
				        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
				0000   00 00 00 00 00 00 00 00 00 00 00 00 08 00 45 00
				0010   00 43 f6 92 40 00 40 11 46 15 7f 00 00 01 7f 00
				0020   00 01 ab c1 12 79 00 2f fe 42 02 04 01 00 00 00
				0030   d8 00 00 23 3e be 02 00 05 00 4d 06 21 a0 08 YY
				0040   YY YY YY YY YY YY YY 17 05 f4 XX XX XX XX 2b 2b
				0050   2b
				YY YY YY YY YY YY YY YY = IMSI 1
				XX XX XX XX = TMSI
					"""
					tmsi1 = p[0x10:][:4]


			# Channel 2: TCH/F (Full rate) (2)
			elif p[0xB] == 0x08 and (p[0xC] & 0x1) == 0x1:
				# Mobile Identity 2 Type: IMSI (1)
				"""
				        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
				0000   00 00 00 00 00 00 00 00 00 00 00 00 08 00 45 00
				0010   00 43 57 8e 40 00 40 11 e5 19 7f 00 00 01 7f 00
				0020   00 01 99 d4 12 79 00 2f fe 42 02 04 01 00 00 00
				0030   c7 00 00 11 05 99 02 00 03 00 4d 06 21 00 05 f4
				0040   yy yy yy yy 17 08 XX XX XX XX XX XX XX XX 2b 2b
				0050   2b
				yy yy yy yy = TMSI/P-TMSI - Mobile Identity 1
				XX XX XX XX XX XX XX XX = IMSI
				"""
				tmsi1 = p[0x6:][:4]
				imsi2 = p[0xC:][:8]
				print decode_imsi(imsi2)

			# Mobile Identity - Mobile Identity 1 - TMSI/P-TMSI
			elif p[0x4] == 0x05 and (p[0x5] & 0x07) == 4:
				"""
				        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
				0000   00 00 00 00 00 00 00 00 00 00 00 00 08 00 45 00
				0010   00 43 b3 f7 40 00 40 11 88 b0 7f 00 00 01 7f 00
				0020   00 01 ce 50 12 79 00 2f fe 42 02 04 01 00 03 fd
				0030   d1 00 00 1b 03 5e 05 00 00 00 41 06 21 00 05 f4
				0040   XX XX XX XX 17 05 f4 YY YY YY YY 2b 2b 2b 2b 2b
				0050   2b
				XX XX XX XX = TMSI/P-TMSI - Mobile Identity 1
				YY YY YY YY = TMSI/P-TMSI - Mobile Identity 2
				"""
				tmsi1 = p[0x6:][:4]
				# Mobile Identity - Mobile Identity 2 - TMSI/P-TMSI
				if p[0xB] == 0x05 and (p[0xC] & 0x07) == 4:
					tmsi2 = p[0xD:][:4]
				else:
					tmsi2 = ""

				#t.register_imsi(gsm.arfcn, imsi1, imsi2, tmsi1, tmsi2, p)

		elif p[0x2] == 0x22:  # Message Type: Paging Request Type 2
			# Mobile Identity 3 Type: IMSI (1)
			if p[0xD] == 0x08 and (p[0xE] & 0x1) == 0x1:
				"""
				        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f				
				0000   00 00 00 00 00 00 00 00 00 00 00 00 08 00 45 00
				0010   00 43 1c a6 40 00 40 11 20 02 7f 00 00 01 7f 00
				0020   00 01 c2 e4 12 79 00 2f fe 42 02 04 01 00 00 00
				0030   c9 00 00 16 20 e3 02 00 04 00 55 06 22 00 yy yy
				0040   yy yy zz zz zz 4e 17 08 XX XX XX XX XX XX XX XX
				0050   8b
				yy yy yy yy = TMSI/P-TMSI - Mobile Identity 1
				zz zz zz zz = TMSI/P-TMSI - Mobile Identity 2
				XX XX XX XX XX XX XX XX = IMSI
				"""
				tmsi1 = p[0x4:][:4]
				tmsi2 = p[0x8:][:4]
				imsi2 = p[0xE:][:8]
				print decode_imsi(imsi2)

logfile = sys.argv[1]
print "Log File: " + logfile
logs = io.open(logfile, "rb")
while 1:
    find_imsi(logs.read(0x17))
logs.close()

