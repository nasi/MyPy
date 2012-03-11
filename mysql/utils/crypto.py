from mysql.utils.hashcompat import sha_constructor


def scramble(password, salt):
    if not password: return chr(0)
    
    stage1_hash = sha_constructor(password).digest()
    stage2_hash = sha_constructor(stage1_hash).digest()
    hash_ = sha_constructor(salt + stage2_hash).digest()
    
    result = chr(len(hash_))
    for x, y in zip(hash_, stage1_hash):
        result += chr(ord(x) ^ ord(y))
    
    return result
