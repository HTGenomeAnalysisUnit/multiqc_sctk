#!/usr/bin/env python
"""
MultiQC_SCTK is a plugin for MultiQC, providing additional tools which are
specific to SCTK single cell QC tool, as modified by HT team.

For more information about SCTK, see https://github.com/compbiomed/singleCellTK
The JSON output used by this plugin is based on our fork here: https://github.com/HTGenomeAnalysisUnit/singleCellTK/tree/HT_GAU_2.6.0
For more information about MultiQC, see http://multiqc.info
"""

from setuptools import setup, find_packages

version = '0.1'

setup(
    name = 'multiqc_sctk',
    version = version,
    author = 'Edoardo Giacopuzzi',
    author_email = 'edoardo.giacopuzzi@fht.org',
    description = "MultiQC plugin for SCTK single-cell QC metrics used in HT scRNA pipeline",
    long_description = __doc__,
    keywords = 'bioinformatics',
    url = 'https://github.com/MultiQC/MultiQC_bcbio',
    download_url = 'https://github.com/MultiQC/MultiQC_bcbio/releases',
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    zip_safe=False,
    install_requires = [
        'multiqc>=1.0',
    ],
    entry_points = {
        'multiqc.modules.v1': [
            'sctk = multiqc_sctk.sctk:MultiqcModule',
        ],
        'multiqc.cli_options.v1': [
            'before_config = multiqc_sctk.cli:sctk_disable',
        ],
        'multiqc.hooks.v1': [
            'execution_start = multiqc_sctk:multiqc_sctk_config'
        ]
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ]
)

