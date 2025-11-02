# CSV Import Workflow

```mermaid
flowchart TD
    A[Download one or more CSV files] --> B[Merge input files]
    B --> C{Do formats match?}
    C -- Yes --> D[Skip transformation]
    C -- No --> E[Transform merged CSVs]
    D --> F[Backup current Google Sheet]
    E --> F[Backup current Google Sheet]
    F --> G[Deduplicate against Sheet]
    G --> H[Import to Google Sheet]
```

This chart visualizes the process for importing and transforming multiple CSV files for organizations, including merging, deduplication, automated Google Sheet backup, and Google Sheets integration.

**Key workflow updates:**

- Use `--input-files` to specify a comma-separated list of CSVs to merge and process.
- Before any update, the current Google Sheet is backed up to `backups/` with a timestamped filename.
- Deduplication compares merged input data against the latest Google Sheet records.
- Data is imported and sorted in the target Google Sheet.