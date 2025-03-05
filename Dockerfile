FROM python:3.9-slim

LABEL maintainer="GenePattern Team"
LABEL description="Docker image for H5adToGCT module"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    scanpy \
    pandas \
    humanfriendly \
    anndata \
    h5py

# Create directory structure
RUN mkdir -p /usr/local/H5adToGCT

# Copy the wrapper script
COPY src/wrapper_script.py /usr/local/H5adToGCT/H5adToGCT.py

# Make the script executable
RUN chmod +x /usr/local/H5adToGCT/H5adToGCT.py

# Create an entrypoint script
RUN echo '#!/bin/bash\npython /usr/local/H5adToGCT/H5adToGCT.py "$@"' > /usr/local/bin/run_h5adtogct.sh && \
    chmod +x /usr/local/bin/run_h5adtogct.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/run_h5adtogct.sh"]

# Set working directory
WORKDIR /data