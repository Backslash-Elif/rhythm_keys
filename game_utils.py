import global_vars

def hextobits(hex:str):
    dec = int(hex, 16)
    bits = []
    for i in range(4):
        bits.append(True if dec%2 else False)
        dec = int(dec/2)
    return list(reversed(bits))

def bitstohex(bits:iter):
    bits = list(reversed(bits))
    dec = 0
    for i in range(4):
        dec += [1,2,4,8][i] if bits[i] else 0
    return str(hex(dec)[2:])

def loadfromlvldat(index:int):
    if index in global_vars.editor_lvldat:
        return global_vars.editor_lvldat[index]
    else:
        return '0'