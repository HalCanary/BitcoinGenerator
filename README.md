
BitcoinGenerator
================

Philosophy
----------

When generating Bitcoin addresses for long-term storage of Bitcoins,
it is reccomended that you use a secure offline computer usually with
a freshly installed O/S or a LiveCD O/S.

This program is short enough that one can read through the code and
find out exactly what it does.  Its output is a simple block of text
that contains [1] a passphrase (a bytestring whose sha256sum is your
private key), [2] the private key itself, and [3] the associated
public key.

As long as [1] and [2] are stored secret and safe, money may be
deposited into this account via [3].  At any time, the account
balance may be checked using http://blockchain.info/.

Use
---

From a command-line (denoted by '`$ `'), type:

    $ cd /path/to/this/directory
    $ echo -n 'my passphrase' | ./BitcoinGenerator.py

The private key will be the sha256 hash of your passphrase.  (This is
the same as used by brainwallet.org.)  A passphrase is (in theory)
memorizable; it also serves as a redundant way to store and encode the
private key.

It is not recommended that you use a simple passphrase.  You can use
the provided `RandomWords.py` program to generate a passphrase with
128-bits of entropy.  Before using it, download the wordlist from

    http://world.std.com/~reinhold/diceware.wordlist.asc

You may modify the code use any other list of words to populate the
WordList variable.

It is designed to either use the python random.SystemRandom RNG or to
continually reseed fron `/dev/random` (the default behaviour).  On
systems that lack `/dev/random`, you will need to change
`useDevRandom` to `False`.  Please note that on Linux, reading from
`/dev/random` will block the process and you will need to wiggle your
mouse to generate entropy.

You can feed the output of `RandomWords` into `BitcoinGenerator`.

    $ ./RandomWords.py | ./BitcoinGenerator.py

Alternatively, one can send the output directly to a file:

    $ ./RandomWords.py | ./BitcoinGenerator.py > mykeys.txt

Or encrypt the output:

    $ ./RandomWords.py | ./BitcoinGenerator.py | gpg -cao mykeys.asc


