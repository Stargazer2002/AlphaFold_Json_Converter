import json
import argparse
import re
from pathlib import Path

def parse_fasta(fasta_file):
    """Parse a FASTA file and extract protein sequences with their identifiers."""
    proteins = []
    current_id = None
    current_sequence = []
    
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('>'):
                # Save the previous sequence if there is one
                if current_id is not None:
                    proteins.append({
                        'id': current_id,
                        'sequence': ''.join(current_sequence)
                    })
                
                # Start a new sequence
                current_id = line[1:]
                current_sequence = []
            else:
                # Add to the current sequence, removing whitespace and non-amino acid characters
                cleaned_line = re.sub(r'[^A-Za-z]', '', line)
                current_sequence.append(cleaned_line)
    
    # Add the last sequence
    if current_id is not None:
        proteins.append({
            'id': current_id,
            'sequence': ''.join(current_sequence)
        })
    
    return proteins

def create_alphafold_json(proteins, fixed_sequence, output_file, job_name_prefix="Fold Job"):
    """Create AlphaFold JSON format with the fixed sequence paired with each protein from the FASTA file."""
    jobs = []

    # Ensure the job_name_prefix only contains valid characters
    # Valid characters are: letters, numbers, spaces, dashes, underscores, colons
    valid_prefix = re.sub(r'[^A-Za-z0-9 \-_:]', '', job_name_prefix)
    
    for i, protein in enumerate(proteins, 1):
        # Create job entry with valid name
        job = {
            "name": f"{valid_prefix} No {i}",
            "modelSeeds": [],
            "sequences": [
                {
                    "proteinChain": {
                        "sequence": fixed_sequence,
                        "count": 1
                    }
                },
                {
                    "proteinChain": {
                        "sequence": protein["sequence"],
                        "count": 1,
                        # Adding empty lists for glycans and modifications for optional future editing
                        "glycans": [],
                        "modifications": []
                    }
                }
            ]
        }
        jobs.append(job)
    
    # Write to JSON file
    with open(output_file, 'w') as f:
        json.dump(jobs, f, indent=2)
    
    print(f"Created AlphaFold JSON file with {len(jobs)} jobs at {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Convert FASTA file to AlphaFold JSON format')
    parser.add_argument('fasta_file', help='Path to the input FASTA file')
    parser.add_argument('--fixed-sequence', required=True, help='Fixed protein sequence to pair with each FASTA sequence')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--job-prefix', default="Fold Job", help='Prefix for job names')
    
    args = parser.parse_args()
    
    # If output file is not specified, use the input file name with .json extension
    if not args.output:
        input_path = Path(args.fasta_file)
        args.output = str(input_path.with_suffix('.json'))
    
    # Parse FASTA file
    proteins = parse_fasta(args.fasta_file)
    print(f"Found {len(proteins)} protein sequences in the FASTA file")
    
    # Create AlphaFold JSON
    create_alphafold_json(proteins, args.fixed_sequence, args.output, args.job_prefix)

if __name__ == "__main__":
    main()