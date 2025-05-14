# Copyright 2025 Joe Bears
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import csv
import warnings

import numpy as np
import pandas as pd
from pint import Quantity
from pint.errors import UndefinedUnitError

from structuraltools.template import Result
from structuraltools.unit import unit, Numeric


def sqrt(value: Numeric) -> Numeric:
    """Square root function compatible with pint Quantities and structuraltools
    Results

    Parameters
    ==========

    value : Numeric
        Value to take the square root of"""
    if isinstance(value, Result):
        value = value.value
    return np.sqrt(value)

def sign(value: Numeric, *args, **kwargs) -> int:
    """Wrapper around np.sign to provide compatibility with structuraltools
    Result instances

    Parameters
    ==========

    value : Numeric
        Value to check the sign for

    *args
        Refer to the numpy.sign documentation

    **kwargs
        Refer to the numpy.sign documentation"""
    if isinstance(value, Result):
        value = value.value
    return np.sign(value)

def isclose(
        value_1: Numeric,
        value_2: Numeric,
        rtol: Numeric = 1e-5,
        atol: Numeric = 1e-8,
        equal_nan: bool = False) -> bool:
    """Wrapper around np.isclose to provide compatibility with structuraltools
    Result instances

    Parameters
    ==========

    value_1 : Numeric
        First value to compare

    value_2 : Numeric
        Second value to compare

    rtol : Numeric
        Relative tolerance for returning True

    atol : Numeric
        Absolute tolerance for returning True

    equal_nan : bool
        Whether to compare NaNs as equal"""
    args = []
    for value in [value_1, value_2, rtol, atol]:
        if isinstance(value, Result):
            args.append(value.value)
        else:
            args.append(value)
    return np.isclose(*args, equal_nan)

def linterp(
        x_1: Numeric,
        y_1: Numeric,
        x_2: Numeric,
        y_2: Numeric,
        x_3: Numeric) -> Numeric:
    """Linear interpolation between two points

    Parameters
    ==========

    x1 : Numeric
        x value of first point for interpolation

    y1 : Numeric
        y value of first point for interpolation

    x2 : Numeric
        x value of second point for interpolation

    y2 : Numeric
        y value of second point for interpolation

    x3 : Numeric
        x value of point to interpolate y value for."""
    y_3 = y_1+(y_2-y_1)/(x_2-x_1)*(x_3-x_1)
    return y_3

def linterp_dicts(
        x_1: Numeric,
        dict_1: dict[any, dict],
        x_2: Numeric,
        dict_2: dict[any, dict],
        x_3: Numeric) -> dict[any, dict]:
    """Returns a dictionary that is a linear interpolation between two provided
    dictionaries of dictionaries with the same keys. Numeric value are
    interpolated all other values are taken from dict_1.

    Parameters
    ==========

    x_1 : Numeric
        Value to associate with dict_1 for interpolation

    dict_1 : dict[any, dict]
        First dictionary of values to interpolate

    x_2 : Numeric
        Value to associate with dict_2 for interpolation

    dict_2 : dict[any, dict]
        Second dictionary of values to interpolate

    x_3 : Numeric
        Interpolation value to associate with the new dictionary"""
    dict_3 = {}
    for key_1 in dict_1.keys():
        dict_3.update({key_1: {}})
        for key_2 in dict_1[key_1].keys():
            if isinstance(dict_1[key_1][key_2], int | float | Quantity):
                dict_3[key_1].update({
                    key_2: linterp(
                        x_1,
                        dict_1[key_1][key_2],
                        x_2,
                        dict_2[key_1][key_2],
                        x_3)
                    })
            else:
                dict_3[key_1].update({key_2: dict_1[key_1][key_2]})
    return dict_3

def round_to(value: Numeric, to: Numeric) -> Numeric:
    """Round the provided value away from 0 to the nearest multiple of to

    Parameters
    ==========

    value : Numeric
        Value to round

    to : Numeric
        Rounding target"""
    to = abs(to)
    if isinstance(value, Quantity):
        return to*(abs(value.to(to.units).magnitude)//to.magnitude+1)*sign(value)
    return to*(abs(value)//to+1)*sign(value)

def convert_to_unit(value: any) -> any:
    """Attempts to convert the given value to a Quantity if it is a string.
    The value is returned unmodified if it cannot be converted.

    Parameters
    ==========

    value : any
        Value to convert"""
    if isinstance(value, str):
        first_value = value.split(" ")[0]
        for character in ".-eE":
            first_value = first_value.replace(character, "")
        if first_value.isdigit():
            try:
                value = unit(value)
            except UndefinedUnitError:
                warnings.warn(f"'{value}' was not evaluated as a unit")
    return value

def read_data_table(filepath: str) -> pd.DataFrame:
    """Reads a .csv file and returns a pandas DataFrame with the first column
    set as the index and convert_to_unit run on all values

    Parameters
    ==========

    filepath : str
        Path to the file"""
    data_table = pd.read_csv(filepath)
    data_table = data_table.map(convert_to_unit)
    data_table = data_table.set_index(data_table.columns[0], drop=True)
    return data_table
