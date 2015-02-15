# -*- coding: utf-8 -*-
from __future__ import print_function

"""
THIS FILE SHOULD RESIDED AT THE ROOT OF THE PROJECT DIRECTORY
Configuration file and utility script.
"""

from os.path import realpath, dirname, join


def init_project_directory():
    """
    Looks up for project's root directory
    """
    full_path = realpath(__file__)
    return dirname(full_path)

project_directory = init_project_directory()
database = join(project_directory, 'data', 'maiden-quebec.db')
zik = join(project_directory, 'data', 'zik')
img = join(project_directory, 'data', 'img')
snd = join(project_directory, 'data', 'snd')