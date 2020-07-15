#!/usr/bin/env python3
# coding: utf-8
# @Author: ArthurBernard
# @Email: arthur.bernard.92@gmail.com
# @Date: 2020-07-01 06:21:03
# @Last modified by: ArthurBernard
# @Last modified time: 2020-07-15 10:52:26

""" Script to read csv from zip file. """

# Built-in packages
from zipfile import ZipFile

# Third party packages
import pandas as pd

# Local packages


__all__ = ['load_csv']


def load_csv(path, file):
    """ Load data from the specified path.

    Parameters
    ----------
    (str) path : The path of the file to load.
    (str) file : The name of the file to load.

    Returns
    -------
    (pandas.DataFrame) Loaded data.

    """
    with ZipFile(path) as zf:
        with zf.open(file) as f:
            return pd.read_csv(f)
