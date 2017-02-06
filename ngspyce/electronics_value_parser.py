# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 2016

"""
from __future__ import division, print_function, unicode_literals

__all__ = ['value_parser']

prefixes = {
    'Y': 1e24,
    'Z': 1e21,
    'E': 1e18,
    'P': 1e15,
    'T': 1e12,
    'G': 1e9,
    'M': 1e6,
    'MEG': 1e6,
    'Meg': 1e6,
    'k': 1e3,
    'K': 1e3,  # Common but not standard
    'm': 1e-3,
    'u': 1e-6,  # Common but not standard
    '\u03bc': 1e-6,  # GREEK SMALL LETTER MU
    '\u00b5': 1e-6,  # MICRO SIGN
    'n': 1e-9,
    'p': 1e-12,
    'f': 1e-15,
    'a': 1e-18,
    'z': 1e-21,
    'y': 1e-24,
    }

infixes = prefixes.copy()
infixes.update({'R': 1})

units = {
    'R': 'ohm',
    '\u2126': 'ohm',  # OHM SIGN
    '\u03a9': 'ohm',  # GREEK CAPITAL LETTER OMEGA
    'ohm': 'ohm',
    'F': 'farad',
    'H': 'henry',
    'V': 'volt',
    'A': 'ampere',
    'W': 'watt',
    'Hz': 'hertz',
    'C': 'coulomb',
    'S': 'siemen',
    }


def value_parser(value):
    """
    Converts typical electronics schematics value labels into a float and a
    unit string.  Accepts things like '3000', '3k3', '3e3', '4 μF', etc.
    """
    try:
        value = float(value)
        unit = None
    except ValueError:
        # Units
        for test_unit in units:
            if value.endswith(test_unit):
                unit = units[test_unit]
                value = value[:-len(test_unit)].strip()
                break
        else:
            unit = None

        if value[-1] in prefixes:
            # Unit prefixes at end
            mul = prefixes[value[-1]]
            value = value[:-1]
        else:
            # Unit prefixes but infixed
            # TODO: Could convert '3k3' to '3.3k' instead of testing this way
            for test_inf in infixes:
                if test_inf in value:
                    parts = value.split(test_inf)
                    value = parts[0] + '.' + parts[1]
                    mul = infixes[test_inf]
                    break
            else:
                mul = 1

        value = float(value) * mul

    return value, unit


# TODO: from nose.tools import assert_almost_equals
# instead of testing floats for equality

def test_unitless():
    # Literals
    assert value_parser(4700) == (4700, None)
    assert value_parser(3.3) == (3.3, None)
    assert value_parser(4.7e3) == (4.7e3, None)
    assert value_parser(9.83652e-05) == (9.83652e-05, None)

    # Strings
    assert value_parser('3.3') == (3.3, None)
    assert value_parser('3') == (3, None)
    assert value_parser('3e3') == (3e3, None)
    assert value_parser('9.83652e-05') == (9.83652e-05, None)


def test_trailing_prefix():
    assert value_parser('3k') == (3000, None)
    assert value_parser('3K') == (3000, None)
    assert value_parser('3.3K') == (3300, None)
    assert value_parser('10u') == (10 * 1e-6, None)  # almost_equal
    assert value_parser('10 u') == (10 * 1e-6, None)  # almost_equal
    assert value_parser('10μ') == (10 * 1e-6, None)  # almost_equal
    assert value_parser('10µ') == (10 * 1e-6, None)  # almost_equal


def test_infix():
    assert value_parser('3k3') == (3300, None)
    assert value_parser('2M2') == (2.2e6, None)
    assert value_parser('4n7') == (4.7 * 1e-9, None)
    assert value_parser('3R3') == (3.3, None)  # !!!


def test_units():
    assert value_parser('10mA') == (10e-3, 'ampere')
    assert value_parser('10 ohm') == (10, 'ohm')
    assert value_parser('10   A') == (10, 'ampere')
    assert value_parser('3kA') == (3e3, 'ampere')
    assert value_parser('1 F') == (1, 'farad')
    assert value_parser('3kohm') == (3e3, 'ohm')
    assert value_parser('3 kΩ') == (3e3, 'ohm')
    assert value_parser('103.013 uF') == (103.013 * 1e-6, 'farad')
    assert value_parser('10 μF') == (10 * 1e-6, 'farad')
    assert value_parser('100R') == (100, 'ohm')
    assert value_parser('4.7kV') == (4.7 * 1e3, 'volt')
    assert value_parser('4.7k\u2126') == (4.7 * 1e3, 'ohm')
    assert value_parser('4.7k\u03a9') == (4.7 * 1e3, 'ohm')
    assert value_parser('245.894 mH') == (245.894 * 1e-3, 'henry')

#
#if __name__ == "__main__":
#    import pytest
#    pytest.main(['--tb=short', __file__])
