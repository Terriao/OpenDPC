# OpenDPC — Software

This folder contains the **pre-built Windows binary** of OpenDPC, ready for end users who only want to run the player and the JND annotation sub-platform (no Unity Editor required).

For the project background, system architecture, and subjective-experiment protocol, see the [main README](../README.md).

---

## 📦 Contents

```
Software/
└── software_v2.0.rar       ← compressed archive containing the full Unity build
```

Once extracted, the archive expands into:

```
software_v2.0/
├── JNDModelStreamViewer.exe                ← double-click to launch
└── JNDModelStreamViewer_Data/              ← Unity runtime assets
    ├── Managed/
    ├── Resources/
    ├── StreamingAssets/
    ├── boot.config
    ├── globalgamemanagers
    └── …
```

> ℹ️ The executable is named `JNDModelStreamViewer.exe` for historical reasons — the JND sub-platform was the first component built. The two names (`OpenDPC` / `JNDModelStreamViewer`) refer to the same application; alignment is on the to-do list for the next public build.

---

## 🚀 Quick start

### Prerequisites

| Item | Minimum | Recommended |
|---|---|---|
| OS | 64-bit **Windows 10** | Windows 11 |
| GPU | Discrete, OpenGL 4.x / DirectX 11 | NVIDIA RTX 3060+ |
| VRAM | 4 GB | 8 GB+ — needed for JND Mode, which holds **two sequences simultaneously** |
| Disk | ~500 MB (binary) + 10s of GB for the test data | + a fast SSD |
| Archive utility | [WinRAR](https://www.win-rar.com/) / [7-Zip](https://www.7-zip.org/) | 7-Zip ≥ 21.0 |

### Install and launch

1. Download [`software_v2.0.rar`](software_v2.0.rar) from this folder.
2. Extract anywhere (e.g. `C:\OpenDPC\`).
3. Double-click `JNDModelStreamViewer.exe`.
4. The **Home Panel** appears — pick `Player Mode` or `JND Mode`.

### Smoke test in 60 seconds

1. Grab one test sequence from [`../test_data/`](../test_data) (see that folder's README for the Google Drive download).
2. Preprocess it with [`../preprocess_tool/PontZen_v3.exe`](../preprocess_tool/PontZen_v3.exe).
3. In OpenDPC, open Player Mode, point at the preprocessed sequence folder, click *Start*. Playback should loop smoothly at the default 15 fps.

---

## 🧭 Operating modes

### Player Mode

A single-pane dynamic point cloud viewer.

- **Inputs.** One folder of per-frame `.ply` files, lexicographically ordered (`0001.ply` … `NNNN.ply`).
- **Controls.** `Space` — pause / resume · left-drag — rotate model · scroll wheel — zoom · *Settings* tab — live FPS change.
- **Use case.** Visual inspection, demos, screencasts, sanity-checking a sequence before submitting it to JND.

### JND Mode

A paired-comparison annotation harness driven by a search controller over the V-PCC distortion ladder.

- **Inputs.** A *reference* folder and a *distortion-ladder parent folder* (the harness auto-discovers `r01/` … `r20/` subfolders).
- **Configurable parameters.** Viewing seconds (default 6 s), FPS (default 15), model scale (default 3×), search mode.
- **Search modes.**
  - **Dichotomizing** *(default)* — ternary-refinement controller on the rate-point ladder; converges in 4–5 paired comparisons per sequence.
  - **Linear** — exhaustive r1 → r20 walk; ~20 comparisons per sequence; reserved for ground-truth calibration.
- **Outputs.** A *result file* (per-subject JND rate point per sequence) and a *session log* under `<install>/Logs/`.

---

## 🖥️ Platform notes

- **Windows-only for now.** The current build uses native Win32 file dialogs (`VistaFileDialog`, `SHBrowseForFolder`). The Unity codebase is portable; macOS and Linux builds are on the project [roadmap](../README.md#roadmap), blocked only on substituting `Standalone File Browser` for the native Windows calls.
- **No installer.** The build is a portable folder — no admin privileges, no registry writes; delete the extracted folder to uninstall.
- **Antivirus false positives.** Some antivirus engines flag fresh, unsigned Unity executables. If a warning appears, verify the SHA-256 against the published value in the Releases page before whitelisting.

---

## 🧰 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Window opens, then immediately closes | Missing DirectX runtime or out-of-date GPU driver | Update GPU driver; install the latest DirectX redistributable |
| Paired-comparison view freezes after a few trials | VRAM exhausted (JND Mode holds 2 sequences at once) | Reduce sequence point count or use a GPU with more VRAM |
| `Sequence folder not found` | Path contains Unicode the Unity build does not handle | Move the folder to a path with ASCII-only characters |
| Verdict buttons stay disabled | The 6-second dwell timer has not elapsed yet | Wait for the timer (intentional anti-reflex measure) |
| No `Logs/` directory | First run has not yet completed | Run a full session; the directory is created on first write |

If a problem persists, please file an [issue](https://github.com/Terriao/OpenDPC/issues) with:
- Windows version (`winver`)
- GPU model and driver version (`dxdiag`)
- The `<install>/Logs/` file from the failing session
- Steps to reproduce

---

## 🏗️ Build provenance

`software_v2.0.rar` was produced from the Unity project source under the same MIT licence as the rest of OpenDPC.

- **Engine.** Unity 2022.3 LTS
- **Build target.** Standalone Windows 64-bit, Mono backend
- **Default Product Name.** `JNDModelStreamViewer` (see note at the top)

Developers who want to modify the application source — change panels, swap the search controller, port to another platform — should clone the upstream repository's Unity project rather than working from this binary.

---

## 📚 Citation

If this binary supports your research, please cite the accompanying paper:

```bibtex
@inproceedings{gao2026opendpc,
  title     = {OpenDPC: An Open Source Dynamic Point Cloud Player and Platform
               for Just Noticeable Distortion},
  author    = {Gao, Wenxu and Fan, Songlin and Gao, Wei},
  booktitle = {Proceedings of the 34th ACM International Conference on Multimedia},
  year      = {2026},
  note      = {Under review}
}
```

---

## ✉️ Contact

Build issues, feature requests, or collaboration enquiries:
**Asso. Prof. Wei Gao** — `gaowei262@pku.edu.cn` · [GitHub Issues](https://github.com/Terriao/OpenDPC/issues)
