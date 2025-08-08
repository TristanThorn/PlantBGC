import os
from bs4 import BeautifulSoup
import pandas as pd

# Define input and output directories
input_dir = "html/"
output_dir = "html_extract/"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to process a single HTML file
def process_html_file(html_file, output_dir):
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    data = []
    table_rows = soup.find_all("tr", role="row")

    for row in table_rows:
        cells = row.find_all("td")
        if len(cells) < 9:
            continue  # Skip rows that do not contain the required number of columns

        cluster_number = cells[0].text.strip().replace("Cluster ", "")
        record_number = cells[1].text.strip()
        cluster_type = cells[2].text.strip()
        nucl_start = cells[3].text.strip()
        nucl_end = cells[4].text.strip()
        size_kb = cells[5].text.strip()
        core_domains = cells[6].text.strip()
        product = cells[7].text.strip()

        # Convert size from kilobases (KB) to bases
        try:
            size = int(float(size_kb) * 1000)
        except ValueError:
            size = ""

        data.append([cluster_number, record_number, cluster_type, nucl_start, nucl_end, size, core_domains, product])

    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        "potentialBGC", "sequence_id", "type", "nucl_start", "nucl_end", "size", "core_domains", "product"
    ])

    # Define output file path
    base_name = os.path.splitext(os.path.basename(html_file))[0]  # Get file name without extension
    output_file = os.path.join(output_dir, f"{base_name}_html.tsv")

    # Save to TSV
    df.to_csv(output_file, sep="\t", index=False)
    print(f"Processed: {html_file} → {output_file}")

# Iterate over all HTML files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".html"):
        process_html_file(os.path.join(input_dir, filename), output_dir)

print(f"All HTML files processed. TSV files saved in: {output_dir}")
