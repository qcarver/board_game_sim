#!/bin/bash

output_file="regular_files_in_$(basename "$PWD").txt"

# Write instructions at the beginning of the file
echo "This file contains the concatenated contents of all regular (non-binary) files in the current directory." > "$output_file"
echo "Each file's content is preceded by a banner with the filename." >> "$output_file"
echo "Use this file to review or process the combined content of all files." >> "$output_file"
echo "" >> "$output_file"

for file in *; do
    if [ -f "$file" ] && ! file "$file" | grep -q "binary"; then
        echo "========================================" >> "$output_file"
        echo "Filename: $file" >> "$output_file"
        echo "========================================" >> "$output_file"
        cat "$file" >> "$output_file"
        echo "" >> "$output_file"
    fi
done

echo "All regular (non-binary) files have been concatenated into $output_file"