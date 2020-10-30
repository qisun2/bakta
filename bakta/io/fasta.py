
import logging

from Bio import SeqIO

import bakta.config as cfg
import bakta.constants as bc


log = logging.getLogger('io:fasta')

FASTA_LINE_WRAPPING = 60

def import_contigs(contigs_path):
    """Import raw contigs."""
    contigs = []
    with contigs_path.open() as fh:
        for record in SeqIO.parse(fh, 'fasta'):
            seq = str(record.seq).upper()
            contig = {
                'id': record.id,
                'desc': record.description,
                'sequence': seq,
                'length': len(seq),
                'complete': False,
                'type': bc.REPLICON_CONTIG,
                'topology': bc.TOPOLOGY_LINEAR
            }
            contigs.append(contig)
    return contigs


def export_contigs(contigs, fasta_path, description=False, wrap=False):
    """Write contigs to Fasta file."""
    with fasta_path.open('w') as fh:
        for contig in contigs:
            if(description):
                fh.write(">%s %s\n" % (contig['id'], contig['desc']))
            else:
                fh.write(">%s\n" % (contig['id'], ))
            if(wrap):
                fh.write(wrap_sequence(contig['sequence']))
            else:
                fh.write("%s\n" % contig['sequence'])


def wrap_sequence(sequence):
    lines = ''
    while len(sequence) > FASTA_LINE_WRAPPING:
        lines += sequence[:FASTA_LINE_WRAPPING] + '\n'
        sequence = sequence[FASTA_LINE_WRAPPING:]
    lines += sequence + '\n'
    return lines


def write_faa(features, faa_path):
    """Write translated CDS sequences to Fasta file."""
    with faa_path.open('w') as fh:
        for feat in features:
            if(feat['type'] == bc.FEATURE_CDS or feat['type'] == bc.FEATURE_SORF):
                fh.write(">%s %s\n%s\n" % (feat['locus'], feat['product'], feat['sequence']))
