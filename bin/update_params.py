#!/usr/bin/env python3
import argparse
import glob
import os
import xml.etree.ElementTree as ET


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-x",
        "--xml",
        type=str,
        default=None,
        required=True,
        help="Input parameter xml file",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=1,
        required=False,
        help="Number of threads to use",
    )
    parser.add_argument(
        "-f",
        "--fasta",
        type=str,
        default=None,
        required=True,
        help="Fasta file",
    )
    parser.add_argument(
        "-r",
        "--raw_folder",
        type=str,
        default=None,
        required=True,
        help="Folder containing the raw data.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="params.xml",
        help="Output file name, default params.xml",
    )
    args = parser.parse_args()
    return args


def main():
    """Automatically modify the params input file."""
    # Parse input
    args = _parse_args()

    # Parse the XML file using the parser object
    tree = ET.parse(args.xml)
    # Load the XML file
    root = tree.getroot()

    # set xsd xsi
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    # Find the elements that need to be modified
    fasta_file_path_elem = tree.find(".//fastaFilePath")
    num_threads_elem = tree.find("numThreads")

    # Modify the elements as needed
    fasta_file_path_elem.text = args.fasta
    num_threads_elem.text = str(args.threads)

    # Remove existing file paths
    old_file_paths = root.find("filePaths")
    for child in old_file_paths.findall("string"):
        old_file_paths.remove(child)

    # Add new file paths
    new_file_paths = glob.glob(f"{args.raw_folder}/*raw")

    for path in new_file_paths:
        new_file_path = ET.Element("string")
        new_file_path.text = path
        root.find("filePaths").append(new_file_path)

    # Remove existing experiments
    old_exp = root.find("experiments")
    for child in old_exp.findall("string"):
        old_exp.remove(child)

    # Add new file paths
    new_exp = [os.path.basename(x).strip("raw").strip("\.") for x in new_file_paths]

    for exp in new_exp:
        new_exp = ET.Element("string")
        new_exp.text = exp
        root.find("experiments").append(new_exp)

    # Save the modified XML file
    tree.write(args.output, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
