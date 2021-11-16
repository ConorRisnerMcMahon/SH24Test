def normalise_postcode(postcode: str) -> str:
    postcode = ''.join(postcode.split())
    postcode = postcode.upper()
    postcode = postcode[:-3] + ' ' + postcode[-3:]
    return postcode
