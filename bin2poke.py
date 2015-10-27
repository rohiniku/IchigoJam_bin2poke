import sys
import getopt

def open_files(args_wo_options):
    if len(args_wo_options) == 0:
        in_file = sys.stdin
        out_file = sys.stdout
    elif len(args_wo_options) == 1:
        in_file = open(args_wo_options[0], 'rb')
        out_file = sys.stdout
    elif len(args_wo_options) == 2:
        in_file = open(args_wo_options[0], 'rb')
        out_file = open(args_wo_options[1], 'w+')
    else:
        print('error: too many files')
        sys.exit(1)
    return in_file, out_file

def write_u1(file, format, data):
    if format == 10:
        file.write(',{0:d}'.format(data)),
    elif format == 2:
        file.write(',`{0:0>8b}'.format(data)),
    else:
        file.write(',#{0:0>2x}'.format(data)),

def write_u2(file, format, data):
    if format == 10:
        file.write(',{0:d}'.format(data)),
    elif format == 2:
        file.write(',`{0:0>16b}'.format(data)),
    else:
        file.write(',#{0:0>4x}'.format(data)),
    
def get_u3_u8(inst):
    u3 = (inst >> 8) & 0x0007
    u8 = inst & 0x00ff
    return u3, u8

def get_u3_u3(inst):
    u3_h = (inst >> 3) & 0x0007
    u3_l = inst & 0x0007
    return u3_h, u3_l

def get_u5_u3_u3(inst):
    u5 = (inst >> 6) & 0x001f
    u3_h = (inst >> 3) & 0x0007
    u3_l = inst & 0x0007
    return u5, u3_h, u3_l

def get_u3_u3_u3(inst):
    u5, n, d = get_u5_u3_u3(inst)
    u3 = u5 & 0x0007
    return u3, n, d

def get_s8(inst):
    u8 = inst & 0x00ff
    if u8 & 0x80:
        return -((u8 - 1) ^ 0xff)
    else:
        return u8

def get_s11(inst):
    u11 = inst & 0x07ff
    if u11 & 0x400:
        return -((u11 - 1) ^ 0x7ff)
    else:
        return u11

inst_str15_11_s11 = {
    0b1110000000000000: lambda n11: 'GOTO {0:}'.format(n11 + 2)
}

inst_str15_11_u3_u8 = {
    0b0010000000000000: lambda d,u8: 'R{0:}={1:}'.format(d, u8),
    0b0011000000000000: lambda d,u8: 'R{0:}=R{0:}+{1:}'.format(d, u8),
    0b0011100000000000: lambda d,u8: 'R{0:}=R{0:}-{1:}'.format(d, u8),
    0b0010100000000000: lambda n,u8: 'R{0:}-{1:}'.format(n, u8)
}

inst_str15_11_u5_u3_u3 = {
    0b0111100000000000: lambda u5,n,d: 'R{0:}=[R{1:}+{2:}]'.format(d, n, u5),
    0b0111000000000000: lambda u5,n,d: '[R{0:}+{1:}]=R{2:}'.format(n, u5, d),
    0b0000000000000000: lambda u5,m,d: 'R{0:}=R{1:}<<{2:}'.format(d, m, u5),
    0b0000100000000000: lambda u5,m,d: 'R{0:}=R{1:}>>{2:}'.format(d, m, u5)
}
    
inst_str15_9_u3_u3_u3 = {
    0b0101110000000000: lambda m,n,d: 'R{0:}=[R{1:}+R{2:}]'.format(d, n, m),
    0b0101010000000000: lambda m,n,d: '[R{0:}+R{1:}]=R{2:}'.format(n, m, d),
    0b0001100000000000: lambda m,n,d: 'R{0:}=R{1:}+R{2:}'.format(d, n, m),
    0b0001101000000000: lambda m,n,d: 'R{0:}=R{1:}-R{2:}'.format(d, n, m),
    0b0001110000000000: lambda u3,n,d: 'R{0:}=R{1:}+{2:}'.format(d, n, u3),
    0b0001111000000000: lambda u3,n,d: 'R{0:}=R{1:}-{2:}'.format(d, n, u3)
}

inst_str15_8_s8 = {
    0b1101000000000000: lambda n8: 'IF 0 GOTO {0:}'.format(n8 + 2),
    0b1101000100000000: lambda n8: 'IF !0 GOTO {0:}'.format(n8 + 2)
}

