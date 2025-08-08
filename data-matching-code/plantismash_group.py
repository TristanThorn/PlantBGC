import pandas as pd
import os

# Define directory paths
dir1_path = "html_extract/"  # Directory containing former files with last three columns
dir2_path = "html_merge/"  # Directory containing latter files to be modified
output_dir = "outputs/plantismash_grouped/"  # Directory to store merged TSV files

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get sorted lists of files in both directories
files1 = sorted([os.path.join(dir1_path, f) for f in os.listdir(dir1_path) if f.endswith(".tsv")])
files2 = sorted([os.path.join(dir2_path, f) for f in os.listdir(dir2_path) if f.endswith(".csv")])

# Process files sequentially
num_files = min(len(files1), len(files2))  # Ensure we don't go out of range

if num_files == 0:
    print("No matching files found between the two directories.")
else:
    for i in range(num_files):
        try:
            file1_path = files1[i]
            file2_path = files2[i]

            # Load the data
            df1 = pd.read_csv(file1_path, sep="\t")  # Load former file
            df2 = pd.read_csv(file2_path)  # Load latter file

            # Extract the last three columns from df1
            last_three_columns = df2.iloc[:, -3:]

            # Ensure "sequence_id" exists in df2 before proceeding
            if "sequence_id" in df1.columns:
                # Remove "sequence_id" from its current position
                df1_reordered = df1.drop(columns=["sequence_id"])

                # Insert "sequence_id" before the last three columns
                df1_reordered.insert(len(df1_reordered.columns), "sequence_id", df1["sequence_id"])

                # Concatenate the dataframes
                df_combined = pd.concat([df1_reordered, last_three_columns], axis=1)

                # Define output file path
                output_path = os.path.join(output_dir, f"{file2_path}.plantismash.tsv")

                # Save the merged data
                df_combined.to_csv(output_path, sep="\t", index=False)

                print(f"Processed and saved: {output_path}")
            else:
                print(f"Skipping : 'sequence_id' column not found in latter file.")

        except Exception as e:
            print(f"Error processing: {e}")

print("Processing completed.")
