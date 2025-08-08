from __future__ import (
    print_function,
    division,
    absolute_import,
)
import subprocess
import os
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
import logging
from distutils.spawn import find_executable


class ProdigalProteinRecordAnnotator(object):
    def __init__(self, record, tmp_path_prefix, meta_mode=True):
        self.record = record
        self.tmp_path_prefix = tmp_path_prefix
        self.meta_mode = meta_mode  # 默认设置为True，也可以在初始化时从外部设置

    def annotate(self):
        logging.info('Finding genes in record: %s', self.record.id)
        nucl_path = self.tmp_path_prefix + '.prodigal.nucl.fa'
        SeqIO.write(self.record, nucl_path, 'fasta')
        protein_path = self.tmp_path_prefix + '.prodigal.proteins.fa'

        if not find_executable('prodigal'):
            raise Exception("Prodigal needs to be installed and available on PATH in order to detect genes.")

        logging.debug('Detecting genes using Prodigal...')

        # 这里总是使用 -p meta 选项，无论 meta_mode 的值如何
        command = ['prodigal', '-i', nucl_path, '-a', protein_path, '-p', 'meta']
        logging.debug('Running command: %s', ' '.join(command))

        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        out, err = p.communicate()

        if p.returncode or not os.path.exists(protein_path):
            logging.error('== Prodigal Error: ================')
            logging.error(err.strip())
            logging.error('== End Prodigal Error. ============')
            raise Exception("Unexpected error detecting protein domains using Prodigal")

        proteins = SeqIO.parse(protein_path, 'fasta')
        for protein in proteins:
            splits = protein.description.split('#')
            start = int(splits[1]) - 1
            end = int(splits[2])
            strand = int(splits[3])
            location = FeatureLocation(start, end, strand=strand)
            protein_feature = SeqFeature(location=location, id=protein.id, type="CDS",
                                         qualifiers={'locus_tag': ['{}_{}'.format(self.record.id, protein.id)]})
            self.record.features.append(protein_feature)

