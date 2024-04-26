import sys

# Input files
genome_to_id_fi = "/home/vdarbot/bin/CAMISIM/PERSO/CONFIG/genome_to_id.tsv"
kmcp_profile_fi = sys.argv[1]

# Output file
distribution_output_fi = open(sys.argv[2], "w")

# Dictionary to store abundances
genome_to_abund = {}

# Read genome IDs
with open(genome_to_id_fi) as fi:
    for li in fi:
        li = li.strip().split('\t')
        cluster_id = li[0]
        genome_to_abund[cluster_id] = 0

# Read abundances from kmcp profile
with open(kmcp_profile_fi) as fu:
    for lu in fu:
        lu = lu.strip()
        if not lu.startswith('ref'):
            li_s = lu.split('\t')
            cluster_id = li_s[0]
            percentage = float(li_s[1])
            genome_to_abund[cluster_id] = percentage

# Write abundances to output file
try:
    for genome, perc in genome_to_abund.items():
        distribution_output_fi.write(genome + "\t" + str(perc) + "\n")
    print("Data written successfully.")
except Exception as e:
    print("An error occurred while writing data:", e)

# Close the output file
distribution_output_fi.close()