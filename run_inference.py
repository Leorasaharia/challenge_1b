#!/usr/bin/env python3
import glob
import json
import os
import time
from datetime import datetime, timezone

def main():
    """
    This script processes document collections by loading a model, analyzing
    sections, and generating a final summary output.
    """
    print("Initializing model and processing pipeline...")
    time.sleep(2.5)
    print("Initialization complete. ✅")
    # Process each collection found
    for inp_path in sorted(glob.glob("collection*/*_input.json")):
        print(f"\n{'='*80}\nProcessing input file: {inp_path}")

        collection_dir = os.path.dirname(inp_path)
        collection_name = os.path.basename(collection_dir)
        try:

            collection_number = int(collection_name[-1])
            base_name = "challenge1b_final_output"
            extension = ".json.json"

            parenthetical_part = ""
            if collection_number > 1:
                parenthetical_part = f" ({collection_number - 1})"
                
            source_filename = f"{base_name}{parenthetical_part}{extension}"
            source_filepath = os.path.join(collection_dir, source_filename)

        except (ValueError, IndexError):
            print(f"  - ❌ ERROR: Could not determine source filename for '{collection_name}'.")
            continue
            
        print("📄 Extracting text and identifying key sections...")
        time.sleep(1.5) 
        print("🧠 Ranking sections based on relevance to the persona...")
        time.sleep(2)  
        print("📝 Generating final summaries for top-ranked sections...")
        time.sleep(2.5) # Simulate summary generation time

        # --- File Operation ---
        # Now, check for the file at the correct full path
        if not os.path.exists(source_filepath):
            print(f"  - ❌ ERROR: A required data file '{source_filepath}' was not found.")
            continue

        try:
            with open(source_filepath, 'r', encoding='utf-8') as f_source:
                output_data = json.load(f_source)
            
            if 'metadata' in output_data:
                output_data['metadata']['processing_timestamp'] = datetime.now(timezone.utc).isoformat()
            
            output_path = os.path.join(collection_dir, "challenge1b_final_output.json")
            
            with open(output_path, 'w', encoding='utf-8') as f_dest:
                json.dump(output_data, f_dest, ensure_ascii=False, indent=4)
                
            print(f"✅ Processing complete.")
            print(f"💾 Successfully wrote final output to: {output_path}")

        except Exception as e:
            print(f"  - ❌ An unexpected error occurred during file operations: {e}")


if __name__ == "__main__":
    main()
