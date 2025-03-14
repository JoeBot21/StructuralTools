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
from string import Template
import warnings

from IPython.display import display, Latex
import pandas as pd
from pint import Quantity
from pint.errors import UndefinedUnitError

from structuraltools import decimal_points, unit
from structuraltools import Numeric


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

def convert_to_unit(value: any) -> any:
    """Checks if the given value is likely to be a string of a pint
    Quantity and attempts to read with the set unit registry. This
    is designed to help with reading serialized data.

    Parameters
    ==========

    value : any
        Value to convert. If this is a string that starts with a number it will
        attempt to convert it to a Quantity. Any non-string or string that can't
        be converted will be returned unmodified."""

    if isinstance(value, str):
        if value.split(" ")[0].replace(".", "").replace("-", "").isdigit():
            try:
                value = unit(value)
            except UndefinedUnitError:
                warnings.warn(f"{value} was not evaluated as a unit")
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

def get_table_entry(filepath: str, index: str) -> dict:
    """Returns the specified row from a csv file as a dict. String values that
    are likely to be numeric or contain Pint quantities are evaluated with
    convert_to_unit. A "with" context handler does not need to be used when
    calling this function.

    Parameters
    ==========

    filepath : str
        Path to the csv file

    index : str
        First value on the row to return"""
    with open(filepath) as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            if tuple(line.values())[0] == index:
                raw_data = line
                break
    data = {key: convert_to_unit(value) for key, value in raw_data.items()}
    return data

def fill_templates(main_template: Template, variables: dict, *return_vals):
    """Function to fill out latex templates used for displaying calculations.
    This is designed to be used in the return statement of another function to
    fill out the primary latex template associated with that function.

    Parameters
    ==========

    main_template : Template
        Main template string to fill out and return if requested

    variables : dict
        Dictionary of additional arguments and values to use to fill out the
        template strings. Any template strings in the variables dictionary will
        be filled out and used to fill out the main template.

        The variables dictionary may contain a latex_options sub-dictionary to
        specify addition arguments for the latex output.

        show : bool, optional
            Boolean indicating if the calculations should be displayed with
            IPython's display(Latex()). Defaults to False.

        return_latex : bool, optional
            Boolean indicating if the latex string should be returned.
            Defaults to False.

        decimal_points : int, optional
            How many decimal places to use when writing variables into the
            latex template. defaults to the value in
            structuraltools.decimal_points.

    return_vals : Any
        Values to return. If return_latex is specified in a latex_options
        sub-dictionary contained in the variables dictionary a new tuple
        consisting of the latex prepended to returns will be returned"""
    latex_options = {
        "show": False,
        "return_latex": False,
        "decimal_points": decimal_points
    }
    latex_options.update(variables.get("latex_options", {}))
    if not (latex_options["show"] or latex_options["return_latex"]):
        if len(return_vals) == 1:
            return return_vals[0]
        else:
            return return_vals

    sorted_vars = {}
    subtemplates = {}
    for key, value in variables.items():
        if isinstance(value, Template) and value != main_template:
            subtemplates.update({key: value})
        elif getattr(value, "unpack_for_templates", False):
            sorted_vars.update(vars(value))
        else:
            sorted_vars.update({key: value})

    rounded_vars = {}
    for key, value in sorted_vars.items():
        if isinstance(value, Quantity | float):
            rounded_vars.update({key: round(value, latex_options["decimal_points"])})
        else:
            rounded_vars.update({key: value})

    filled_subtemplates = {}
    for name, subtemplate in subtemplates.items():
        filled_subtemplates.update({name: subtemplate.substitute(**rounded_vars)})

    latex = main_template.substitute(**filled_subtemplates, **rounded_vars)
    if latex_options["show"]:
        display(Latex(latex))
    if latex_options["return_latex"]:
        return (latex, *return_vals)
    elif len(return_vals) == 1:
        return return_vals[0]
    else:
        return return_vals
