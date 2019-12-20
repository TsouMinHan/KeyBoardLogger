import struct
import socket
import io

def int_to_nbyte(n):
    if n < (1 << 8):
        # 數值小於256，用byte
        tag = 'B'
    elif n < (1 << 16):
        # 數值小於65536，用word
        tag = 'H'
    elif n < (1 << 32):
        # 數值小於429467296，用long
        tag = 'L'
    else:
        # 超過
        tag = 'Q'

    return tag.encode('utf-8') + struct.pack('!' + tag, n)

def nbyte_to_int(source):
    read_bytes = lambda d, s: (d[:s], d[s:])
    read_file = lambda d, s: (d.read(s), d)
    read_socket = lambda d, s: (d.recv(s), d)

    reader_dc = {
        bytes: read_bytes, 
        io.IOBase: read_file,
        socket.socket: read_socket
    }
    size_info = {'B': 1, 'H': 2, 'L': 4, 'Q': 8,}

    reader = reader_dc[type(source)]

    btag, source = reader(source, 1)

    tag = btag.decode('utf-8')

    if not tag in size_info:
        raise TypeError('Incalid type: ' + type(tag))

    size = size_info[tag]

    bnum, source = source[:size], source[size:]

    return struct.unpack('!' + tag, bnum)[0], source

def bignum_to_bytes(n):
    result = b''

    while n>0:
        b = n % 128
        n >>= 7

        if n:
            b +=128
        
        result += bytes([b])

    return result

def bytes_to_bignum(bs):
    result = 0
    exp = 0

    for b in bs:
        n = b % 128
        result += n << exp
        exp += 7

        if b & (1 << 7) == 0:
            break
    
    return result

def str_to_nbyte(s):
    tag, s_byte = ('s', s) if isinstance(s, bytes) else ('c', s.encode('utf-8'))
    n_bytes = int_to_nbyte(len(s_byte))

    return tag.encode('utf-8') + n_bytes + s_byte

def nbyte_to_str(source):
    read_bytes = lambda d,s: (d[:s], d[s:])
    read_file = lambda d, s: (d.read(s), d)
    read_socket = lambda d, s: (d.recv(s), d)
    reader_dc = {
        bytes: read_bytes,
        io.IOBase: read_file,
        socket.socket: read_socket
    }
    reader = reader_dc[type(source)]

    btag, source = reader(source, 1)
    tag = btag.decode('utf-8')

    if tag not in ['s', 'c']:
        raise TypeError('invalid tag: ' + tag)

    size, source = nbyte_to_int(source)

    bstr, source = reader(source, size)

    return bstr if tag == 's' else bstr.decode('utf-8')

def data_to_nbyte(n):
    if isinstance(n, int):
        if n < (1 << 8):
        # 數值小於256，用byte
            tag = 'B'
        elif n < (1 << 16):
            # 數值小於65536，用word
            tag = 'H'
        elif n < (1 << 32):
            # 數值小於429467296，用long
            tag = 'L'
        else:
            # 超過
            tag = 'Q'
        
        return tag.encode('utf-8') + struct.pack('!' + tag, n)

    elif isinstance(n, bytes):
        tag = 's'

        return tag.encode('utf-8') + data_to_nbyte(len(n)) + n
    
    elif isinstance(n, str):
        tag = 'c'

        return tag.encode('utf-8') + data_to_nbyte(len(n)) + n.encode('utf-8')

    raise TypeError('Invalid type: ' + type(tag))

def nbyte_to_data(source):
    read_bytes = lambda d,s: (d[:s], d[s:])
    read_file = lambda d, s: (d.read(s), d)
    read_socket = lambda d, s: (d.recv(s), d)
    reader_dc = {
        bytes: read_bytes,
        io.IOBase: read_file,
        socket.socket: read_socket
    }
    size_info = {'B': 1, 'H': 2, 'L': 4, 'Q': 8,}

    reader = reader_dc[type(source)]
    btag, source = reader(source, 1)

    if not btag:
        return None, source
    
    tag = btag.decode('utf-8')

    if tag in size_info:
        size = size_info[tag]
        bnum, source = reader(source, size)
        result = struct.unpack('!'+tag, bnum)[0]

    elif tag in ['s', 'c']:
        size, source = nbyte_to_data(source)
        if size >= 65536:
            raise ValueError('length too long: ' + str(size))
        bstr, source = reader(source, size)
        result = bstr if tag == 's' else bstr.decode('utf-8')
    
    else:
        raise TypeError('Invalid type: ' + tag)

    return result, source

if __name__ == "__main__":
    
    b = data_to_nbyte('Hello, World')
    print(b)

    print(nbyte_to_data(b))

    b = data_to_nbyte(5201314)
    print(b)

    print(nbyte_to_data(b))

