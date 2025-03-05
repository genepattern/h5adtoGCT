# H5adToGCT

A tool for converting h5ad files to GCT format.

## Description

H5adToGCT is a Python-based tool that converts AnnData (h5ad) files to Gene Cluster Text (GCT) format. This tool is particularly useful for single-cell RNA-seq data analysis workflows.

## Features

- Convert h5ad files to GCT format
- Include metadata fields in the output
- Specify which layer to use for expression values
- Verbose output option for detailed processing information

## Dependencies

The Docker image includes the following dependencies:
- Python 3.9
- scanpy
- pandas
- anndata
- h5py
- humanfriendly

## Docker Usage

### Building the Docker Image

To build the Docker image:

```bash
docker build -t h5adtogct .
```

This will create a Docker image based on Python 3.9-slim and install all necessary dependencies.

### Running the Docker Container

Basic usage:

```bash
docker run -v $(pwd):/data h5adtogct -i /data/your_file.h5ad
```

The output will be saved as `output.gct` in the current directory.

### Command Line Options

- `-i, --input`: Input h5ad file (required)
- `-m, --metadata`: Comma-separated list of metadata fields to include (optional)
- `-l, --layer`: Layer to use for expression values (default: use .X) (optional)
- `-v, --verbose`: Increase output verbosity (optional)

### Examples

Convert a file with verbose output:

```bash
docker run -v $(pwd):/data h5adtogct -i /data/your_file.h5ad -v
```

Include metadata fields:

```bash
docker run -v $(pwd):/data h5adtogct -i /data/your_file.h5ad -m "cell_type,batch"
```

Use a specific layer:

```bash
docker run -v $(pwd):/data h5adtogct -i /data/your_file.h5ad -l "normalized"
```

## Helper Script

A helper script `build_and_run.sh` is provided to simplify building and running the Docker container:

```bash
# Build the Docker image
./build_and_run.sh build

# Run the container
./build_and_run.sh run /path/to/your_file.h5ad -v

# Show help
./build_and_run.sh help
```

## GenePattern Module

This tool is also available as a GenePattern module. The module can be run through the GenePattern web interface or programmatically using the GenePattern API.

## License

[Add license information here] 