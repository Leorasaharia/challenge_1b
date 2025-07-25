import sys
import os
import nbformat

def clean_notebook(fn_in):
    if not os.path.isfile(fn_in):
        print(f"Error: file not found: {fn_in}")
        sys.exit(1)

    # Derive the output filename
    base, ext = os.path.splitext(fn_in)
    fn_out = f"{base}_clean{ext}"

    # Load
    nb = nbformat.read(fn_in, as_version=nbformat.NO_CONVERT)

    # Strip code cell outputs and execution counts
    for cell in nb.cells:
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        # Remove any widget metadata
        cell.get("metadata", {}).pop("widgets", None)
        cell.get("metadata", {}).pop("jupyter", None)

    # Clean top-level
    nb.metadata.pop("widgets", None)
    nb.metadata.pop("jupyter", None)

    # Write cleaned copy
    nbformat.write(nb, fn_out)
    print(f"Wrote cleaned notebook to {fn_out}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    clean_notebook(sys.argv[1])
