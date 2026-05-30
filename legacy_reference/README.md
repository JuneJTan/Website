# Legacy Reference Archive

This folder keeps source material from the old website for future reference and migration.

## Folder Structure

- `OldVersion/`
  - Original old website HTML.
  - Main file: `OldVersion/index.htm`

- `figs/`
  - Image and PDF resources collected for the old website.
  - Includes SUSTech logo, department logo, lab logo, professor photo, ORCID icon, recruitment image, and `NEMO_2018_program.pdf`.

- `extracted_publications/`
  - Publication lists extracted from `OldVersion/index.htm`.
  - Includes Markdown files by category and `publications.json` for future structured import.

## Extracted Publication Counts

- Journal Papers: 110
- Books and Book Chapters: 4
- Conference Proceedings: 135
- Workshop and Invited Seminar Presentations: 35

## Notes

- The old HTML references some asset filenames that do not exactly match the files in `figs/`.
- During migration, match or rename assets carefully instead of assuming the old HTML paths already work.
- Keep this folder as a read-only reference source while building the new website.
