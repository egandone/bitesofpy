def dec_to_base(number, base):
    """
    Input: number is the number to be converted
           base is the new base  (eg. 2, 6, or 8)
    Output: the converted number in the new base without the prefix (eg. '0b')
    """
    if (number >= base):
        n = number % base
        p = dec_to_base(number//base, base)
        n = p * 10 + n
    else:
        n = number
    return n
