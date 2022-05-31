#!/usr/bin/env python
""" MultiQC command line options - we tie into the MultiQC
core here and add some new command line parameters. """

import click

sctk_disable = click.option('--disable_sctk',
    is_flag = True,
    default = False,
    help = "Disable the MultiQC_SCTK plugin on this run"
)