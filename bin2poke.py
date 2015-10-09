import sys
import getopt

def main():
    # default value
    line_no = 100
    line_step = 10
    poke_address = 0x700
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:s:d:')
    except getopt.GetoptError, err:
        print(str(err))
        sys.exit(2)
    for o, a in opts:
        if o == '-a':
            if a.find('0x') == 0:
                a = a[2:]
            poke_address = int('0x' + a, 16)
        elif o == '-s':
            line_no = int(a)
        elif o == '-d':
            line_step = int(a)
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
            in_file.close()
            if pos_in_line != 0:
                out_file.write('\n')
            out_file.close()
            break
        else:
            if pos_in_line == 0:
                out_file.write('%d poke #%03x' % (line_no, poke_address)),
                poke_address += 8
            out_file.write(',#%02x' % ord(byte)),
            pos_in_line += 1
            if pos_in_line >= 8:
                pos_in_line = 0
                line_no += line_step
                out_file.write('\n')
                    
# data = sys.stdin.read()

# line_no = line_no_start
# poke_address = poke_start

# for line in range(len(data) / 8):
#     print('%d poke #%03x,' % line_no, poke_address),
#     for i in range(8):
#         print('%02x' % ord(data[i])),


if __name__ == '__main__':
    main()
