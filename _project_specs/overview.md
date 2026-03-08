# Project Overview

## Vision
A CLI tool for remapping pixel values in NIfTI segmentation files. Useful for relabeling anatomical regions in medical image segmentations.

## Goals
- [x] Read NIfTI files and validate pixel range [0, 255]
- [x] Interactive prompt for value remapping
- [x] Write remapped NIfTI preserving spatial metadata
- [ ] Add tests

## Non-Goals
- GUI interface
- Batch processing (for now)
- Non-NIfTI format support

## Success Metrics
- Correctly remaps all pixel values
- Preserves NIfTI affine/header exactly
- Handles edge cases (empty files, single-value files)
