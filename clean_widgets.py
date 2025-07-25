# clean_widgets.py
import nbformat

# 1) Load your notebook (correct the filename here!)
fn_in  = "Challenge_1b_final_flan_t5_base.ipynb"      
fn_out = "Challenge_1b_final_flan_t5_base_clean.ipynb"
nb = nbformat.read(fn_in, as_version=nbformat.NO_CONVERT)

# 2) Remove only widget metadata (leaves outputs in place)
nb.metadata.pop("widgets", None)
for cell in nb.cells:
    cell.metadata.pop("widgets", None)

# 3) Write a cleaned copy
nbformat.write(nb, fn_out)
print("Wrote cleaned notebook to", fn_out)
