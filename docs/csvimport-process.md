# CSV Import Workflow

```mermaid
flowchart TD
    A[Download one or more CSV files] --> B[Merge input files]
    B --> C{Do formats match?}
    C -- Yes --> D[Skip transformation]
    C -- No --> E[Transform merged CSVs]
    D --> F[Backup current target]
    E --> F[Backup current target]
    F --> G[Deduplicate against existing records]
    G --> H[Import to target]
```

This chart visualizes the process for importing and transforming multiple CSV files for organizations, including merging, deduplication, automated backup, and integration with the target data store.

**Key workflow updates:**

- Use `--input-files` to specify a comma-separated list of CSVs to merge and process.
- Before any update, the current target data store is backed up to `backups/` with a timestamped filename.
- Deduplication compares merged input data against the latest records in the target data store.
- Data is imported and sorted in the target data store.