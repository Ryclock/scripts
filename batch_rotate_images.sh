#!/bin/bash

if ! command -v ffmpeg &> /dev/null; then
    echo "Error: FFmpeg is not installed. Please install FFmpeg and try again."
    exit 1
fi

if [ $# -lt 4 ]; then
    echo "Error: Please provide input folder, output folder, image format as command-line arguments."
    echo "Usage: $0 <input_folder> <output_folder> --format <image_format>"
    exit 1
fi

input_folder="$1"
output_folder="$2"
image_format="$4"

if [ ! -d "$input_folder" ]; then
    echo "Error: Input image folder does not exist."
    exit 1
fi

mkdir -p "$output_folder"

case "$image_format" in
    jpg|jpeg|png)
        ;;
    *)
        echo "Error: Unsupported image format: $image_format. Supported formats: jpg, jpeg, png"
        exit 1
        ;;
esac

shopt -s nullglob
for file in "$input_folder"/*."$image_format"; do
    if ! file --mime-type "$file" | grep -qE "image/(jpeg|png)"; then
        echo "Skipping non-image file: $file"
        continue
    fi
    filename=$(basename -- "$file")
    output_file="$output_folder/${filename%.*}_rotated.$image_format"

    if ! ffmpeg -i "$file" -vf "transpose=2" "$output_file"; then
        echo "Error: Failed to process file $file. Check FFmpeg installation and try again."
    fi
done

shopt -u nullglob
