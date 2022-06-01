# MultiQC SCTK plugin

This plug-in parses the output of the [SCTK QC tool](https://camplab.net/sctk/v2.6.0/articles/cmd_qc.html) as modified by HT Genome Analysis Unit. Check our [forked repo of SCTK](https://github.com/HTGenomeAnalysisUnit/singleCellTK/tree/HT_GAU_2.6.0).

The plugin reads summary CSV file and counts JSON file for each sample and create a SCTK section in the MultiQC report.

## Installation

First, install MultiQC: `pip install MultiQC`

Then clone this repo and install the plugin: `python setup.py install`

## Disable the plugin

Use the `--disable-sctk` flag to disable the plugin execution.

## File name convention

The plugins expects the following file names:

1. **CSV**: `SCTK_*_summary.csv`
2. **JSON**: `SCTK_*_counts.json`

## Report output

An example report containing the SCTK section is in the example folder.

The plugin will add a new section to the report named SCTK that contains:

- A table with summary stats from QC (% doublets, % contamination, etc)

- Density and cumsum plots for N genes detected, N UMIs, N reads and % mitochondrial reads per cell
