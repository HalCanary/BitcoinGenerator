#!/usr/bin/env python
import hashlib, sys, math
'''
A single Python script to convert a passphrase into a Bitcoin address.

   Copyright 2013 Hal Canary

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
# PRIVATE: "correct horse battery staple"
# PRIVATE: 5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS
# PUBLIC:  1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T
# privkey, pubkey = getkeys("correct horse battery staple")
# assert privkey == '5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS'
# assert pubkey == '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T'

def shash(s):
	return hashlib.sha256(s).digest()
def ripe(s):
	h = hashlib.new('ripemd160')
	h.update(s)
	return h.digest()
def shex(s):
	'convert a bytestring number to hex'
	return ''.join('%02x'%ord(x) for x in s)
def stringtoint(x):
	'convert a bytestring to an integer'
	return sum(ord(c)*(0x100 ** i) for i,c in enumerate(reversed(x)))
def hextoint(s):
	'convert a hex to an integer'
	return int(s,16)
def inttohex(x):
	'convert a integer to hex'
	return '%x' % x
def inttostring(x):
	'convert an integer to a bytestring'
	def genbytes(x):
		while (x > 0):
			x, y = divmod(x, 0x100)
			yield chr(y)
	return ''.join(reversed(list(genbytes(x))))
def hextostring(s):
	'convert a hex to a bytestring '
	if len(s) % 2: s = '0' + s
	return ''.join(chr( int (s[i:i+2], 16 ) ) for i in range(0, len(s), 2))
def addcheck(s):
	s1 = chr(0x80) + s
	return s1 + shash(shash(s1))[:4]
def pubcheck(s):
	s1 = chr(0x00) + ripe(shash(s))
	return s1 + shash(shash(s1))[:4]
def encode(s):
	num = stringtoint(s)
	alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	base_count = len(alphabet)
	encode = ''
	if (num < 0):
		return ''
	while (num > 0):
		num, mod = divmod(num, base_count)
		encode = alphabet[mod] + encode
	if s[0] == chr(0x00):
		encode = alphabet[0] + encode
	return encode
def decode(s):
	alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	alphadict = dict((x,i) for i,x in enumerate(alphabet))
	base = len(alphabet)
	return sum(alphadict[c] * (base ** i) for i,c in enumerate(reversed(s)))
def ExtendedEuclidian(a,b):
	if b == 0:
		return (a,1,0)
	x2, x1, y2, y1 = 1, 0, 0, 1
	while b > 0:
		q, r = divmod(a, b)
		a, b, x2, x1, y2, y1 = b, r, x1, x2 - (q * x1), y1, y2 - (q * y1)
	return (a,x2,y2)
def invert(a):
	p =  int('ffffffffffffffffffffffffffffffff'
			 'fffffffffffffffffffffffefffffc2f',16)
	d,x,y = ExtendedEuclidian(a,p)
	assert d == 1
	return x
def ecdouble(P):
	p =  int('ffffffffffffffffffffffffffffffff'
			 'fffffffffffffffffffffffefffffc2f',16)
	x,y = P
	la = (3 * (x**2)) * invert(2 * y)
	xr = ((la ** 2) - (2 * x)) % p
	return (xr, ((la * (x - xr)) - y) % p)
def ecadd(P,Q):
	p =  int('ffffffffffffffffffffffffffffffff'
			 'fffffffffffffffffffffffefffffc2f',16)
	if P is None:
		return Q
	(xp,yp), (xq,yq) = P, Q
	la = (yq - yp) *  invert(xq - xp)
	xr = (la**2 - xp - xq) % p
	return (xr, (la * (xp - xr) - yp) % p)
def ecmul(x):
	Gx = int('79BE667EF9DCBBAC55A06295CE870B07'
			 '029BFCDB2DCE28D959F2815B16F81798',16)
	Gy = int('483ADA7726A3C4655DA4FBFC0E1108A8'
			 'FD17B448A68554199C47D08FFB10D4B8',16)
	Q = None
	m = int(math.log(x, 2)) + 1
	for i in xrange(m - 1, -1, -1):
		if Q is not None:
			Q = ecdouble(Q)
		if (x >> i) & 1 == 1:
			Q = ecadd(Q,(Gx,Gy))
	return Q
def PrivateKeyToPublicKey(privkey):
	x,y = ecmul(stringtoint(privkey))
	return chr(0x04) + inttostring(x) + inttostring(y)
def CheckPrivateKey(key):
	n = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
			'EBAAEDCE6AF48A03BBFD25E8CD0364141',16)
	return key > n
def getkeys(phrase):
	privkey = shash(phrase)
	assert CheckPrivateKey(privkey)
	pubkey = PrivateKeyToPublicKey(privkey)
	return (encode(addcheck(privkey)), encode(pubcheck(pubkey)))
if __name__ == '__main__':
	phrase = sys.stdin.read()
	print 'private phrase', repr(phrase)
	privkey, pubkey = getkeys(phrase)
	print 'private key', privkey
	print 'public key', pubkey

