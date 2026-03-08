"""Tests for map_seg.py."""

import numpy as np
import nibabel as nib
import pytest

from map_seg import load_nifti, get_mapping, remap


def make_nifti(data: np.ndarray, tmp_path, filename="test.nii.gz") -> str:
    """Create a temporary NIfTI file and return its path."""
    path = str(tmp_path / filename)
    img = nib.Nifti1Image(data.astype(np.uint8), affine=np.eye(4))
    nib.save(img, path)
    return path


class TestLoadNifti:
    def test_valid_file(self, tmp_path):
        data = np.array([[[0, 1], [2, 3]]], dtype=np.uint8)
        path = make_nifti(data, tmp_path)
        img = load_nifti(path)
        loaded = np.asarray(img.dataobj)
        np.testing.assert_array_equal(loaded, data)

    def test_rejects_negative_values(self, tmp_path):
        data = np.array([[[-1, 0], [1, 2]]], dtype=np.int16)
        path = str(tmp_path / "neg.nii.gz")
        img = nib.Nifti1Image(data, affine=np.eye(4))
        nib.save(img, path)
        with pytest.raises(SystemExit):
            load_nifti(path)

    def test_rejects_values_above_255(self, tmp_path):
        data = np.array([[[0, 256]]], dtype=np.int16)
        path = str(tmp_path / "high.nii.gz")
        img = nib.Nifti1Image(data, affine=np.eye(4))
        nib.save(img, path)
        with pytest.raises(SystemExit):
            load_nifti(path)

    def test_accepts_boundary_values(self, tmp_path):
        data = np.array([[[0, 255]]], dtype=np.uint8)
        path = make_nifti(data, tmp_path)
        img = load_nifti(path)
        loaded = np.asarray(img.dataobj)
        np.testing.assert_array_equal(loaded, data)


class TestGetMapping:
    def test_basic_mapping(self, monkeypatch):
        inputs = iter(["0", "2", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        mapping = get_mapping(2)
        assert mapping == {0: 0, 1: 2, 2: 1}

    def test_identity_mapping(self, monkeypatch):
        inputs = iter(["0", "1", "2", "3"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        mapping = get_mapping(3)
        assert mapping == {0: 0, 1: 1, 2: 2, 3: 3}

    def test_single_value(self, monkeypatch):
        inputs = iter(["5"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        mapping = get_mapping(0)
        assert mapping == {0: 5}

    def test_rejects_invalid_then_accepts(self, monkeypatch):
        inputs = iter(["abc", "-1", "300", "42"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        mapping = get_mapping(0)
        assert mapping == {0: 42}


class TestRemap:
    def test_swap_values(self, tmp_path):
        data = np.array([[[0, 1, 2], [2, 1, 0]]], dtype=np.uint8)
        path = make_nifti(data, tmp_path)
        img = load_nifti(path)
        mapping = {0: 0, 1: 2, 2: 1}
        result = remap(img, mapping)
        expected = np.array([[[0, 2, 1], [1, 2, 0]]], dtype=np.uint8)
        np.testing.assert_array_equal(np.asarray(result.dataobj), expected)

    def test_all_to_same_value(self, tmp_path):
        data = np.array([[[0, 1, 2, 3]]], dtype=np.uint8)
        path = make_nifti(data, tmp_path)
        img = load_nifti(path)
        mapping = {0: 5, 1: 5, 2: 5, 3: 5}
        result = remap(img, mapping)
        expected = np.full_like(data, 5)
        np.testing.assert_array_equal(np.asarray(result.dataobj), expected)

    def test_preserves_affine(self, tmp_path):
        data = np.array([[[1, 2]]], dtype=np.uint8)
        affine = np.diag([2.0, 3.0, 4.0, 1.0])
        path = str(tmp_path / "affine.nii.gz")
        img = nib.Nifti1Image(data, affine=affine)
        nib.save(img, path)
        img = load_nifti(path)
        result = remap(img, {0: 0, 1: 10, 2: 20})
        np.testing.assert_array_equal(result.affine, affine)

    def test_unmapped_values_unchanged(self, tmp_path):
        """Values not in the mapping dict stay as-is (LUT identity)."""
        data = np.array([[[0, 5, 10]]], dtype=np.uint8)
        path = make_nifti(data, tmp_path)
        img = load_nifti(path)
        mapping = {0: 0, 5: 50, 10: 100}
        result = remap(img, mapping)
        expected = np.array([[[0, 50, 100]]], dtype=np.uint8)
        np.testing.assert_array_equal(np.asarray(result.dataobj), expected)

    def test_3d_volume(self, tmp_path):
        """Test with a realistic 3D volume shape."""
        rng = np.random.default_rng(42)
        data = rng.integers(0, 4, size=(10, 10, 10), dtype=np.uint8)
        path = make_nifti(data, tmp_path)
        img = load_nifti(path)
        mapping = {0: 3, 1: 2, 2: 1, 3: 0}
        result = remap(img, mapping)
        result_data = np.asarray(result.dataobj)
        # Verify every voxel
        for old, new in mapping.items():
            np.testing.assert_array_equal(result_data[data == old], new)


class TestEndToEnd:
    def test_round_trip(self, tmp_path, monkeypatch):
        """Full pipeline: create file, remap, verify output file."""
        data = np.array([[[0, 1, 2], [1, 0, 2]]], dtype=np.uint8)
        input_path = make_nifti(data, tmp_path, "input.nii.gz")
        output_path = str(tmp_path / "output.nii.gz")

        # Simulate user input: 0->0, 1->2, 2->1
        inputs = iter(["0", "2", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        img = load_nifti(input_path)
        mapping = get_mapping(int(np.asarray(img.dataobj).max()))
        out_img = remap(img, mapping)
        nib.save(out_img, output_path)

        # Load and verify output
        result = nib.load(output_path)
        result_data = np.asarray(result.dataobj)
        expected = np.array([[[0, 2, 1], [2, 0, 1]]], dtype=np.uint8)
        np.testing.assert_array_equal(result_data, expected)
