import os.path
from configparser import ConfigParser


class Appconfig:
    if os.name == 'nt':
        home = os.path.join('library', 'config')
    else:
        home = os.path.expanduser('~')

    # Reading all variables from eSim config.ini
    parser_esim = ConfigParser()
    parser_esim.read(os.path.join(home, os.path.join('.esim', 'config.ini')))
    try:
        src_home = parser_esim.get('eSim', 'eSim_HOME')
        xml_loc = os.path.join(src_home, 'library/modelParamXML')
        lib_loc = os.path.expanduser('~')
    except BaseException:
        pass
    esimFlag = 0

    # Reading all variables from ngveri config.ini
    # parser_ngveri = ConfigParser()
    # parser_ngveri.read(os.path.join(home,
    # os.path.join('.ngveri', 'config.ini')))

    kicad_lib_template = {
        "start_def": "DEF comp_name U 0 40 Y Y 1 F N",
        "U_field": "F0 \"U\" 2850 1800 60 H V C CNN",
        "comp_name_field": "F1 \"comp_name\" 2850 2000 60 H V C CNN",
        "blank_field": ["F2 blank_quotes 2850 1950 60 H V C CNN",
                        "F3 blank_quotes 2850 1950 60 H V C CNN"],
        "start_draw": "DRAW",
        "draw_pos": "S 2350 2100 3350 1800 0 1 0 N",
        "input_port": "X in 1 2150 2000 200 R 50 50 1 1 I",
        "output_port": "X out 2 3550 2000 200 L 50 50 1 1 O",
        "end_draw": "ENDDRAW",
        "end_def": "ENDDEF"
    }
