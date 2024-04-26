import argparse

"""
The script takes one profile generated from KMCP, and write the percentage relative abundance of clusters in a CAMISIM distribution file, in order to set the distribution profile for a simulated sample.

It takes also the genome_to_id.tsv CAMISIM file, to set all the clusters as 0 abundance from the beginning, to have the same number of genomes within every samples
"""

def read_genome_ids(genome_to_id_file):
    genome_to_abund = {}
    with open(genome_to_id_file) as file:
        for line in file:
            cluster_id, *_ = line.strip().split('\t')
            genome_to_abund[cluster_id] = 0
    return genome_to_abund

def read_abundances(kmcp_profile_file, genome_to_abund):
    with open(kmcp_profile_file) as file:
        for line in file:
            if not line.startswith('ref'):
                cluster_id, percentage = line.strip().split('\t')[0], line.strip().split('\t')[1]
                genome_to_abund[cluster_id] = float(percentage)

def write_output(genome_to_abund, output_file):
    with open(output_file, "w") as file:
        for genome, perc in genome_to_abund.items():
            file.write(f"{genome}\t{perc}\n")

def main(args):
    genome_to_abund = read_genome_ids(args.genome_to_id_file)
    read_abundances(args.kmcp_profile, genome_to_abund)
    write_output(genome_to_abund, args.output_distribution)
    print("Data written successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process kmcp profile and generate distribution output.")
    parser.add_argument("-i", "--kmcp_profile", required=True, help="Path to the kmcp profile file")
    parser.add_argument("-o", "--output_distribution", required=True,  help="Path to the output file")
    parser.add_argument("-g", "--genome-to-id-file", default="/home/vdarbot/bin/CAMISIM/PERSO/CONFIG/genome_to_id.tsv", help="Path to the genome to id file (default: %(default)s)")
    
    args = parser.parse_args()
    main(args)