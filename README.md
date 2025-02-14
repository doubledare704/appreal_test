# CSV and Regex Processing Scripts

This project includes two Python scripts for processing CSV files:
1. **`csv-task.py`**: Converts a TSV (Tab-Separated Values) file to a CSV, with an additional column based on a price transformation.
2. **`regex-task.py`**: Filters products with "Knit" in their name (excluding "Knit Jumper") from a CSV file.

## Requirements

The following Python packages are required:

- `pandas` (or the version you're using)
- Python 3.8+

You can install the required packages using:

```bash
pip install -r requirements.txt
```

## Scripts

1. **`csv-task.py`**: Convert TSV to CSV with Price Transformation.
- This script converts a TSV file to a CSV file, while also adding a new column, price_edited, which is derived from the rrp_price column.
```bash 
  python csv-task.py --infile <input_tsv_file> --out <output_csv_file>
  ```
2. **`regex-task.py`**: Filter Knit Products (Excluding Jumpers)
- This script filters products that contain the word "Knit" in their name, but excludes those with the word "Jumper". The filtered results are saved to a new CSV file.
```bash 
python regex-task.py --infile <input_csv_file> --out <output_csv_file>
```

# Design task

### Change Detection Mechanism

To avoid reprocessing unchanged products, we store **product hashes** in a **state-tracking database** (e.g., PostgreSQL, Redis). This allows us to:
- Detect which products have changed.
- Identify new and removed products efficiently.

#### Steps:
1. Generate a **hash** (e.g., SHA256) for each product’s relevant fields:
   - `product_id`
   - `price`
   - `in_stock`
   - `image_checksum` (based on image content)
2. Store these hashes in a **persistent key-value store** (e.g., Redis).
3. Compare new catalog hashes with previous ones to categorize products:
   - **Unchanged:** Skip processing.
   - **Metadata Changed:** Update only the relevant fields.
   - **Image Changed:** Rerun image processing for new deep tags.
   - **New Product:** Full processing and indexing.
   - **Removed Product:** Remove from Elasticsearch.

### Incremental Updates to Elasticsearch

Instead of creating a new index for every update, we use **partial updates** to modify only the changed records.

#### Steps:
1. Use **Elasticsearch’s `_update_by_query` API** to update only modified records.
2. Utilize **bulk indexing** to minimize API calls and improve performance.
3. Delete removed products using **soft deletes** (mark as `is_deleted = true`) before permanent deletion.

### Efficient Image Processing for Deeptags

To avoid reprocessing unchanged images, we use **image hashing** (e.g., Perceptual Hashing, MD5) to detect changes and only rerun the deep tagging algorithm when necessary.

#### Steps:
1. Extract **image features** and generate an **image hash**.
2. Compare the new image hash with the previously stored hash.
3. If the hash is unchanged, reuse the previously generated deep tags.
4. If the hash has changed, run the deep tagging algorithm and store the new deep tags.

### Index Versioning & Atomic Swaps

To ensure a **seamless switch** between old and new data, we use **alias-based swapping** in Elasticsearch, maintaining a staging index before applying changes.

#### Steps:
1. Create a **new index (`catalog_v2`)** and apply incremental updates.
2. Once updates are complete, **swap aliases** to point to the new index:
   ```json
   POST /_aliases
   {
     "actions": [
       { "remove": { "alias": "catalog_current", "index": "catalog_v1" } },
       { "add": { "alias": "catalog_current", "index": "catalog_v2" } }
     ]
   }
3. Delete old indices after confirming the switch.