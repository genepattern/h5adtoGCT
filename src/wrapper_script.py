#!/usr/bin/env python3

import argparse
import os
import scanpy as sc
import pandas as pd
from timeit import default_timer as timer
import humanfriendly

beginning_of_time = timer()

parser = argparse.ArgumentParser(description='Convert h5ad file to GCT format')
parser.add_argument("-i", "--input", 
                    required=True,
                    help="Input h5ad file")
parser.add_argument("-m", "--metadata", 
                    default=None,
                    help="Comma-separated list of metadata fields to include")
parser.add_argument("-l", "--layer", 
                    default=None,
                    help="Layer to use for expression values (default: use .X)")
parser.add_argument("-v", "--verbose", 
                    action="store_true",
                    help="Increase output verbosity")

args = parser.parse_args()

# Use fixed output filename
output_file = "output.gct"

if args.verbose:
    print(f"Reading input file: {args.input}")
    print(f"Output will be written to: {output_file}")

# Read the h5ad file
adata = sc.read_h5ad(args.input)

if args.verbose:
    print(f"AnnData object: {adata}")
    print(f"Shape: {adata.shape}")

# Get expression matrix
if args.layer is not None and args.layer in adata.layers:
    if args.verbose:
        print(f"Using layer: {args.layer}")
    expr_matrix = pd.DataFrame(adata.layers[args.layer].toarray() if hasattr(adata.layers[args.layer], 'toarray') else adata.layers[args.layer], 
                              index=adata.obs_names, 
                              columns=adata.var_names)
else:
    if args.verbose:
        print("Using .X matrix")
    expr_matrix = pd.DataFrame(adata.X.toarray() if hasattr(adata.X, 'toarray') else adata.X, 
                              index=adata.obs_names, 
                              columns=adata.var_names)

# Get metadata fields
metadata_fields = []
if args.metadata:
    metadata_fields = [field.strip() for field in args.metadata.split(',')]
    if args.verbose:
        print(f"Including metadata fields: {metadata_fields}")

# Create description column
description = pd.Series("na", index=adata.obs_names)
if metadata_fields:
    for field in metadata_fields:
        if field in adata.obs.columns:
            description = description.astype(str) + "_" + adata.obs[field].astype(str)
    # Remove leading "na_" from description
    description = description.str.replace("^na_", "", regex=True)

# Write GCT file
with open(output_file, 'w') as f:
    # Write header
    f.write("#1.3\n")
    f.write(f"{expr_matrix.shape[0]}\t{expr_matrix.shape[1]}\n")
    
    # Write column headers
    f.write("NAME\tDescription\t" + "\t".join(expr_matrix.columns) + "\n")
    
    # Write data rows
    for idx, row in expr_matrix.iterrows():
        f.write(f"{idx}\t{description[idx]}\t" + "\t".join(map(str, row.values)) + "\n")

if args.verbose:
    print(f"GCT file written to {output_file}")

end_of_time = timer()
print("Conversion complete! Wall time elapsed:", humanfriendly.format_timespan(end_of_time - beginning_of_time))