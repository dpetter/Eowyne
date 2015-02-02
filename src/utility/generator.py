import random
import string


# Random Key Generator
# -------------------------------------------------------------------------------- #
def randomkey(size, prefix = ""):
    '''
    Generates a string of random letters. The key starts with @prefix and
    is @size characters long.
    '''
    randomlength = size - len(prefix)
    if randomlength <= 0: raise ValueError("Prefix longer than key.")
    key = prefix
    for x in range(randomlength):  # @UnusedVariable
        key += random.choice(string.ascii_letters)
    return key