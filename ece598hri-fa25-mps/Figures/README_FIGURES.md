# MP1 Report Figures Reference

## Generated Plots (7 total)

All plots generated from experimental data in `mp1_experiment_data_20251018_164122.csv`

### 1. **performance_summary.png**
- **Type**: Dashboard (multi-panel)
- **Shows**: 
  - Detection success rate pie chart
  - Response time statistics (mean, median, min, max)
  - Safe distance statistics
  - Response time per trial bar chart
- **Use**: Overview/summary figure showing all key metrics at a glance

### 2. **success_rate.png**
- **Type**: Pie chart
- **Shows**: Detection success rate (100% = 15/15 trials)
- **Use**: Demonstrates perfect detection performance

### 3. **response_times_trials.png**
- **Type**: Line plot
- **Shows**: Detection latency, stop latency, and total response time across all 15 trials
- **Use**: Shows timing performance over trials, reveals bimodal distribution

### 4. **bimodal_analysis.png**
- **Type**: Scatter plot
- **Shows**: Fast trials (green, <1s) vs slow trials (red, ≥1s) 
- **Use**: Clearly visualizes the two distinct groups due to entry marking methodology

### 5. **response_time_distribution.png**
- **Type**: Histogram + Box plot (side by side)
- **Shows**: Distribution of total response times with mean and median lines
- **Use**: Statistical distribution analysis, shows outliers and skewness

### 6. **latency_comparison.png**
- **Type**: Box plot
- **Shows**: Detection latency vs stop latency side-by-side comparison
- **Use**: Compares the two components of total response time, shows system response characteristics

### 7. **distance_measurements.png**
- **Type**: Bar chart
- **Shows**: Minimum safe distance for each trial with 5cm requirement line and mean line
- **Use**: Demonstrates safety margin compliance across all trials

## Original Photos (3 total)

### 8. **Experimental_setup.JPG**
- **Type**: Photograph
- **Shows**: UR3 robot with overhead camera setup
- **Use**: Shows physical experimental setup

### 9. **data_collection.png**
- **Type**: Screenshot
- **Shows**: Data collection interface with real-time detection visualization
- **Use**: Shows the automated data collection system in action

### 10. **data_collection_2.png**
- **Type**: Screenshot
- **Shows**: Additional view of data collection interface
- **Use**: Alternative view of the system (optional, not currently used in report)

---

## Figure Usage in Report

### Markdown Report (MP1_Report.md)
- Figure 1: Experimental_setup.JPG
- Figure 2: data_collection.png
- Figure 3: performance_summary.png
- Figure 4: success_rate.png
- Figure 5: response_times_trials.png
- Figure 6: bimodal_analysis.png
- Figure 7: response_time_distribution.png
- Figure 8: latency_comparison.png
- Figure 9: distance_measurements.png

### LaTeX Report (MP1_Report.tex)
All figures included with proper LaTeX formatting:
- Uses `\includegraphics` for image inclusion
- Proper figure environments with captions and labels
- Some figures arranged side-by-side using minipage
- All figures cross-referenced in text

---

## Key Insights from Figures

### What the Data Shows

1. **Perfect Detection** (Fig 4, 3)
   - 100% success rate, no missed detections
   - System is highly reliable for detection

2. **Bimodal Timing** (Fig 6, 7)
   - Clear separation: fast (<1s) vs slow (>1s) trials
   - Due to experimental methodology, not system failure
   - Fast group represents actual system capability

3. **Stop Latency is Key** (Fig 8)
   - Once detected, robot stops consistently (~346ms mean)
   - Detection latency has high variance due to entry marking
   - Stop latency better represents intrinsic system performance

4. **Excellent Safety Margins** (Fig 9)
   - All trials exceed 5cm minimum requirement
   - Mean distance: 23.5cm (far exceeds minimum)
   - System maintains safe separation

5. **Trial-to-Trial Consistency** (Fig 5)
   - Detection and stop latency relatively stable
   - Total response variance driven by detection timing
   - System behavior is predictable once detection occurs

---

## Regenerating Plots

If you need to regenerate the plots with different data or styling:

```bash
cd /Users/samuel/Workspace/Class/hri_ece598/ece598hri-fa25-mps
python3 generate_plots.py
```

The script will:
1. Load data from `results/mp1_experiment_data_20251018_164122.csv`
2. Generate all 7 plots
3. Save them to `Figures/` directory
4. Overwrite existing plot files

---

## For Overleaf

When uploading to Overleaf:

1. **Create folder structure**:
   ```
   project/
   ├── MP1_Report.tex
   └── Figures/
       ├── Experimental_setup.JPG
       ├── data_collection.png
       ├── performance_summary.png
       ├── success_rate.png
       ├── response_times_trials.png
       ├── bimodal_analysis.png
       ├── response_time_distribution.png
       ├── latency_comparison.png
       └── distance_measurements.png
   ```

2. **Upload files**:
   - Upload `MP1_Report.tex` to project root
   - Create `Figures` folder
   - Upload all image files to `Figures/` folder

3. **Compile**:
   - Click "Recompile"
   - All figures should appear correctly

**Note**: The LaTeX file uses relative paths `../Figures/`, so adjust if your Overleaf structure is different. You may need to change `../Figures/` to just `Figures/` in the .tex file if you place them in the same level.

---

## Tips for Presentation

- **Performance Summary** (Fig 3): Great for first slide/overview
- **Bimodal Analysis** (Fig 6): Key for explaining timing results
- **Success Rate** (Fig 4): Simple, impactful - shows main achievement
- **Distance Measurements** (Fig 9): Demonstrates safety compliance

Use figures to tell the story:
1. Setup (Fig 1) 
2. Perfect detection (Fig 4)
3. Timing has variance (Fig 6, 7)
4. But system works well (Fig 8)
5. Safe distances maintained (Fig 9)

