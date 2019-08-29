import os.path
from ConfigParser import SafeConfigParser


class Appconfig:
    home = os.path.expanduser("~")
    #Reading all varibale from eSim config.ini
    parser_esim = SafeConfigParser()
    parser_esim.read(os.path.join(home, os.path.join('.esim','config.ini')))
    try:
        src_home = parser_esim.get('eSim','eSim_HOME')
        xml_loc = os.path.join(src_home,'src/modelParamXML')
        lib_loc = os.path.expanduser('~')
    except:
        pass
    esimFlag = 0

    #Reading all variable from nghdl config.ini
    parser_nghdl = SafeConfigParser()
    parser_nghdl.read(os.path.join(home,os.path.join('.nghdl','config.ini')))

    kicad_lib_template = {
    "start_def":"DEF comp_name U 0 40 Y Y 1 F N",
    "U_field":"F0 \"U\" 2850 1800 60 H V C CNN",
    "comp_name_field":"F1 \"comp_name\" 2850 2000 60 H V C CNN",
    "blank_field":["F2 blank_quotes 2850 1950 60 H V C CNN","F3 blank_quotes 2850 1950 60 H V C CNN"],
    "start_draw":"DRAW",
    "draw_pos":"S 2550 2100 3150 1800 0 1 0 N",
    "input_port":"X in 1 2350 2000 200 R 50 50 1 1 I",
    "output_port":"X out 2 3350 2000 200 L 50 50 1 1 O",
    "end_draw":"ENDDRAW",
    "end_def":"ENDDEF"
    }


