import sys
import getopt

def main():
    # default value
    line_no = 100
    line_step = 10
    byte_count = 8
    poke_address = 0x700
    output_format = 16
    array_mode = False
    
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
            if a == 'hex':
                output_format = 16
            elif a == 'dec':
                output_format = 10
            elif a == 'bin':
                output_format = 2
            else:
                print('error: unsupported format')
                sys.exit(1)
        elif o == '-c':
            byte_count = int(a)
        else:
            print('error: unhandled option')
            sys.exit(1)
    if len(args) == 0:
        in_file = sys.stdin
        out_file = sys.stdout
    elif len(args) == 1:
        in_file = open(args[0], 'rb')
        out_file = sys.stdout
    elif len(args) == 2:
        in_file = open(args[0], 'rb')
        out_file = open(args[1], 'w+')
    else:
        print('error: too many files')
        sys.exit(1)
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
                poke_address += byte_count
            if array_mode:
                word = ord(byte)
                byte_h = in_file.read(1)
                if byte_h != '':
                    word = word | ord(byte_h) << 8
                out_file.write(',#%04x' % word),
                if byte_h == '':
                    break
            else:
                if output_format == 10:
                    out_file.write(',%d' % ord(byte)),
                elif output_format == 2:
                    out_file.write(',`' + format(ord(byte),'08b')),
                else:
                    out_file.write(',#%02x' % ord(byte)),
            pos_in_line += 1
            if pos_in_line >= byte_count:
                pos_in_line = 0
                line_no += line_step
                out_file.write('\n')
    in_file.close()
    if pos_in_line != 0:
        out_file.write('\n')
        out_file.close()
                    

if __name__ == '__main__':
    main()
