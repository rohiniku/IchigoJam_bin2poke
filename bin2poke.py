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
    
def get_d_u8(inst):
    d = (inst >> 8) & 0x0007
    u8 = inst & 0x00ff
    return d, u8

def get_n_u8(inst):
    return get_d_u8(inst)

def get_m_d(inst):
    m = s = (inst >> 3) & 0x0007
    d = inst & 0x0007
    return m, d

def get_s_d(inst):
    return get_m_d(inst)

def get_u5_n_d(inst):
    u5 = (inst >> 6) & 0x001f
    n = (inst >> 3) & 0x0007
    d = inst & 0x0007
    return u5, n, d

def get_u5_m_d(inst):
    return get_u5_n_d(inst)

def get_u3_n_d(inst):
    u5, n, d = get_u5_n_d(inst)
    u3 = u5 & 0x0007
    return u3, n, d

def get_m_n_d(inst):
    return get_u3_n_d(inst)

def get_n8(inst):
    return inst & 0x00ff

def get_n11(inst):
    return inst & 0x07ff

def disasm(inst):
    inst_str = 'unknown'
    inst15_11 = inst & 0xf800
    inst15_9  = inst & 0xfe00
    inst15_8  = inst & 0xff00
    inst15_6  = inst & 0xffc0
    # print('inst15_11 {0:016b}'.format(inst15_11))
    # print('inst15_9  {0:016b}'.format(inst15_9))
    # print('inst15_8  {0:016b}'.format(inst15_8))
    # print('inst15_6  {0:016b}'.format(inst15_6))
    if inst15_11 == 0b0010000000000000:
        d, u8 = get_d_u8(inst)
        inst_str = 'R{0:}={1:}'.format(d, u8)
        print("{0:016b} {1:}".format(inst, inst_str))
    elif inst15_11 == 0b0100000000000000:
        m, d = get_m_d(inst)
        s = m
        inst10_6 = inst & 0x07c0
        if inst10_6 == 0b0000011000000000:
            inst_str = 'R{0:}=R{1:}'.format(d, m)
        elif inst10_6 == 0b0000000000000000:
            inst_str = 'R{0:}=R{0:}&R{1:}'.format(d, m)
        elif inst10_6 == 0b0000000001000000:
            inst_str = 'R{0:}=R{0:}^R{1:}'.format(d, m)
        elif inst10_6 == 0b0000000010000000:
            inst_str = 'R{0:}=R{0:}<<R{1:}'.format(d, s)
        elif inst10_6 == 0b0000000011000000:
            inst_str = 'R{0:}=R{0:}>>R{1:}'.format(d, s)
        elif inst10_6 == 0b0000001001000000:
            inst_str = 'R{0:}=-R{1:}'.format(d, m)
        elif inst10_6 == 0b0000001100000000:
            inst_str = 'R{0:}=R{0:}|R{1:}'.format(d, m)
        elif inst10_6 == 0b0000001101000000:
            inst_str = 'R{0:}=R{0:}*R{1:}'.format(d, m)
        elif inst10_6 == 0b0000001110000000:
            inst_str = 'R{0:}=R{0:}&~R{1:}'.format(d, m)
        elif inst10_6 == 0b0000001111000000:
            inst_str = 'R{0:}=~R{1:}'.format(d, m)
        elif inst == 0b0100011101110000:
            inst_str = 'RET'
    elif inst15_11 == 0b0111100000000000:
        u5, n, d = get_u5_n_d(inst)
        inst_str = 'R{0:}=[R{1:}+{2:}]'.format(d, n, u5)
    elif inst15_11 == 0b0111000000000000:
        u5, n, d = get_u5_n_d(inst)
        inst_str = '[R{0:}+{1:}]=R{2:}'.format(n, u5, d)
    elif inst15_9 == 0b0101110000000000:
        m, n, d = get_m_n_d(inst)
        inst_str = 'R{0:}=[R{1:}+R{2:}]'.format(d, n, m)
    elif inst15_9 == 0b0101010000000000:
        m, n, d = get_m_n_d(inst)
        inst_str = '[R{0:}+R{1:}]=R{2:}'.format(n, m, d)
    elif inst15_11 == 0b0011000000000000:
        d, u8 = get_d_u8(inst)
        inst_str = 'R{0:}=R{0:}+{1:}'.format(d, u8)
    elif inst15_11 == 0b0011100000000000:
        d, u8 = get_d_u8(inst)
        inst_str = 'R{0:}=R{0:}-{1:}'.format(d, u8)
    elif inst15_11 == 0b0000000000000000:
        u5, m, d = get_u5_m_d(inst)
        inst_str = 'R{0:}=R{1:}<<{2:}'.format(d, m, u5)
    elif inst15_11 == 0b0000100000000000:
        u5, m, d = get_u5_m_d(inst)
        inst_str = 'R{0:}=R{1:}>>{2:}'.format(d, m, u5)
    elif inst15_9 == 0b0001110000000000:
        u3, n, d = get_u3_n_d(inst)
        inst_str = 'R{0:}=R{1:}+{2:}'.format(d, n, u3)
    elif inst15_9 == 0b0001111000000000:
        u3, n, d = get_u3_n_d(inst)
        inst_str = 'R{0:}=R{1:}-{2:}'.format(d, n, u3)
    elif inst15_9 == 0b0001100000000000:
        m, n, d = get_m_n_d(inst)
        inst_str = 'R{0:}=R{1:}+R{2:}'.format(d, n, m)
    elif inst15_9 == 0b0001101000000000:
        m, n, d = get_m_n_d(inst)
        inst_str = 'R{0:}=R{1:}-R{2:}'.format(d, n, m)
    elif inst15_11 == 0b0010100000000000:
        n, u8 = get_n_u8(inst)
        inst_str = 'R{0:}-{1:}'.format(n, u8)
    elif inst15_6 == 0b0100001010000000:
        m, n = get_m_n(inst)
        inst_str = 'R{0:}-R{1:}'.format(n, m)
    elif inst15_6 == 0b0100001000000000:
        m, n = get_m_n(inst)
        inst_str = 'R{0:}&R{1:}'.format(n, m)
    elif inst15_8 == 0b1101000000000000:
        n8 = get_n8(inst)
        inst_str = 'IF 0 JUMP {0:}<<1'.format(n8)
    elif inst15_8 == 0b1101000100000000:
        n8 = get_n8(inst)
        inst_str = 'IF !0 JUMP {0:}<<1'.format(n8)
    elif inst15_11 == 0b1110000000000000:
        n11 = get_n11(inst)
        inst_str = 'JUMP {0:}<<1'.format(n11)
    
    print("->{0:016b} {1:}".format(inst, inst_str))
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
