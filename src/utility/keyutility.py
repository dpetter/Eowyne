# -*- coding: utf-8 -*-
#
# Key Utility
#
# Provides functions for generating keys and hashes.
#
# Created on 2015-02-22.
# ================================================================================ #
import random
import string
import hashlib


# Random Key Generator
# -------------------------------------------------------------------------------- #
def randomkey(size, prefix = ""):
    '''
    @returns            Random key.
    @param size:        Length of the random key to generate.
    @param prefix:      Character sequence the key starts with.
    '''
    randomlength = size - len(prefix)
    if randomlength <= 0: raise ValueError("Prefix longer than key.")
    key = prefix + "".join([random.choice(string.ascii_letters)
                            for x in range(randomlength)])  # @UnusedVariable
    return key

# -------------------------------------------------------------------------------- #
def encrypt(text):
    '''
    Encrypts text with sha265.
    '''
    global salt
    if not text: return None
    t = salt + ":" + text
    return hashlib.sha256(t.encode("ascii")).hexdigest()