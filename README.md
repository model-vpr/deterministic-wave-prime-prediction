# deterministic-wave-prime-prediction
A deterministic approach to prime distribution using wave interference analysis. This repository contains the Predictive Sonar algorithm for proactive prime detection and spectral analysis of the 6n ± 1 progression.

# Deterministic Wave Prime Prediction

[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.XXXXXXX-blue.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

## Overview
This repository contains the official implementation of the **Interference Wave Model (IWM)** and the **Predictive Sonar Algorithm**. The project demonstrates a deterministic approach to prime number distribution by treating the number line as a wave interference field.

Instead of traditional trial division or probabilistic methods, this model identifies primes as **Zero-Density Nodes** ($\Phi(x) = 0$) within the 6n ± 1 harmonic progression (The Crown).

### 📄 Full Research Paper
The theoretical foundations, spectral analysis, and empirical verifications are available in the preprint:
**"The Geometry of Silence: A Deterministic Wave Interference Model for Prime Distribution"**
[Link to Document on Zenodo/ResearchGate]

---

## 📂 Repository Structure & File Descriptions

### 1. Core Algorithms
* **`evolutionary_simulation.py`**: The primary engine that simulates wave propagation. It shows how every integer emits waves and how the interference field evolves sequentially from source 5 to N.
* **`targeted_pulse_predictor.py`**: An optimized version of the algorithm designed for high-speed prediction. It focuses on specific coordinates to verify prime/composite status without full field simulation.

### 2. Analysis & Diagnostics
* **`twins_sonar.py`**: Specifically designed to scan for Twin Primes (Zero-Impact adjacency) and identify **Peak Interference Density** points (Maximum Resonance) in the number line.

### 3. Visualization Tools
* **`waves_plot.py`**: Generates visual representations of the interference patterns, illustrating how waves cancel out at prime coordinates.
* **`crown_1.py`** & **`crown_2.py`**: Scripts for 3D and 2D visualization of the 6n ± 1 progression, mapping the harmonic structure of the "Crown" logic.

---


