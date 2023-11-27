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

    # KiCad v6 Library Template
    kicad_sym_template = {
        "start_def":    "(symbol \"comp_name\" (pin_names (offset 1.016)) " +
                        "(in_bom yes) (on_board yes)",
        "U_field":  "(property \"Reference\" \"U\" (id 0) (at 12 15 0)" +
                    "(effects (font (size 1.524 1.524))))",
        "comp_name_field":  "(property \"Value\" \"comp_name\" (id 1) " +
                            "(at 12 18 0)(effects (font (size 1.524 1.524))))",
        "blank_field":  [
            "(property \"Footprint\" blank_quotes (id 2) " +
            "(at 72.39 49.53 0)(effects (font (size 1.524 1.524))))",
            "(property \"Datasheet\" blank_quotes (id 3) " +
            "(at 72.39 49.53 0)(effects (font (size 1.524 1.524))))"
        ],
        "draw_pos":     "(symbol \"comp_name\"(rectangle (start 0 0 ) " +
                        "(end 25.40 3.6 )(stroke (width 0) (type default) " +
                        "(color 0 0 0 0))(fill (type none))))",
        "start_draw":   "(symbol",
        "input_port":   "(pin input line(at -5.15 0.54 0 )(length 5.08 )" +
                        "(name \"in\" (effects(font(size 1.27 1.27))))" +
                        "(number \"1\" (effects (font (size 1.27 1.27)))))",
        "output_port":  "(pin output line(at 30.52 0.54 180 )(length 5.08 )" +
                        "(name \"out\" (effects(font(size 1.27 1.27))))" +
                        "(number \"2\" (effects (font (size 1.27 1.27)))))",
        "end_draw":     "))"
    }
