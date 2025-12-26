import os

# Folder containing all your TXT files
input_folder = r"C:\Users\kumar\Downloads\Amazon_train_data\English_US"  # <-- change this to your folder path
# Folder where the split files will be saved
output_folder = "split_txt_files"
os.makedirs(output_folder, exist_ok=True)

# Maximum file size in bytes (50 KB)
MAX_SIZE = 47 * 1024  # 50 KB

def split_txt_file(file_path, output_folder):
    # Read the full content of the file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Start splitting
    start = 0
    part = 1
    content_bytes = content.encode('utf-8')  # count in bytes

    while start < len(content_bytes):
        chunk = content_bytes[start:start + MAX_SIZE]
        chunk_text = chunk.decode('utf-8', errors='ignore')  # safe decode
        
        # Save chunk as a new file
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(output_folder, f"{base_name}_part{part}.txt")
        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.write(chunk_text)
        
        part += 1
        start += MAX_SIZE

# Process all TXT files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".txt"):
        file_path = os.path.join(input_folder, filename)
        split_txt_file(file_path, output_folder)

print(f"All TXT files have been split into ≤50 KB chunks in '{output_folder}' folder.")


import os
import pandas as pd

# Folder containing TXT files
txt_folder = "split_txt_files"  # <-- change this to your folder path
# Folder to save CSV files
csv_folder = "csv_files"
os.makedirs(csv_folder, exist_ok=True)

# Columns for CSV
columns = ["Phrase", "SoundsLike", "IPA", "DisplayAs"]

# Process each TXT file
for filename in os.listdir(txt_folder):
    if filename.lower().endswith(".txt"):
        txt_path = os.path.join(txt_folder, filename)
        
        # Read TXT file
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        data = []
        for line in lines:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            
            # Split line by spaces
            parts = line.split()
            
            # If fewer than 4 elements, fill empty strings
            while len(parts) < 4:
                parts.append("")
            
            # If more than 4 elements, combine extras into the last column (DisplayAs)
            if len(parts) > 4:
                parts = parts[:3] + [" ".join(parts[3:])]
            
            data.append(parts[:4])
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        # Drop the IPA column
        df = df.drop(columns=["IPA"])
        
        # Save CSV
        base_name = os.path.splitext(filename)[0]
        csv_path = os.path.join(csv_folder, f"{base_name}.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"All TXT files from '{txt_folder}' have been converted to CSV files in '{csv_folder}' without the IPA column.")
