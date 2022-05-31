from __future__ import absolute_import

# Add search patterns and config options for the things that are used in MultiQC_SCTK
def multiqc_sctk_config():
    from multiqc import config
    """ Set up MultiQC config defaults for this package """
    sctk_search_patterns = {
        'sctk/csv': {'fn': 'SCTK_*_cellQC_summary.csv'},
        'sctk/json': {'fn': 'SCTK_*_cellQC_counts.json'},
    }
    config.update_dict(config.sp, sctk_search_patterns)

    config.fn_clean_exts.extend([
        {'type': 'truncate', 'pattern': '_cellQC'},
    ])
    config.fn_clean_trim.extend([
        'SCTK_',
    ])