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
import bcrypt


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
def hash_password(text):
    '''
    Encrypts text with bcrypt.
    '''
    if not text: return None
    return bcrypt.hashpw(text, bcrypt.gensalt(12))  # @UndefinedVariable

# -------------------------------------------------------------------------------- #
def match_password(text, pw_hash):
    '''
    Checks if the password matches.
    '''
    return bcrypt.hashpw(text, pw_hash) == pw_hash  # @UndefinedVariable