inst_str15_6_u3_u3 = {
    0b0100011000000000: lambda m,d: 'R{0:}=R{1:}'.format(d, m),
    0b0100000000000000: lambda m,d: 'R{0:}=R{0:}&R{1:}'.format(d, m),
    0b0100000001000000: lambda m,d: 'R{0:}=R{0:}^R{1:}'.format(d, m),
    0b0100000010000000: lambda s,d: 'R{0:}=R{0:}<<R{1:}'.format(d, s),
    0b0100000011000000: lambda s,d: 'R{0:}=R{0:}>>R{1:}'.format(d, s),
    0b0100001001000000: lambda m,d: 'R{0:}=-R{1:}'.format(d, m),
    0b0100001100000000: lambda m,d: 'R{0:}=R{0:}|R{1:}'.format(d, m),
    0b0100001101000000: lambda m,d: 'R{0:}=R{0:}*R{1:}'.format(d, m),
    0b0100001110000000: lambda m,d: 'R{0:}=R{0:}&~R{1:}'.format(d, m),
    0b0100001111000000: lambda m,d: 'R{0:}=~R{1:}'.format(d, m),
    0b0100001010000000: lambda m,n: 'R{0:}-R{1:}'.format(n, m),
    0b0100001000000000: lambda m,n: 'R{0:}&R{1:}'.format(n, m)
}

inst_str15_0 = {
    0b0100011101110000: 'RET'
}

def disasm(inst):
    inst_str = 'unknown'
    inst15_11 = inst & 0xf800
    inst15_9  = inst & 0xfe00
    inst15_8  = inst & 0xff00
    inst15_6  = inst & 0xffc0

    if inst in inst_str15_0:
        inst_str = inst_str15_0[inst]
    elif inst15_11 in inst_str15_11_s11:
        n11 = get_s11(inst)
        inst_str = inst_str15_11_s11[inst15_11](n11)
    elif inst15_11 in inst_str15_11_u3_u8:
        d, u8 = get_u3_u8(inst)
        inst_str = inst_str15_11_u3_u8[inst15_11](d, u8)
    elif inst15_11 in inst_str15_11_u5_u3_u3:
        u5, n, d = get_u5_u3_u3(inst)
        inst_str = inst_str15_11_u5_u3_u3[inst15_11](u5, n, d)
    elif inst15_9 in inst_str15_9_u3_u3_u3:
        m, n, d = get_u3_u3_u3(inst)
        inst_str = inst_str15_9_u3_u3_u3[inst15_9](m, n, d)
    elif inst15_8 in inst_str15_8_s8:
        n8 = get_s8(inst)
        inst_str = inst_str15_8_s8[inst15_8](n8)
    elif inst15_6 in inst_str15_6_u3_u3:
        m, d = get_u3_u3(inst)
        inst_str = inst_str15_6_u3_u3[inst15_6](m, d)
    
    return inst_str

def main():
    # default value
    line_no = 100
    line_step = 10
    data_count = 8
    poke_address = 0x700
    output_format = 16
    array_mode = False
    disasm_mode = False
    support_formats = {'hex':16, 'dec':10, 'bin':2}

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:s:d:o:c:')
    except getopt.GetoptError, err:
        print(str(err))
        sys.exit(2)
    for o, a in opts:
        if o == '-a':
            if a.find('0x') == 0:
                a = a[2:]
            poke_address = int('0x' + a, 16)
            if poke_address == 0:
                array_mode = True
        elif o == '-s':
            line_no = int(a)
        elif o == '-d':
            line_step = int(a)
        elif o == '-o':
            if a in support_formats:
                output_format = support_formats[a]
            else:
                print('error: unsupported format')
                sys.exit(1)
        elif o == '-c':
            data_count = int(a)
        else:
            print('error: unhandled option')
            sys.exit(1)
    if array_mode and output_format == 2 and data_count == 1:
        disasm_mode = True

    in_file, out_file = open_files(args)
    out_file.softspace = False

    pos_in_line = 0
    while True:
        byte = in_file.read(1)
        if byte == '':
            break
        else:
            if pos_in_line == 0:
                if array_mode:
                    out_file.write('%d let[%d]' % (line_no, poke_address)),
                else:
                    out_file.write('%d poke#%03x' % (line_no, poke_address)),
                poke_address += data_count
            if array_mode:
                word = ord(byte)
                byte_h = in_file.read(1)
                if byte_h != '':
                    word = word | ord(byte_h) << 8
                write_u2(out_file, output_format, word)
                if disasm_mode:
                    disasm_code = disasm(word)
                    out_file.write(':\'' + disasm_code),
                if byte_h == '':
                    break
            else:
                write_u1(out_file, output_format, ord(byte))
            pos_in_line += 1
            if pos_in_line >= data_count:
                pos_in_line = 0
                line_no += line_step
                out_file.write('\n')
    in_file.close()
    if pos_in_line != 0:
        out_file.write('\n')
        out_file.close()
                    

if __name__ == '__main__':
    main()
