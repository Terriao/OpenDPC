# OpenDPC — Preprocess Tool (PontZen)

This folder contains **PontZen**, the standalone preprocessing executable that prepares raw dynamic point cloud sequences for GPU-resident playback in the OpenDPC viewer. The output of PontZen is the canonical input format consumed by the binary in [`../Software/`](../Software).

---

## 📦 Contents

```
preprocess_tool/
└── PontZen_v3.exe       ← Windows command-line preprocessing tool
```

---

## ❓ What it does

PontZen performs two transforms per frame, and only two:

### 1. Geometric normalisation

The frame's centroid is translated to the coordinate origin, and the geometry is then isotropically rescaled until it fits inside the unit sphere of radius 1. The normalisation removes the dependence of downstream viewing parameters (camera distance, model scale) on the absolute capture units — a sequence captured in millimetres and one captured in metres will render at the same apparent size.

### 2. Attribute bit-packing

The four attribute channels per point — **R**ed, **G**reen, **B**lue, and a derived **luminance** — are encoded into a single 32-bit unsigned integer:

| Bits | 0 – 7 | 8 – 15 | 16 – 23 | 24 – 31 |
|:---:|:---:|:---:|:---:|:---:|
| Channel | R | G | B | Luminance |

Packing four 8-bit channels into one 32-bit integer halves the per-point upload bandwidth and, more importantly, lets the entire preprocessed sequence be uploaded to VRAM in one pass and indexed per frame at playback time without further memory copies. The arithmetic cost (one shift-and-mask per channel per shader invocation) is negligible relative to the bandwidth saved.

---

## 🎯 Why a separate tool

We split PontZen out of the Unity application on purpose:

- The preprocessing step is **single-pass, deterministic, and dataset-wide** — bundling it inside the viewer would force a re-pack every time the user opens a sequence.
- Keeping it standalone lets the same packed output be **reused across many sessions, many subjects, and many studies** without ever re-running the conversion.
- The renderer and the preprocessor can therefore be **ported independently** — a relevant property for the planned macOS / Linux builds.

---

## 🚀 Usage

### Prerequisites

- 64-bit **Windows** (10 / 11).
- Per-frame point cloud files for one sequence, lexicographically ordered (`0001.ply` … `NNNN.ply`).

### Workflow

1. Place the raw per-frame files of one sequence in a single source folder.
2. Run `PontZen_v3.exe`.
3. Supply the source folder and an output folder when prompted.
4. PontZen processes each frame in turn and writes the packed output to the output folder.
5. Point the OpenDPC viewer (or the JND sub-platform's *Reference Folder* / *Distortion Ladder Folder* fields) at the **output** folder.

```text
raw point clouds            PontZen_v3.exe              packed sequence
─────────────────   ───────────────────────────►   ────────────────────
0001.ply                                              0001.ply  (packed)
0002.ply                  centre + unit-sphere        0002.ply  (packed)
0003.ply       ───►          + 32-bit RGBL pack   ───►   0003.ply  (packed)
   …                                                       …
```

For the 18 test sequences shipped with the project (see [`../test_data/`](../test_data)), the PontZen step has already been performed — those sequences load directly into the viewer with no further preprocessing.

---

## ⚙️ Implementation notes

- **Single-pass and deterministic.** Re-running PontZen on the same input produces byte-identical output.
- **Lossless on attributes.** The RGB-plus-luminance channels are quantised to 8 bits each, which is the same precision the underlying captures already carry; no perceptually meaningful information is discarded.
- **Lossless on geometry, up to a similarity transform.** The centre + unit-sphere rescale is invertible — the original geometry can be recovered if the per-sequence translation vector and scale factor are recorded (PontZen writes these to a small sidecar metadata file alongside the packed frames).
- **No external dependencies.** Ships as a single `.exe` — no DLL chain, no installer, no admin privileges required.

---

## 🖥️ Platform notes

- **Windows-only for now.** The Unity-side player has the same constraint; both will move to macOS / Linux on the same milestone (see project [roadmap](../README.md#roadmap)).
- **No GPU required.** PontZen runs entirely on the CPU; the GPU is only used downstream by the viewer.
- **Out-of-process by design.** Even when the player and PontZen ship together in a future release, they will remain separate executables for the reusability reasons described above.

---

## 🧰 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `PontZen_v3.exe` exits immediately | Input folder empty or path contains Unicode | Use an ASCII-only path; verify the folder contains `.ply` frames |
| Output folder is empty after a run | Output path is read-only or full | Pick a writable output location with sufficient disk space |
| Viewer reports "frame count mismatch" between reference and distortion ladder | A subset of rate-point folders was preprocessed before adding new reference frames | Re-run PontZen on **all** rate-point folders and the reference together |
| Player loads packed frames but renders black | Sequence was preprocessed by an older PontZen version with a different bit layout | Re-run with `PontZen_v3.exe` (current); regenerate the packed sequence |

If a problem persists, please file an [issue](https://github.com/Terriao/OpenDPC/issues) with the source folder size, the PontZen console output, and a short description of the input format.

---

## 📚 Citation

If PontZen and OpenDPC support your research, please cite:

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

Preprocessing bugs, feature requests, or porting questions:
**Asso. Prof. Wei Gao** — `gaowei262@pku.edu.cn` · [GitHub Issues](https://github.com/Terriao/OpenDPC/issues)
