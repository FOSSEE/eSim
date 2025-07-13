# -*- coding: utf-8 -*-
# Copyright © 2017 Kevin Thibedeau
# Distributed under the terms of the MIT license
import io
import os
from collections import OrderedDict

from hdlparse.minilexer import MiniLexer

"""Verilog documentation parser"""

verilog_tokens = {
    # state
    'root': [
        # patterns
        #  pattern, action, new_state
        (r'\bmodule\s+(\w+)\s*', 'module', 'module'),
        (r'/\*', 'block_comment', 'block_comment'),
        (r'//#+(.*)\n', 'metacomment'),
        (r'//.*\n', None),
    ],
    'module': [
        (r'parameter\s*(signed|integer|realtime|real|time)?\s*(\[[^]]+\])?', 'parameter_start', 'parameters'),
        (
            r'^[\(\s]*(input|inout|output)\s+(reg|supply0|supply1|tri|triand|trior|tri0|tri1|wire|wand|wor)?'
            r'\s*(signed)?\s*((\[[^]]+\])+)?',
            'module_port_start', 'module_port'),
        (r'endmodule', 'end_module', '#pop'),
        (r'/\*', 'block_comment', 'block_comment'),
        (r'//#\s*{{(.*)}}\n', 'section_meta'),
        (r'//.*\n', None),
    ],
    'parameters': [
        (r'\s*parameter\s*(signed|integer|realtime|real|time)?\s*(\[[^]]+\])?', 'parameter_start'),
        (r'\s*(\w+)\s*=\s*((?:(?!\/\/|[,)]).)*)', 'param_item'),
        (r'//#+(.*)\n', 'metacomment'),
        (r',', None),
        (r'//.*\n', None),
        (r'[);]', None, '#pop'),
    ],
    'module_port': [
        (
            r'\s*(input|inout|output)\s+(reg|supply0|supply1|tri|triand|trior|tri0|tri1|wire|wand|wor)?'
            r'\s*(signed)?\s*((\[[^]]+\])+)?',
            'module_port_start'),
        (r'\s*(\w+)\s*,?', 'port_param'),
        (r'/\*', 'block_comment', 'block_comment'),
        (r'[);]', None, '#pop'),
        (r'//#\s*{{(.*)}}\n', 'section_meta'),
        (r'//#+(.*)\n', 'metacomment'),
        (r'//.*\n', None),
    ],

    'block_comment': [
        (r'\*/', 'end_comment', '#pop'),
    ],
}

VerilogLexer = MiniLexer(verilog_tokens)


class VerilogObject:
    """Base class for parsed Verilog objects"""

    def __init__(self, name, desc=None):
        self.name = name
        self.kind = 'unknown'
        self.desc = [] if desc is None else desc


class VerilogParameter:
    """Parameter and port to a module"""

    def __init__(self, name, mode=None, data_type=None, default_value=None, desc=None):
        self.name = name
        self.mode = mode
        self.data_type = data_type
        self.default_value = default_value
        self.desc = [] if desc is None else desc

    def __str__(self):
        if self.mode is not None:
            param = f"{self.name} : {self.mode} {self.data_type}"
        else:
            param = f"{self.name} : {self.data_type}"
        if self.default_value is not None:
            param = f"{param} := {self.default_value}"
        return param

    def __repr__(self):
        return f"VerilogParameter('{self.name}')"


class VerilogModule(VerilogObject):
    """Module definition"""

    def __init__(self, name, ports, generics=None, sections=None, desc=None):
        VerilogObject.__init__(self, name, desc)
        self.kind = 'module'
        # Verilog params
        self.generics = generics if generics is not None else []
        self.ports = ports
        self.sections = sections if sections is not None else {}

    def __repr__(self):
        return f"VerilogModule('{self.name}') {self.ports}"


def parse_verilog_file(fname):
    """Parse a named Verilog file

    Args:
      fname (str): File to parse.
    Returns:
      List of parsed objects.
    """
    with open(fname, 'rt') as fh:
        text = fh.read()
    return parse_verilog(text)


def parse_verilog(text):
    """Parse a text buffer of Verilog code

    Args:
      text (str): Source code to parse
    Returns:
      List of parsed objects.
    """
    lex = VerilogLexer

    name = None
    kind = None
    saved_type = None
    mode = 'input'
    port_type = 'wire'
    param_type = ''

    metacomments = []
    parameters = []

    generics = []
    ports = OrderedDict()
    sections = []
    port_param_index = 0
    last_item = None
    array_range_start_pos = 0

    objects = []

    for pos, action, groups in lex.run(text):
        if action == 'metacomment':
            comment = groups[0].strip()
            if last_item is None:
                metacomments.append(comment)
            else:
                last_item.desc.append(comment)

        if action == 'section_meta':
            sections.append((port_param_index, groups[0]))

        elif action == 'module':
            kind = 'module'
            name = groups[0]
            generics = []
            ports = OrderedDict()
            sections = []
            port_param_index = 0

        elif action == 'parameter_start':
            net_type, vec_range = groups

            new_param_type = ''
            if net_type is not None:
                new_param_type += net_type

            if vec_range is not None:
                new_param_type += ' ' + vec_range

            param_type = new_param_type

        elif action == 'param_item':
            param_name, default_value = groups
            param = VerilogParameter(param_name, 'in', param_type, default_value)
            generics.append(param)
            last_item = param

        elif action == 'module_port_start':
            new_mode, net_type, signed, vec_range = groups[0:4]

            new_port_type = ''
            if net_type is not None:
                new_port_type += net_type

            if signed is not None:
                new_port_type += ' ' + signed

            if vec_range is not None:
                new_port_type += ' ' + vec_range

            # Start with new mode
            mode = new_mode
            port_type = new_port_type

        elif action == 'port_param':
            port_ident = groups[0]
            port_obj = VerilogParameter(port_ident, mode, port_type)
            ports[port_ident] = port_obj
            port_param_index += 1
            last_item = port_obj

        elif action == 'end_module':
            vobj = VerilogModule(name, ports.values(), generics, dict(sections), metacomments)
            objects.append(vobj)
            last_item = None
            metacomments = []

    return objects


def is_verilog(fname):
    """Identify file as Verilog by its extension

    Args:
      fname (str): File name to check
    Returns:
      True when file has a Verilog extension.
    """
    return os.path.splitext(fname)[1].lower() in ('.vlog', '.v')


class VerilogExtractor:
    """Utility class that caches parsed objects"""

    def __init__(self):
        self.object_cache = {}

    def extract_objects(self, fname, type_filter=None):
        """Extract objects from a source file

        Args:
          fname(str): Name of file to read from
          type_filter (class, optional): Object class to filter results
        Returns:
          List of objects extracted from the file.
        """
        objects = []
        if fname in self.object_cache:
            objects = self.object_cache[fname]
        else:
            with io.open(fname, 'rt', encoding='utf-8') as fh:
                text = fh.read()
                objects = parse_verilog(text)
                self.object_cache[fname] = objects

        if type_filter:
            objects = [o for o in objects if isinstance(o, type_filter)]

        return objects

    def extract_objects_from_source(self, text, type_filter=None):
        """Extract object declarations from a text buffer

        Args:
          text (str): Source code to parse
          type_filter (class, optional): Object class to filter results
        Returns:
          List of parsed objects.
        """
        objects = parse_verilog(text)

        if type_filter:
            objects = [o for o in objects if isinstance(o, type_filter)]

        return objects

    def is_array(self, data_type):
        """Check if a type is an array type

        Args:
          data_type (str): Data type
        Returns:
          True when a data type is an array.
        """
        return '[' in data_type
