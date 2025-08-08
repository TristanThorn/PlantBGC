import os
import pandas as pd
from difflib import SequenceMatcher

# Load the two TSV files
plantismash_dir = "/Users/cassandrayang/Desktop/plantismash_grouped/"
plantbgc_dir = "/Users/cassandrayang/Desktop/plantbgc_grouped/"
output_dir = "/Users/cassandrayang/Desktop/similarity_output/"

plantismash_files = sorted([f for f in os.listdir(plantismash_dir) if f.endswith(".tsv")])
plantbgc_files = sorted([f for f in os.listdir(plantbgc_dir) if f.endswith(".tsv")])

# Process each file in plantismash_dir
for plantismash_file in plantismash_files:
    plantismash_path = os.path.join(plantismash_dir, plantismash_file)

    # Load plantismash TSV file
    plantismash_df = pd.read_csv(plantismash_path, sep="\t")

    # Find the best-matching plantbgc file (assumes filenames match)
    matching_bgc_file = next((f for f in plantbgc_files if f.split("_plantbgc")[0] in plantismash_file), None)

    if matching_bgc_file:
        plantbgc_path = os.path.join(plantbgc_dir, matching_bgc_file)
        plantbgc_df = pd.read_csv(plantbgc_path, sep="\t")

        # Ensure required columns exist
        if "Gene cluster gene accessions" in plantismash_df.columns and "Gene cluster gene accessions" in plantbgc_df.columns:
            
            # Function to find the best match for a given gene accession
            def find_best_match(gene_accession):
                best_match = None
                highest_similarity = 0.0

                for idx, bgc_gene_accession in enumerate(plantbgc_df["Gene cluster gene accessions"]):
                    similarity = SequenceMatcher(None, str(gene_accession), str(bgc_gene_accession)).ratio()
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        best_match = idx + 1  # Assuming record number is 1-based index

                return best_match, highest_similarity * 100  # Convert similarity to percentage

            # Apply function to find best match for each record
            plantismash_df[["Best_Match_BGC", "Similarity"]] = plantismash_df["Gene cluster gene accessions"].apply(
                lambda x: pd.Series(find_best_match(x))
            )

            # Save the results
            output_file = os.path.join(output_dir, f"{plantismash_file}_similarity_output.tsv")
            plantismash_df.to_csv(output_file, sep="\t", index=False)
            print(f"Saved: {output_file}")

        else:
            print(f"Error: Required column missing in {plantismash_file} or {matching_bgc_file}")
    else:
        print(f"No matching plantbgc file found for {plantismash_file}")

print("Processing complete.")