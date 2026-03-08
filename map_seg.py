#!/usr/bin/env python3
"""Remap pixel values in a NIfTI segmentation file."""

import argparse
import sys

import nibabel as nib
import numpy as np


def load_nifti(path: str) -> nib.Nifti1Image:
    img = nib.load(path)
    data = np.asarray(img.dataobj)
    min_val, max_val = int(data.min()), int(data.max())
    if min_val < 0 or max_val > 255:
        print(f"Error: pixel values must be in [0, 255], got [{min_val}, {max_val}]")
        sys.exit(1)
    return img, min_val, max_val


def get_mapping(min_val: int, max_val: int) -> dict[int, int]:
    mapping = {}
    for v in range(min_val, max_val + 1):
        while True:
            try:
                new_val = int(input(f"  {v} -> "))
                if 0 <= new_val <= 255:
                    mapping[v] = new_val
                    break
                print("    Value must be between 0 and 255.")
            except ValueError:
                print("    Please enter an integer.")
    return mapping


def remap(img: nib.Nifti1Image, mapping: dict[int, int]) -> nib.Nifti1Image:
    data = np.asarray(img.dataobj, dtype=np.uint8)
    lut = np.arange(256, dtype=np.uint8)
    for old, new in mapping.items():
        lut[old] = new
    remapped = lut[data]
    return nib.Nifti1Image(remapped, img.affine, img.header)


def main():
    parser = argparse.ArgumentParser(description="Remap pixel values in a NIfTI segmentation file.")
    parser.add_argument("input", help="Input NIfTI file path")
    parser.add_argument("output", help="Output NIfTI file path")
    args = parser.parse_args()

    img, min_val, max_val = load_nifti(args.input)
    data = np.asarray(img.dataobj)

    print(f"Pixel value range: {min_val} to {max_val}")
    print("Enter new value for each input value:")
    mapping = get_mapping(min_val, max_val)

    out_img = remap(img, mapping)
    nib.save(out_img, args.output)
    print(f"Saved remapped file to {args.output}")


if __name__ == "__main__":
    main()
