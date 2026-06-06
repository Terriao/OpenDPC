<div align="center">

<img src="opendpc.png" alt="OpenDPC" width="780"/>

**An open-source dynamic point cloud player and a paired-comparison platform for just-noticeable-distortion annotation**

[![Engine](https://img.shields.io/badge/built%20on-Unity-000000?logo=unity&logoColor=white)](#)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)
[![Paper](https://img.shields.io/badge/ACM%20MM-2026%20(under%20review)-orange)](#citation)
[![Demo](https://img.shields.io/badge/demo-online-success)](https://docs.google.com/presentation/d/1kI2ak1zXNcYN4-CCj-AFejLzboaM6lWH/edit?usp=sharing)

**🔗 GitHub:** <https://github.com/Terriao/OpenDPC>

</div>

---

## Why this project exists

A dynamic point cloud is a *sequence* of point clouds — one per frame — and the format has matured into a serious 3D representation for VR, autonomous-driving telemetry, volumetric telepresence, and immersive cultural-heritage capture. The ecosystem around it, however, has lagged. Almost every viewer in circulation is a static-point-cloud tool patched to accept a folder of `.ply` files, breaking the moment a sequence runs past a few hundred frames or carries non-trivial colour attributes. And almost every JND or perceptual study on dynamic point clouds is run on bespoke, never-released code, so the next group has to rebuild the apparatus before it can rebuild the science.

OpenDPC is one Unity-based project that addresses both gaps at once:

1. **A real dynamic point cloud player** — frame-rate-correct, GPU-resident, interactive, looped, and built to handle full-length sequences without stuttering.
2. **A subjective JND annotation harness** — a paired-comparison interface for locating the lowest V-PCC rate point at which distortion crosses the perceptual threshold, on a per-sequence per-subject basis.

> *"Dynamic point clouds need playback infrastructure that is as boring and as reliable as a video player — and a perceptual-evaluation layer that does not get rebuilt every time a paper is written. OpenDPC tries to be both."*

---

## Contents

1. [At a glance](#at-a-glance)
2. [System architecture](#system-architecture)
3. [Getting started](#getting-started)
4. [The player in detail](#the-player-in-detail)
5. [The JND sub-platform in detail](#the-jnd-sub-platform-in-detail)
6. [Test sequences and V-PCC quality tiers](#test-sequences-and-v-pcc-quality-tiers)
7. [Subjective experiment and results](#subjective-experiment-and-results)
8. [Use cases](#use-cases)
9. [Roadmap](#roadmap)
10. [FAQ](#faq)
11. [Citation](#citation)
12. [Community](#community)
13. [License](#license)
14. [Acknowledgements](#acknowledgements)
15. [Contributors and contact](#contributors-and-contact)

---

## At a glance

| | Component | One-line description |
|---|---|---|
| 1 | **Dynamic point cloud processor** | A pre-rendering step that normalises geometry and bit-packs RGB-plus-luminance into a single 32-bit integer per point, ready for the GPU. |
| 2 | **Dynamic point cloud player** | Real-time looping playback of `.ply` sequences with pause / resume, frame counter, configurable FPS, free rotation, and free zoom. |
| 3 | **JND annotation sub-platform** | A side-by-side reference-versus-distorted viewer with synchronised camera and a ternary-search controller that converges on the perceptual threshold across a 20-rate distortion ladder. |

All three components share the same Unity project and the same data preprocessing path, so a sequence ingested once is ready for either playback or perceptual evaluation.

---

## System architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Dynamic point cloud assets                    │
│            (per-frame .ply files; one folder per sequence)           │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │   ❶ Dynamic point cloud       │
                  │      processor                │
                  │  · centring + unit-sphere     │
                  │    scaling                    │
                  │  · 32-bit RGB+luminance pack  │
                  └───────────────┬───────────────┘
                                  │  GPU buffers
                  ┌───────────────┴───────────────┐
                  │                               │
       ┌──────────▼──────────┐          ┌─────────▼──────────┐
       │  ❷ Player           │          │  ❸ JND sub-platform │
       │  · loop playback    │          │  · paired view      │
       │  · pause / resume   │          │  · synced camera    │
       │  · FPS control      │          │  · ternary search   │
       │  · rotate / zoom    │          │  · 6 s dwell timer  │
       └─────────────────────┘          └────────────────────┘
```

---

## Getting started

**Prerequisites.** Unity 2022.3 LTS or later. A discrete GPU with ≥ 4 GB VRAM is recommended for sequences longer than 200 frames or denser than 10⁶ points per frame.

**Clone and open.**

```bash
git clone https://github.com/Terriao/OpenDPC.git
```

Open the project root in Unity Hub → *Open* → *Add project from disk*. Let Unity import; the first import resolves shaders and asset references and takes a few minutes.

**Prepare a sequence.** Place the per-frame `.ply` files of one sequence in a single folder, ordered lexicographically (`0001.ply`, `0002.ply`, …). The processor will pick them up automatically when you point the player at the folder.

**Run the player.** Open the `Player` scene → Press Play → select the sequence folder in the settings panel → click *Start*. Playback begins immediately at the configured FPS.

**Run the JND harness.** Open the `JNDViewer` scene → select the reference folder and the distortion-ladder folder → set viewing seconds, FPS, and model scale if you want non-default values → click *Start*. The harness then drives the ternary-search loop described below.

---

## The player in detail

<p align="center"><img src="player.png" alt="OpenDPC dynamic point cloud player" width="640"/></p>

The player is built around three design constraints we found missing in existing tools:

1. **Streaming-friendly memory.** Each `.ply` frame is pre-processed into a tightly-packed GPU buffer where the four-channel colour (R, G, B, luminance) is encoded as one 32-bit unsigned integer per point — bits 0–7 for R, 8–15 for G, 16–23 for B, 24–31 for luminance. The full sequence is uploaded to VRAM once and indexed per frame at playback time. The arithmetic is cheap; the memory bandwidth saved is real.

2. **Camera-anchored model.** Each frame is rendered onto a single empty model placed at the camera origin, which means rotation and zoom interact intuitively with the model rather than with the world. Pause does not freeze the camera — you can keep inspecting the geometry from any angle while a frame holds.

3. **Frame counter + adjustable FPS.** A persistent overlay shows the current frame index and the total length of the sequence. The settings panel lets you change the playback rate without restarting the viewer.

Interactive controls during playback:

| Action | Input |
|---|---|
| Pause / resume | `Space` or the play/pause icon |
| Rotate model | Left-drag |
| Zoom | Scroll wheel |
| Change FPS | Settings panel (live) |

---

## The JND sub-platform in detail

<p align="center"><img src="jndviewer.png" alt="JND sub-platform configuration"  width="640"/></p>

### Configuration

The configuration screen exposes the parameters that previous JND-on-video studies have shown to dominate inter-subject variance:

| Parameter | Default | What it controls |
|---|---|---|
| **Viewing seconds** | 6 s | Minimum time the subject must observe each comparison before the verdict buttons unlock. Prevents reflex clicks and gives temporal masking time to settle. |
| **FPS** | 15 fps | Playback rate during evaluation. Lower than typical real-time playback to keep per-frame attention high. |
| **Model scale** | 3× | Apparent size of the model. Held constant so that retinal projection is comparable across subjects and sessions. |
| **Reference folder** | — | The pristine sequence. |
| **Distortion ladder folder** | — | A folder of subfolders, one per rate point, sorted by ascending distortion. |

### The viewer

<p align="center"><img src="jnd.png" alt="JND paired-comparison view" width="640"/></p>

The viewer shows the pristine sequence on the left and the candidate distorted sequence on the right. Crucially, **the two cameras are locked**: any rotation or zoom applied to one side is mirrored on the other, so the subject is never comparing apples and oranges at different angles. Two verdict buttons sit between the panels: `Similar` and `Different`.

### The ternary-search controller

Locating the JND boundary in a twenty-point distortion ladder by exhaustive comparison would need twenty trials per subject per sequence. We use a **ternary refinement** instead of a pure bisection, which is gentler on the noisy verdicts that subjective experiments inevitably produce:

```
Initial interval: [r1, r20]            (whole ladder)
Loop until interval has length 1:
    candidate ← midpoint of interval
    show paired comparison: reference vs candidate
    wait for verdict (button unlocks after 6 s)
    if verdict = "Similar":            -->  trim left third of interval
    if verdict = "Different":          -->  trim right third of interval
Output: lower end of the final interval = subject's JND rate point
```

Trimming **a third** rather than a half at each step costs a small number of extra comparisons relative to plain bisection — but the surplus dampens the noise that comes from low-confidence verdicts near the threshold, and the rate point the controller settles on lands closer to the true JND across our subject pool. A more aggressive halving converges faster but is brittle when the subject is uncertain on the very comparison that drives the next decision.

---

## Test sequences and V-PCC quality tiers

The repository ships a curated library of eighteen dynamic models sourced from Sketchfab, covering objects, characters, and animals (see thumbnails below). For each model, the first 64 frames are encoded by **V-PCC** at twenty rate points spanning nine quality tiers — from lossless down to very-low-quality. Five of the twenty rate points align with the **MPEG V-PCC Common Test Conditions** (CTC R1 through R5), so OpenDPC results are directly comparable to standardisation reports.

<p align="center"><img src="samples.png" alt="18 test sequences" width="640"/></p>

### V-PCC rate-point configuration

| Rate point | occupancyPrecision | Geometry QP | Attribute QP | Quality tier |
|:---:|:---:|:---:|:---:|:---|
| r1  | 2 | −12 | 0  | Lossless |
| r2  | 2 | −6  | 6  | Near-lossless |
| r3  | 2 | 0   | 9  | Near-lossless |
| r4  | 2 | 4   | 12 | High fidelity |
| r5  | 2 | 8   | 16 | High fidelity |
| r6  | 2 | 12  | 20 | High fidelity |
| r7  | 4 | 16  | 22 | High quality · **CTC R1** |
| r8  | 4 | 17  | 23 | High quality |
| r9  | 4 | 18  | 24 | High quality |
| r10 | 4 | 20  | 27 | Medium-high quality · **CTC R2** |
| r11 | 4 | 21  | 29 | Medium-high quality |
| r12 | 4 | 22  | 30 | Medium-high quality |
| r13 | 4 | 24  | 32 | Medium quality · **CTC R3** |
| r14 | 4 | 25  | 33 | Medium quality |
| r15 | 4 | 26  | 34 | Medium quality |
| r16 | 4 | 28  | 37 | Medium-low quality · **CTC R4** |
| r17 | 4 | 29  | 38 | Medium-low quality |
| r18 | 4 | 30  | 39 | Medium-low quality |
| r19 | 4 | 32  | 42 | Low quality · **CTC R5** |
| r20 | 4 | 36  | 48 | Very-low quality |

Total compressed asset size: 18 sequences × 20 rate points × 64 frames = **23,040 distorted frames** ready for evaluation.

### Asset preparation pipeline

Source `.glb` models from Sketchfab were converted to colour-bearing `.ply` sequences in two stages:

```
.glb (Sketchfab)  ──Blender──►  .obj + textures  ──CloudCompare batch──►  .ply sequence
```

We made the conversion batch-scriptable rather than interactive, so adding new sequences to the test library is a single command.

---

## Subjective experiment and results

### Protocol

We split the 18 sequences into two non-overlapping groups (A–I and J–R) and recruited **sixty volunteers**, thirty per group. The pool mixed multimedia-research-trained subjects with naive participants to keep generalisation honest. Before any data was collected, every subject went through a calibration session covering the protocol, the interface, and the verdict semantics; subjects could request a break at any point during the actual experiment to reduce visual fatigue.

Outlier verdicts were trimmed under the **ITU-R BT.500-13** screening rule before averaging.

### Per-subject JND results, group 1 (sequences A–I, subjects 1–30)

> **Read this table as:** "For sequence A, subject 1 found the distortion first noticeable at rate point r20; subject 2 at r16; …". Lower numbers mean tighter perceptual thresholds.

| Seq | s1 | s2 | s3 | s4 | s5 | s6 | s7 | s8 | s9 | s10 | s11 | s12 | s13 | s14 | s15 | s16 | s17 | s18 | s19 | s20 | s21 | s22 | s23 | s24 | s25 | s26 | s27 | s28 | s29 | s30 | **Mean** | **Std** |
|:---:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| A | 20 | 16 | 16 | 9  | 12 | 19 | 19 | 14 | 18 | 19 | 5  | 13 | 8  | 20 | 8  | 12 | 12 | 16 | 7  | 13 | 15 | 16 | 18 | 20 | 9  | 18 | 10 | 12 | 7  | 8  | **13.63** | 4.60 |
| B | 16 | 13 | 13 | 15 | 9  | 7  | 16 | 13 | 13 | 14 | 7  | 11 | 12 | 10 | 12 | 7  | 9  | 12 | 9  | 9  | 9  | 9  | 9  | 16 | 7  | 7  | 5  | 9  | 5  | 9  | **10.40** | 3.20 |
| C | 13 | 12 | 16 | 16 | 6  | 14 | 19 | 7  | 9  | 14 | 10 | 14 | 14 | 20 | 16 | 7  | 7  | 14 | 20 | 9  | 14 | 7  | 7  | 19 | 9  | 13 | 12 | 12 | 7  | 12 | **12.30** | 4.21 |
| D | 16 | 11 | 15 | 13 | 14 | 13 | 16 | 12 | 7  | 13 | 9  | 15 | 7  | 9  | 15 | 7  | 9  | 16 | 11 | 13 | 13 | 7  | 7  | 13 | 14 | 12 | 12 | 12 | 12 | 8  | **11.70** | 2.97 |
| E | 13 | 5  | 9  | 14 | 7  | 14 | 18 | 16 | 7  | 14 | 7  | 14 | 14 | 14 | 16 | 7  | 7  | 16 | 9  | 9  | 9  | 7  | 7  | 13 | 11 | 9  | 7  | 7  | 5  | 7  | **10.40** | 3.84 |
| F | 16 | 5  | 7  | 14 | 12 | 16 | 16 | 14 | 10 | 16 | 9  | 13 | 11 | 15 | 9  | 10 | 9  | 14 | 7  | 9  | 14 | 7  | 9  | 13 | 12 | 16 | 9  | 12 | 7  | 7  | **11.27** | 3.36 |
| G | 19 | 9  | 14 | 16 | 20 | 18 | 20 | 16 | 15 | 20 | 7  | 16 | 20 | 20 | 18 | 13 | 9  | 19 | 18 | 19 | 14 | 5  | 7  | 16 | 11 | 19 | 9  | 18 | 12 | 12 | **14.97** | 4.57 |
| H | 13 | 6  | 12 | 14 | 16 | 14 | 16 | 16 | 13 | 16 | 5  | 12 | 12 | 20 | 12 | 9  | 12 | 12 | 14 | 9  | 15 | 9  | 7  | 19 | 9  | 14 | 10 | 13 | 9  | 9  | **12.23** | 3.58 |
| I | 13 | 9  | 18 | 16 | 14 | 16 | 18 | 19 | 14 | 19 | 14 | 16 | 16 | 19 | 14 | 14 | 8  | 15 | 10 | 13 | 16 | 7  | 16 | 18 | 16 | 14 | 12 | 16 | 9  | 9  | **14.27** | 3.40 |

### Per-subject JND results, group 2 (sequences J–R, subjects 31–60)

| Seq | s31 | s32 | s33 | s34 | s35 | s36 | s37 | s38 | s39 | s40 | s41 | s42 | s43 | s44 | s45 | s46 | s47 | s48 | s49 | s50 | s51 | s52 | s53 | s54 | s55 | s56 | s57 | s58 | s59 | s60 | **Mean** | **Std** |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| J | 16 | 13 | 15 | 16 | 15 | 16 | 16 | 13 | 11 | 18 | 13 | 14 | 16 | 18 | 16 | 18 | 7  | 18 | 15 | 13 | 16 | 12 | 12 | 18 | 15 | 18 | 16 | 16 | 12 | 16 | **14.93** | 2.55 |
| K | 20 | 7  | 8  | 16 | 11 | 15 | 18 | 13 | 11 | 15 | 13 | 6  | 17 | 10 | 16 | 16 | 14 | 10 | 15 | 16 | 13 | 20 | 6  | 7  | 5  | 18 | 18 | 19 | 6  | 14 | **13.10** | 4.58 |
| L | 20 | 10 | 16 | 17 | 14 | 14 | 16 | 16 | 9  | 19 | 13 | 7  | 9  | 10 | 18 | 14 | 13 | 7  | 9  | 9  | 12 | 20 | 7  | 7  | 7  | 19 | 16 | 12 | 9  | 13 | **12.73** | 4.27 |
| M | 20 | 9  | 13 | 18 | 8  | 14 | 16 | 13 | 13 | 9  | 9  | 7  | 17 | 7  | 19 | 16 | 9  | 5  | 7  | 16 | 15 | 12 | 7  | 9  | 5  | 19 | 18 | 16 | 15 | 16 | **12.57** | 4.60 |
| N | 18 | 10 | 16 | 16 | 15 | 17 | 16 | 13 | 18 | 18 | 9  | 13 | 14 | 13 | 18 | 15 | 12 | 14 | 16 | 13 | 13 | 12 | 9  | 9  | 12 | 18 | 16 | 16 | 9  | 12 | **14.00** | 2.95 |
| O | 16 | 9  | 2  | 17 | 14 | 18 | 16 | 16 | 16 | 18 | 13 | 12 | 5  | 12 | 16 | 15 | 13 | 14 | 16 | 13 | 11 | 12 | 7  | 13 | 7  | 19 | 15 | 16 | 9  | 16 | **13.20** | 4.06 |
| P | 13 | 14 | 10 | 16 | 14 | 16 | 18 | 18 | 14 | 19 | 13 | 13 | 16 | 9  | 16 | 16 | 12 | 18 | 13 | 14 | 12 | 12 | 14 | 14 | 16 | 18 | 16 | 18 | 13 | 14 | **14.63** | 2.48 |
| Q | 16 | 8  | 2  | 17 | 16 | 13 | 16 | 18 | 17 | 15 | 13 | 9  | 15 | 9  | 18 | 16 | 13 | 17 | 18 | 12 | 15 | 16 | 7  | 16 | 5  | 16 | 15 | 16 | 10 | 16 | **13.67** | 4.13 |
| R | 13 | 5  | 15 | 16 | 16 | 17 | 18 | 13 | 18 | 19 | 13 | 14 | 15 | 9  | 18 | 16 | 10 | 18 | 16 | 14 | 16 | 16 | 7  | 12 | 7  | 16 | 16 | 16 | 7  | 15 | **14.03** | 3.77 |

### What the data tells us

**The JND clusters in the middle of the ladder.** Across every one of the 18 sequences the mean JND falls inside the **r10–r15 band** — the transition from *medium-high* to *medium* quality. Below r10 the eye is forgiving; above r15 it is unforgiving; right in between is where the threshold lives.

This has a direct codec-side implication. If a V-PCC encoder picks any rate point above r15 for a perceptually-lossless target, it is leaving bandwidth on the floor — distortion at r15 is already invisible to most observers. If it picks anything below r10, it is buying marginal bitrate savings against visible quality loss. The r10–r15 band is the sweet spot for **maximally aggressive yet perceptually-safe** V-PCC compression.

**Low-motion sequences yield tighter agreement.** Sequences **D, J, P, and N** show the smallest inter-subject standard deviation — they also happen to be the four sequences with the smallest frame-to-frame motion. With less motion, temporal masking weakens, the JND threshold depends less on each viewer's tracking strategy, and verdicts converge. A practical consequence: high-motion content needs more subjects per study to reach the same confidence as low-motion content.

---

## Use cases

OpenDPC has been built with three downstream applications in mind:

1. **Rate-distortion calibration for dynamic point cloud codecs.** Use the JND results to set perceptually-meaningful target bitrates instead of arbitrary PSNR points.
2. **Subjective ground truth for point cloud quality assessment.** Pair the JND ladder with objective quality scores to train and validate PCQA models.
3. **Demos and pedagogy.** The player on its own is the cleanest demo platform we know of for showcasing dynamic point cloud capture, compression, or rendering algorithms.

The repository is permissively licensed for both research and commercial extension.

---

## Roadmap

- **Cross-platform builds** — first-class Windows builds today; macOS and Linux build profiles on the immediate roadmap.
- **GPU-streamed long sequences** — current VRAM-resident pipeline caps sequences at the GPU's free memory; a sliding-window streamer is in development.
- **Automated JND batch mode** — head-mounted display integration and automated session orchestration to scale subjective studies.
- **Beyond V-PCC** — distortion ladders generated by G-PCC and by emerging learned codecs.
- **Public mirror on OpenI** — synchronised mirror at Peng Cheng Laboratory's OpenI platform for users behind GitHub-restricted networks.
- **Companion PCQA library link** — tighter cross-references with the sister project [OpenPCQA](https://github.com/Terriao/OpenPCQA) for objective quality assessment.

---

## FAQ

**Why Unity and not a custom OpenGL renderer?**
Unity gave us a working cross-platform shader pipeline on day one, an interaction layer (drag, zoom, UI panels) that did not need to be hand-rolled, and a build system that targets Windows, macOS, and Linux from the same source tree. The cost is a heavier runtime; the saving is months of engineering. For a research-grade tool, the trade lands in Unity's favour.

**How long does one JND annotation session take per subject?**
About 12–15 minutes for the nine sequences in one group (J subjects ran group 1, K subjects ran group 2). Each sequence converges in 4–5 paired comparisons under the ternary search, plus the mandatory 6 s dwell time per comparison.

**Can I plug in my own distortion ladder?**
Yes. The JND harness only needs an ordered set of subfolders, one per rate point, with the same frame count and indexing as the reference. Whether the distortions come from V-PCC, G-PCC, a learned codec, or hand-injected noise is opaque to the harness.

**What's the data licence on the 18 sequences?**
The source `.glb` models are individually licensed via Sketchfab and are not redistributed in this repo. The conversion scripts and the encoded V-PCC ladders are released under the same MIT licence as the codebase; consult the individual model licences before redistributing the raw asset.

---

## Citation

If OpenDPC supports your research, please cite the companion paper:

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

When you build on V-PCC results, please also cite the MPEG V-PCC standard (Graziosi et al. 2020) and the BT.500-13 protocol (ITU-R 2012).

---

## Community

OpenDPC is released under the **MIT License** and hosted on [GitHub](https://github.com/Terriao/OpenDPC).

We welcome:

- New test sequences (please bring their Sketchfab / source licence)
- Distortion-ladder generators for codecs other than V-PCC
- Translations of the in-app strings (currently English-only)
- Bug reports, especially around long sequences, large attributes, and edge cases in the ternary-search controller

Open an issue first for non-trivial contributions so we can align on interfaces. Pull requests are merged after review.

---

## License

Source code is released under the **MIT License**. Encoded V-PCC distortion ladders are released under the same license, subject to the individual Sketchfab licences of the underlying 3D models. The Unity engine itself is governed by Unity's standard licensing terms — please consult Unity Technologies for redistribution constraints on engine binaries.

---

## Acknowledgements

OpenDPC stands on the work of the **MPEG V-PCC** standardisation activity, the **ITU-R BT.500-13** subjective-evaluation methodology, and the dynamic 3D modelling community that contributes content to **Sketchfab**. The Unity engine and the broader graphics-tools ecosystem made the player implementation possible.

We thank the sixty subjects who participated in the JND study, and **Peng Cheng Laboratory** together with the **OpenI** platform for compute resources and the planned public mirror of the repository.

---

## Contributors and contact

| Role | Name | Affiliation |
|------|------|-------------|
| Coordinator | Asst. Prof. Wei Gao | School of Electronic and Computer Engineering, Peking University · Peng Cheng Laboratory |
| Lead developer | Wenxu Gao | School of Electronic and Computer Engineering, Peking University · Peng Cheng Laboratory |
| Contributor | Songlin Fan | Institute of Trustworthy Embodied AI, Fudan University · China Mobile Shanghai ICT |

For questions, collaboration, OpenI mirror access, or push privileges, please contact:

**Asst. Prof. Wei Gao** — `gaowei262@pku.edu.cn`

Bug reports and feature requests are tracked via [GitHub Issues](https://github.com/Terriao/OpenDPC/issues).

---

<div align="center">
<sub>OpenDPC · Built at the Wei Gao group, Peking University and Peng Cheng Laboratory.</sub>
</div>
