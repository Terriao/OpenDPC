<!-- ============================================================
File: .github/PULL_REQUEST_TEMPLATE.md
Repo: https://github.com/Terriao/OpenDPC
============================================================ -->

# Pull Request — OpenDPC

Thank you for contributing to OpenDPC. Please complete the relevant sections so reviewers can act efficiently.

## Summary

<!-- One-line summary of what this PR changes. -->

## Type of change

- [ ] Bug fix (non-breaking; fixes a reported issue)
- [ ] New feature in the dynamic point cloud player
- [ ] New feature in the JND annotation sub-platform
- [ ] PontZen preprocessing tool change
- [ ] V-PCC distortion-ladder configuration change (`ctc_configs/`)
- [ ] New / updated test sequence (`test_data/`)
- [ ] Documentation (README, FAQ, citation)
- [ ] Build / packaging change (Unity project, release archive)
- [ ] Refactor (no functional change)

## Related issue

<!-- Reference any issue this PR closes or addresses, e.g. Closes #7 -->

## Description

<!-- What problem does this PR solve, and how? Be concrete about the design choice and any
     trade-offs. For Unity changes, note the affected panels (Home / PlayerSettings / PlayerPlaying /
     JndSettings / JndPlaying / System). -->

## Reproducibility

<!-- If this PR changes behaviour observable to subjects, describe how a reviewer can reproduce
     the new behaviour locally. Include sample sequence path, JND config (viewing seconds, FPS,
     scale, search mode), and expected outputs. -->

- Test sequence used: ___________________
- Repro steps:
  1. ___________________
  2. ___________________

## Platform tested

- [ ] Windows 10
- [ ] Windows 11
- [ ] macOS (current release is Windows-only; mark only if porting)
- [ ] Linux (same as above)
- Unity Editor version: ___________________

## Pre-merge checklist

- [ ] The Unity scene compiles without errors (Editor + Standalone Windows build).
- [ ] The pre-built binary in `Software/software_v2.0.rar` was rebuilt and the change confirmed there.
- [ ] If the JND controller logic changed, the result-file format remains backward-compatible (or the change is documented in the README).
- [ ] Log files under `<install>/Logs/` still contain the full search trace.
- [ ] I updated the README section that describes the touched component.
- [ ] No personally identifiable subject data is included.

## Screenshots / Recordings (optional)

<!-- Drag-and-drop screenshots of the affected panels, or a short screen recording, here. -->

---

*Reviewed by:* @Terriao
