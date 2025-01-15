#The MIT License (MIT)

#PSpice to Oscad Schematic Converter
#This code is written by Suryavamshi Tenneti, FOSSEE, IIT Bombay
#The code is modified by Sumanto Kar and Gloria Nandihal, FOSSEE, IIT Bombay


from component_instance import *


def skipTo(input_stream, s):  # Find the line containing the first occurence (after the current position) of string s in istream& in and read it and then return it
    tmp = '1'
    while tmp != '' and tmp.find(s) == -1:
        tmp = input_stream.readline().strip()  # cout<<tmp<<"**"<<endl;

        # print('SkipLine',tmp)
        # print('In skipto',tmp.find(s))

    if tmp == '':  # cerr<<"skipTo error"<<endl;
        return '__ERROR__'

    return tmp


def stripNumFromRef(ref):
    i = len(ref) - 1
    while i >= 0 and ref[i] >= '0' and ref[i] <= '9':
        i -= 1
    return ref[:i + 1]


def fixComp(c):

    # print('In fixComp c.type' ,c.type_)

    ref = c.ref

    # print('last 6')

    if ref == 'Q':  # Transistor
        for i in range(0, len(c.pins)):
            if c.pins[i].n == 'e' or c.pins[i].n == 'E':
                c.pins[i].n = '1'
            if c.pins[i].n == 'b' or c.pins[i].n == 'B':
                c.pins[i].n = '2'
            if c.pins[i].n == 'c' or c.pins[i].n == 'C':
                c.pins[i].n = '3'

        ref = 'Q'
        c.ref = 'Q'
        return

    # print('last 5')

    if ref == 'J':  # Mos
        for i in range(0, len(c.pins)):
            if c.pins[i].n == 'g' or c.pins[i].n == 'G':
                c.pins[i].n = 'G'
            if c.pins[i].n == 's' or c.pins[i].n == 'S':
                c.pins[i].n = 'S'
            if c.pins[i].n == 'd' or c.pins[i].n == 'D':
                c.pins[i].n = 'D'
        ref = 'J'
        c.ref = 'J'
        return

    # print('last 5')

    if ref == 'M':  # FET
        for i in range(0, len(c.pins)):
            if c.pins[i].n == 'g' or c.pins[i].n == 'G':
                c.pins[i].n = 'G'
            if c.pins[i].n == 's' or c.pins[i].n == 'S':
                c.pins[i].n = 'S'
            if c.pins[i].n == 'd' or c.pins[i].n == 'D':
                c.pins[i].n = 'D'
        ref = 'M'
        c.ref = 'M'
        return

    # print('last4')

    if ref == 'E':  # Linear voltage controlled voltage sources
        for i in range(0, len(c.pins)):
            if c.pins[i].n == '1':
                c.pins[i].n = '3'
                continue
            if c.pins[i].n == '2':
                c.pins[i].n = '4'
                continue
            if c.pins[i].n == '3':
                c.pins[i].n = '1'
                continue
            if c.pins[i].n == '4':
                c.pins[i].n = '2'
                continue
        ref = 'E'
        c.ref = 'E'
        return

    # print('last3') #Linear current controlled current sources

    if ref == 'F':
        for i in range(0, len(c.pins)):
            if c.pins[i].n == '1':
                c.pins[i].n = '3'
                continue
            if c.pins[i].n == '2':
                c.pins[i].n = '4'
                continue
            if c.pins[i].n == '3':
                c.pins[i].n = '1'
                continue
            if c.pins[i].n == '4':
                c.pins[i].n = '2'
                continue
        ref = 'F'
        c.ref = 'F'
        return

    # print('last2')

    if ref == 'G':  # Linear Voltage controlled voltage sources
        for i in range(0, len(c.pins)):
            if c.pins[i].n == '1':
                c.pins[i].n = '3'
                continue
            if c.pins[i].n == '2':
                c.pins[i].n = '4'
                continue
            if c.pins[i].n == '3':
                c.pins[i].n = '1'
                continue
            if c.pins[i].n == '4':
                c.pins[i].n = '2'
                continue
        ref = 'G'
        c.ref = 'G'
        return

    # print('last1')

    if ref == 'H':  # Linear Current controlled voltage sources
        for i in range(0, len(c.pins)):
            if c.pins[i].n == '1':
                c.pins[i].n = '3'
                continue
            if c.pins[i].n == '2':
                c.pins[i].n = '4'
                continue
            if c.pins[i].n == '3':
                c.pins[i].n = '1'
                continue
            if c.pins[i].n == '4':
                c.pins[i].n = '2'
                continue
        ref = 'H'
        c.ref = 'H'
        return

    # print('last')

    if c.type_ == 'VPLOT1' or c.type_ == 'VPLOT2' or c.type_ \
        == 'VPRINT1' or c.type_ == 'VPRINT2' or c.type_ == 'IPRINT' \
        or c.type_ == 'IPLOT':
        ref = 'U'
        c.ref = 'U'
        c.value = c.type_
        if c.type_ == 'VPLOT2':
            c.value = 'VPLOT8'
        if c.type_ == 'VPRINT2':
            c.value = 'VPRINT'

        # print('*1')

        return


def fixInst(ci):

    # print(len(ci.attrs))

    ref = stripNumFromRef(ci.attrs[0].value)

    # print('misc',ref)

    if ref == 'J':
        ci.attrs[0].value = 'J?'
        return
    if ref == 'M':
        ci.attrs[0].value = 'M?'
        return

# Voltage sources

    if ci.type_ == 'VAC' or ci.type_ == 'VDC' or ci.type_ == 'VPULSE' \
        or ci.type_ == 'VSIN' or ci.type_ == 'VEXP' or ci.type_ \
        == 'VPWL':
        if ci.attrs[1].value == 'VAC' or ci.attrs[1].value == 'VDC' \
            or ci.attrs[1].value == 'VPULSE' or ci.attrs[1].value \
            == 'VEXP':
            ci.attrs[1].value = \
                ci.attrs[1].value[1:len(ci.attrs[1].value)]
        if ci.attrs[1].value == 'VSIN':
            ci.attrs[1].value = 'SINE'
        return

# Plot sources

    if ci.type_ == 'VPLOT1' or ci.type_ == 'VPLOT2' or ci.type_ \
        == 'VPRINT1' or ci.type_ == 'VPRINT2' or ci.type_ == 'IPRINT' \
        or ci.type_ == 'IPLOT':
        ci.attrs[0].value = 'U?'
        if ci.type_ == 'VPLOT2':
            ci.attrs[1].value = 'VPLOT8'
        if ci.type_ == 'VPRINT2':
            ci.attrs[1].value = 'VPRINT'
        return

# Gnd sources

    if ci.type_ == 'AGND' or ci.type_ == 'GND_ANALOG':
        ci.type_ = 'GND'
        return

    if ci.type_ == 'EGND' or ci.type_ == 'GND_EARTH':

        # print(True)

        ci.type_ = 'GND'
        return

