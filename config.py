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

if 'project_directory' not in locals():
    project_directory = init_project_directory()
    zik = join(project_directory, 'data', 'zik')
    img = join(project_directory, 'data', 'img')
    tile = join(project_directory, 'data', 'img', 'tiles')
    snd = join(project_directory, 'data', 'snd')

    # TODO: Offer GUI to change language
    # TODO: Offer dict or database to handle messages
    languages = ("english", "french")
    language = languages[0]