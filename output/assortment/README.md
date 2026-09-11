# Assortment source export — 18 June 2026 workbook

Source: `Assortment confirmation list with names 260618_1.xlsx` in the user-supplied `products ` directory. The older 251105 workbook mentioned in the request was not supplied; these exports describe the June file only.

- `tabs/`: all nine sheets in original order, preserving the cell grid, multi-line cells, original headers, notes and totals. Empty Sheet2 and Sheet1 are retained as a quoted blank cell.
- `assortment_options.csv`: 1,191 nonempty option lines from Names, 12mm, 6mm, Subsize and Mosaic. Summary/total rows are excluded from this index, but remain in the faithful tab exports. A multi-line cell creates multiple option rows sharing the same source cell. These are **option observations, not 1,191 SKUs or products**.
- `manifest.json`: source SHA-256, sheet dimensions, names and export policy.
- `formula_metadata.json`: 57 original formulas and cached values. Tab CSVs use source cached values; they have not been recalculated.
- The local source-review pack also retains `media/` and `media_index.json`: 112 original embedded images and 300 drawing anchors. This GitHub folder publishes the CSV grids and metadata; selected browser previews are included with the Studio. Anchors alone do not prove product identity.

Encoding is UTF-8 with BOM, comma delimiter, CRLF records, and RFC-style double-quote escaping. Original workbook formatting, merged ranges, comments, image positioning and spreadsheet calculations cannot be represented by CSV; retain the original XLSX as evidence.

`Names` contains reference and proposed names. `12mm` and `6mm` use marketing and technical finish headers on separate rows. `Subsize` includes multiple sizes per cell and a 20 mm column. `Mosaic` uses a different header layout. The option index retains both headers and raw text. Blank marketing headers are not filled into neighbouring finishes. Units, lifecycle, stock, final SKU and Merch priority are not inferred from checkmarks or notes.

Verification: all nine exported tab grids were compared cell-for-cell with the source workbook's cached values. Source formulas are retained here. Original embedded images remain in the local source-review pack.

For operational use, create a reviewed product master with stable product/color/SKU IDs, dimensions in millimetres, controlled finish IDs, lifecycle, positioning and an independent Hit flag. Keep this export as an import/staging source.
