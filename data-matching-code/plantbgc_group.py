import pandas as pd
import re
import os

input_dir = "PlantBGC_Merged3gap_Result/"
output_dir = "outputs/"

for file in os.listdir(input_dir):
    if file.endswith(".tsv"):
        input_file = os.path.join(input_dir, file)
        output_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}_grouped.tsv")

        # Read the TSV file
        df = pd.read_csv(input_file, sep="\t")

        # Filter and group data
        df_new = df[df["potentialBGC"] != 0]
        df_new = df_new.groupby("potentialBGC", as_index=False).agg({
            "protein_ids": lambda x: ";".join(x)  # Merge protein IDs with semicolons
        })

        df_new["protein_ids"] = df_new["protein_ids"].str.replace(",", ";")

        # Function to extract XP identifiers
        def extract_identifiers(pid_string):
            """Extract only XP_... identifiers and separate them by semicolons."""
            ids = re.findall(r'(?:XP_|NP_|KAH_)\d+\.\d+', pid_string)  # Find all XP_... patterns
            return ";".join(sorted(set(ids)))  # Join without duplicates

        df_new["Gene cluster gene accessions"] = df_new["protein_ids"].apply(extract_identifiers)

        # Save the processed data
        df_new.to_csv(output_file, sep="\t", index=False)

        print(f"Transformation complete. File saved to: {output_file}")

print("All files processed.")

