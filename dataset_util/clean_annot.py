import re
import argparse

def replace_file_name(input_file, output_file):
    # Read the content of the input file
    with open(input_file, 'r') as file:
        file_content = file.read()

    # Apply the regex replacement
    updated_content = re.sub(
        r'file_name": "batch_(\d+)/([^"]+)\.(jpg|JPG)"',
        r'file_name": "\1_\2.jpg"',
        file_content
    )

    # Write the updated content to the output file
    with open(output_file, 'w') as file:
        file.write(updated_content)

    print(f"File updated successfully and saved to {output_file}")

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Replace 'file_name' paths in a file.")
    parser.add_argument('input_file', type=str, help="Path to the input file")
    parser.add_argument('output_file', type=str, help="Path to the output file")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    replace_file_name(args.input_file, args.output_file)
