#!/usr/bin/env python
"""
   BitcoinGenerator/MultiKey.py
   Copyright 2013 Hal Canary

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       LICENSE.md in this repository.
       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import random, sys, hashlib, math
from BitcoinGenerator import *

def MiniPrivateKeys(num):
	while True:
		encoded = Sencode(num)
		if hashlib.sha256(encoded + '?').digest()[0] == chr(0x00):
			yield encoded
		num = (num + 1) % (58 ** 29)

def Sencode(num):
	encode = ''
	alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	base_count = len(alphabet)
	while (num > 0):
		num, mod = divmod(num, base_count)
		encode = alphabet[mod] + encode
	return 'S' + encode

def pull(generator, n=1):
	for i in xrange(n):
		yield generator.next()

def search(start, searchkey):
	"""
	Given a secret "startkey" and a public "searchkey", return the
	private key that corresponds to the public searchkey.  Do not give
	out the "private phrase" that is returned.  It is, however, safe
	to use the private key (since sha256 is probably safe).
	"""
	for key in MiniPrivateKeys(decode(start)):
		privkey, pubkey = getkeys(key)
		if pubkey == searchkey:
			print 'private phrase', repr(key)
			print 'private key', privkey
			print 'public key', pubkey
			return

def getKeyList(mpk, N):
	for x in pull(MiniPrivateKeys(decode(mpk)), N):
		privkey, pubkey = getkeys(x)
		print pubkey

useage = """
Example use:
  $ ./MultiKey.py S2111111111111111111111111113K 3
  13TyXm5APvzZcZ6auNN1djqN1FmckjWJrW
  1NViw273yHurD7eN2WrbLw3pd3gqU5cjbh
  1K3Tax3frx9xr8WQL9ewJbq3m7cgFdMzWC

  $ ./MultiKey.py S2111111111111111111111111113K \\
             1K3Tax3frx9xr8WQL9ewJbq3m7cgFdMzWC
  private phrase 'S211111111111111111111111111EG'
  private key 5JUWsvLHVRxs5LRxCLeHACuKUpNV6StFygQGhAwWJNih6EQm6qg
  public key 1K3Tax3frx9xr8WQL9ewJbq3m7cgFdMzWC
"""
if __name__ == '__main__':
	if len(sys.argv) < 3:
		print useage
		exit(1)
	if len(sys.argv[2]) > 7:
		search(sys.argv[1], sys.argv[2])
	else:
		getKeyList(sys.argv[1], int(sys.argv[2]))
