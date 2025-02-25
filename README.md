# AlphaFold_Json_Converter

## How to Use the Script

Run it from the command line with your FASTA file and fixed sequence:

```bash
python fasta_to_alphafold_json.py uniprotkb_accession_A0A0C5B5G6_OR_access_2025_02_25.fasta --fixed-sequence "YOURFIXEDSEQUENCE"
```

### Command Line Arguments

- fasta_file: Path to your input FASTA file (required)
- --fixed-sequence: The fixed protein sequence to pair with each FASTA sequence (required)
- --output: Custom output JSON file path (optional, defaults to input filename with .json extension)
- --job-prefix: Custom prefix for job names (optional, defaults to "Fold Job")

### Example

```bash
python fasta_to_alphafold_json.py uniprotkb_accession_A0A0C5B5G6_OR_access_2025_02_25.fasta --fixed-sequence "REACHER" --job-prefix "Protein Interaction"
```

This will create a JSON file with jobs pairing your fixed sequence "REACHER" with each protein from the FASTA file, using the name format "Protein Interaction No X" for each job.

The script includes placeholders for glycans and modifications, so you can easily add them later by editing the JSON file if needed.
