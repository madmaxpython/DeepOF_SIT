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





## 📦 Installation

```bash
git clone https://github.com/madmaxpython/DeepOF_SIT/
cd DeepOF_SIT
pip install -r requirements.txt
```

## 🚀 Quickstart


=

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

