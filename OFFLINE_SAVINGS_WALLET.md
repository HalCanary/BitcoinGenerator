This work is licensed under a Creative Commons Attribution 3.0 Unported License.  [http://creativecommons.org/licenses/by/3.0/](http://creativecommons.org/licenses/by/3.0/)

Offline Savings Wallet
======================

Some information taken from [https://en.bitcoin.it/wiki/Securing\_your\_wallet](https://en.bitcoin.it/wiki/Securing_your_wallet).

Download the files

-   BitcoinGenerator.py
-   RandomWords.py
-   diceware.wordlist.asc

and save these to a USB stick.

Shut down your computer, and boot Ubuntu (or Linux distribution of your choice) from a liveCD. This will not affect your current operating system.

Disconnect machine from the internet. Unplug any network cables and disable wireless. Verify that wireless is disabled in the icon on the upper right corner (Ubuntu). Double check that machine is disconnected by opening the web browser.

Open a terminal and type:

    $ cd path/to/BitcoinGenerator
    $ ./RandomWords.py | ./BitcoinGenerator.py

You will get an output that looks like:

    private phrase 'em toy jag meson bremen susan qd pn des fuchs'
    private key 5K8kvby6tLzuAFc4cGy57mwE5BcdMgqZu2vREbBKNmCHyMG3aEg
    public key 1JEjGdQh2JbnpwjfE8WPpZrF9ScMiYNYa3

If you are paranoid, use the diceware protocol instead of RandomWords.

    $ echo -n 'em toy jag meson bremen susan qd pn des fuchs' | ./BitcoinGenerator.py

Note: If RandomWords is reading from /dev/random, wiggle your mouse for a minute to give the system entropy.

Repeat this process N times.  Save the output of the program in a text file on your USB stick.  (If you want additional security, use 'gpg --symmetric' to encrypt this file before saving it.  Do not forget that password.)  If you have a non-networked printer, print out the text file.  If not, write down the keys on paper.  Paper can last thousands of years.  Make multiple backups and keep them in several places.

Save the PUBLIC keys only to your hard drive or a second USB stick.

Put the USB stick with your private keys (and any paper copies) in a safe location.  Never stick it into a computer.

Reboot your computer.

Send bitcoins to the address saved on the USB drive. Double check in the block explorer that they have been sent.

* * *
