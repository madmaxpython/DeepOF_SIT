# Social Interaction Test (SIT) Analyzer

**DeepOF_SIT** is a Python package and utility toolkit designed to extract and quantify behavioral metrics from the Social Interaction Test (SIT) using DeepOF output data. It enables reproducible zone-based analyses, including time spent in social zones, distance to social targets, and derived Social Interaction Ratios (SIR).

---

## 🔧 Features

- Define arena and Social Interaction Zone (SIZ) for each animal/video
- Automatically calculate:
  - Time spent in SIZ
  - Distance to a Point of Interest (POI)
  - Social Interaction Ratios (SIR)
- Clean output in `pandas` DataFrame (easy to save to CSV or analyze further)
- Includes scripts for:
  - Zone definition via video frames
  - Measure pixel size
  - 3D visualization
  - Reproducing article figures via Jupyter Notebooks

---

## 📁 Project Structure

| Path                        | Description                                      |
|----------------------------|--------------------------------------------------|
| `sit_analysis/analyzer.py` | Core analysis classes: `SITAnalyzer`, `Experience` |
| `sit_analysis/data_loader.py` | Utility functions for loading configs        |
| `scripts/define_zones.py`  | Tool to draw/define zones on video frames        |
| `scripts/generate_3d_plot.py` | Generate 3D trajectory plots                |
| `notebooks/`               | Jupyter notebooks to reproduce article figures   |
| `main.py`                  | Main script to run the analysis                  |
| `requirements.txt`         | Clean list of dependencies                       |
| `tests/`                   | Optional unit tests                              |



## 📦 Installation

```bash
git clone https://github.com/yourusername/sit-analyzer.git
cd sit-analyzer
pip install -r requirements.txt
```

## 🚀 Quickstart
1. Define Zones for Each Video
Use the provided script to annotate arenas and SIZ regions manually:
```bash
python scripts/define_zones.py
```
This will save TXT files that map arena/SIZ coordinates to each video.

2. Run Batch Analysis
In main.py, set the paths to your project and zone files, then run:
```bash
python main.py
```

Output: a .csv file or DataFrame with per-animal metrics across both sessions.

## 📊 Metrics Included

| Metric                               | Description                                      |
|--------------------------------------|--------------------------------------------------|
| `Time_in_SIZ_Session1/2`             | Time spent in the Social Interaction Zone        |
| `Normalized_distance_to_POI_Session` | Mean distance to POI, scaled to arena size       |
| `Distance_SIR_typeA/B`               | Ratio of Session 2 vs Session 1 distances        |
| `Time_SIR_typeA/B`                   | Ratio of Session 2 vs Session 1 SIZ durations    |

## 🧪 Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `deepof` 
- `opencv-python` 
- `jupyter` *(for notebooks)*

See [`requirements.txt`](./requirements.txt) for exact versions.

---

## 📘 License

**MIT License**  
Feel free to reuse or extend the tool for your own behavioral analyses.

---



## 🤝 Acknowledgements

This tool was developed as a supplementary resource for analyzing mouse social behavior using DeepOF tracking data.  
Thanks to the **Flores Lab** for feedback and support.

