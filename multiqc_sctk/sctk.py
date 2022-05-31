#!/usr/bin/env python
""" MultiQC module to parse output from Samtools """
from __future__ import print_function
import json
from collections import OrderedDict
import logging
from .utils_functions import *

from multiqc.modules.base_module import BaseMultiqcModule
from multiqc import config
from multiqc.plots import linegraph, table

PLUGIN_VERSION = 0.1

# Initialise the logger
log = logging.getLogger('multiqc.sctk')

class MultiqcModule(BaseMultiqcModule):
    """SCTK module: SCTK is a toolkit for single-cell QC. 
    This module parse JSON counts generated by our modified version of SCTK
    """

    def __init__(self):

        # Check that this plugin hasn't been disabled
        if config.kwargs.get('disable_sctk', False) is True:
            log.info("Skipping MultiQC_SCTK as disabled on command line")
            return None
        if getattr(config, 'disable_sctk', False) is True:
            log.debug("Skipping MultiQC_SCTK as specified in config file")
            return None

        log.info("Running SCTK MultiQC Plugin v{}".format(PLUGIN_VERSION))

        # Initialise the parent object
        super(MultiqcModule, self).__init__(
            name="SCTK",
            anchor="sctk",
            href="https://camplab.net/sctk/",
            info="SCTK is a suite that combines several tools for single cell data QC",
            doi="",
        )
    
        self.sctk_summary = dict()
        self.sctk_summary_headers = OrderedDict()
        self.sctk_plot_config = dict()
        self.sctk_plot_data = dict()

        n_reports = {'csv': 0, 'json': 0}
        for f in self.find_log_files("sctk/csv", filehandles=True):
            n_reports['csv'] += 1
            self.parse_sctk_csv(f)

        for f in self.find_log_files("sctk/json", filehandles=False):
            n_reports['json'] += 1
            self.parse_sctk_json(f)

        # Exit if we didn't find anything
        if len(self.sctk_summary) == 0:
            raise UserWarning

        log.info("Found {} SCTK summary reports".format(n_reports['csv']))
        log.info("Found {} SCTK json counts".format(n_reports['json']))
        
        for section in self.sctk_plot_data.keys():
            self.sctk_plot_data[section] = self.ignore_samples(self.sctk_plot_data[section])
        self.sctk_summary = self.ignore_samples(self.sctk_summary)
        
        # Write parsed report data to a file
        self.write_data_file(self.sctk_summary, "SCTK_summary_QC")

        self.sctk_summary_headers = set_hidden_cols(
            self.sctk_summary_headers,
            [
                "scDblFinder - N doublets",
                "DoubletFinder - N doublets",
                "CXDS - N doublets",
                "BCDS - N doublets",
                "SCDS Hybrid - N doublets",
                "Mean contamination",
            ],
        )

        self.add_section(
                name="SCTK - Summary stats",
                anchor="sctk-summary",
                description="Summary QC metrics from SCTK",
                plot=table.plot(self.sctk_summary, self.sctk_summary_headers, {"namespace": "SCTK"}),
            )

        for section in self.sctk_plot_config.keys():
            self.add_section(
                    name=self.sctk_plot_config[section]['name'],
                    anchor=self.sctk_plot_config[section]['anchor'],
                    description=self.sctk_plot_config[section]['description'],
                    plot=linegraph.plot(
                        self.sctk_plot_data[section], self.sctk_plot_config[section]['config']
                    ),
                )

    def parse_sctk_csv(self, f):
        """ Parse the SCTK summary csv file """
        
        data_rows = list()
        for line in f['f']:
            line = line.rstrip('\n').replace('"','').split(",")
            if line[0] != "": data_rows.append(line)
        
        col_dict = {
            "Mean features detected": "mean_features",
            "Median features detected": "median_features",
            "scDblFinder - Number of doublets": "scDblFinder - N doublets",
            "scDblFinder - Percentage of doublets": "scDblFinder - % doublets",
            "DoubletFinder - Number of doublets, Resolution 1.5": "DoubletFinder - N doublets",
            "DoubletFinder - Percentage of doublets, Resolution 1.5": "DoubletFinder - % doublets",
            "CXDS - Number of doublets": "CXDS - N doublets",
            "CXDS - Percentage of doublets": "CXDS - % doublets",
            "BCDS - Number of doublets": "BCDS - N doublets",
            "BCDS - Percentage of doublets": "BCDS - % doublets",
            "SCDS Hybrid - Number of doublets": "SCDS Hybrid - N doublets",
            "SCDS Hybrid - Percentage of doublets": "SCDS Hybrid - % doublets",
            "DecontX - Mean contamination": "Mean contamination",
            "DecontX - Median contamination": "Median contamination",
        }

        self.sctk_summary[f['s_name']], self.sctk_summary_headers = update_dict(
            self.sctk_summary_headers,
            data_rows,
            col_dict,
        )

    def parse_sctk_json(self, f):
        """ Parse the SCTK summary json file with plot data """
        
        sctk_json = json.loads(f['f'])
        sctk_json = {key: data for key, data in sctk_json.items() if key != "sample"}
        
        self.sctk_plot_config['UMI'] = { 
            'name': 'SCTK - UMI counts',
            'anchor': 'sctk-umi-counts',
            'description': 'Counts of UMIs per cell',
            'config': {
                'id': 'sctk-umi-plot',
                'title': 'SCTK: UMI count distribution',
                'data_labels': [
                    {'name': 'density', 'ylab': 'density', 'xlab': 'UMI count'},
                    {'name': 'cumulative', 'ylab': 'fraction of cells UMI > x', 'xlab': 'UMI count'},
                ],
            },
        }

        self.sctk_plot_data['UMI'] = update_plot_data('UMI',self.sctk_plot_data, sctk_json, f['s_name'])

        self.sctk_plot_config['genes'] = { 
            'name': 'SCTK - genes counts',
            'anchor': 'sctk-genes-counts',
            'description': 'Counts of genes per cell',
            'config': {
                'id': 'sctk-genes-plot',
                'title': 'SCTK: genes count distribution',
                'data_labels': [
                    {'name': 'density', 'ylab': 'density', 'xlab': 'genes count'},
                    {'name': 'cumulative', 'ylab': 'fraction of cells genes > x', 'xlab': 'genes count'},
                ],
            },
        }

        self.sctk_plot_data['genes'] = update_plot_data('genes',self.sctk_plot_data, sctk_json, f['s_name'])

        self.sctk_plot_config['counts'] = { 
            'name': 'SCTK - reads counts',
            'anchor': 'sctk-reads-counts',
            'description': 'Counts of gene mapped reads per cell',
            'config': {
                'id': 'sctk-reads-plot',
                'title': 'SCTK: mapped reads distribution',
                'data_labels': [
                    {'name': 'density', 'ylab': 'density', 'xlab': 'reads count'},
                    {'name': 'cumulative', 'ylab': 'fraction of cells reads > x', 'xlab': 'mapped reads count'},
                ],
            },
        }

        self.sctk_plot_data['counts'] = update_plot_data('counts',self.sctk_plot_data, sctk_json, f['s_name'])
        