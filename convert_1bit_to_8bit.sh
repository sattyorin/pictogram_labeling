#!/bin/bash

input_dir="images"
output_dir="converted_images"

mkdir -p $output_dir

for file in "$input_dir"/*.png; do
  output_file="$output_dir/$(basename "$file")"
  
  convert "$file" -depth 8 -alpha remove -alpha off "$output_file"
  echo "Converted $file to $output_file"
done
