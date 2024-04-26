import sys
import glob
# tax_dump_dir, in order to recreate metadata.tsv


# Input files
profiles_dir = "/home/vdarbot/results/test/kmcp/BBP7*profile.tsv"

tax_dump_dir = "/home/vdarbot/db/GTDB/GTDB_test_taxdump/"

names_fi = tax_dump_dir + "names.dmp"

genome_id_fi = "/home/vdarbot/bin/CAMISIM/PERSO/CONFIG/genome_to_id.tsv"

metadata_out = open("/home/vdarbot/bin/CAMISIM/PERSO/CONFIG/metadata.tsv", "w")

Clusters_to_taxid = dict()

taxid_in_profiles = list()

Taxnames_to_clusters = dict()

# Use glob to find all files matching the pattern
file_list = glob.glob(profiles_dir)

# Iterate over each file in the list
for file_path in file_list:
    print("Reading file:", file_path)
    # Open the file for reading
    with open(file_path, "r") as file:
        # Read each line in the file
        for line in file:
           line = line.strip()
           if not line.startswith("ref"):
                line_spl = line.split("\t")

                cluster_id = line_spl[0]
                tax_id = line_spl[12]
                tax_name = line_spl[14]
                
                rank_l = tax_name.split("_")[0]
                if rank_l == "s":
                    rank = "known_species"
                elif rank_l == "g":
                    rank = "known_genus"
                elif rank_l == "f":
                    rank = "known_family"
                elif rank_l == "o":
                    rank = "known_order"
                elif rank_l == "c":
                    rank = "known_class"
                elif rank_l == "p":
                    rank = "known_phylum"
                else:
                    rank = "new_species"

                if cluster_id not in Clusters_to_taxid:
                    Clusters_to_taxid[cluster_id] = tax_id

                    if tax_name not in Taxnames_to_clusters:
                        Taxnames_to_clusters[tax_name] = [rank, cluster_id]
                    
                    else:
                        Taxnames_to_clusters[tax_name].append(cluster_id)

metadata_out.write("genome_ID\tOTU\tNCBI_ID\tnovelty_category\n")
incr_taxname = 0
for taxname, clusters in Taxnames_to_clusters.items():
    incr_taxname += 1

    rank_cur = clusters[0]

    for cluster in clusters[1:]:

        metadata_out.write(cluster + "\t" + str(incr_taxname) + "\t" + Clusters_to_taxid[cluster] + "\t" + rank_cur + "\n" )

with open(genome_id_fi) as file:
    for line in file:
        line=line.strip()
        cluster_id = line.split('\t')[0]
        if cluster_id not in Clusters_to_taxid:
            incr_taxname +=1
            metadata_out.write(cluster_id + "\t" + str(incr_taxname) + "\t1\tnew_species\n" )



metadata_out.close()