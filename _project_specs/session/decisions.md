<!--
LOG DECISIONS WHEN:
- Choosing between architectural approaches
- Selecting libraries or tools
- Making security-related choices
- Deviating from standard patterns

This is append-only. Never delete entries.
-->

# Decision Log

---

## [2026-03-07] Lookup table for value remapping

**Decision**: Use numpy LUT (lookup table) indexing for remapping
**Context**: Need to remap pixel values efficiently across potentially large 3D volumes
**Options Considered**: (1) Loop over unique values with masking, (2) np.vectorize, (3) LUT array indexing
**Choice**: LUT array indexing
**Reasoning**: O(1) per voxel, no branching, leverages numpy's vectorized indexing
**Trade-offs**: Requires values in [0, 255] range (which we validate)
**References**: map_seg.py:remap()
