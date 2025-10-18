# MP1 Experiment Tools - Complete Package

## 📦 What You Have

I've created a complete data collection and analysis system for your MP1 project. Here's everything:

### 1. Safety Implementation
**File:** `ece598hri-fa25-mps/ws_hri/src/hri/scripts/mp1.py`
- ✅ Safety function implemented
- ✅ State-based logging (only logs on state changes)
- ✅ Detects green objects and stops robot

### 2. Data Collection Script
**File:** `ece598hri-fa25-mps/ws_hri/src/hri/scripts/data_collector.py`
- 🎯 Automated data recording
- ⌨️ Interactive keyboard controls
- 📊 CSV output with all metrics
- 🖼️ Visual feedback window

**Automatically Records:**
- Detection time
- Stop time
- Detection latency
- Stop latency
- Total response time
- Minimum distance (approximate)
- Detection success/failure

**Manual Input:**
- Entry time (press 'e' when object enters)

### 3. Analysis Script
**File:** `analyze_results.py`
- 📈 Statistical analysis (mean, std dev, min, max)
- ✅ Hypothesis evaluation
- 📋 Formatted table for report
- 🎯 Pass/fail indicators

### 4. Documentation
- **QUICK_START.md** - Fast reference for running experiments
- **DATA_COLLECTION_GUIDE.md** - Detailed usage instructions
- **MP1_Report.md** - Complete report template with sample data
- **sample_data.csv** - Example data to test analysis script

## 🚀 Quick Start

### Run Your Experiment

**Terminal 1:**
```bash
cd ws_hri && source devel/setup.bash
roslaunch ur3_driver vision_driver.launch
```

**Terminal 2:**
```bash
cd ws_hri && source devel/setup.bash
rosrun hri mp1.py
```

**Terminal 3:**
```bash
cd ws_hri && source devel/setup.bash
rosrun hri data_collector.py
```

### Collect Data

1. Press `s` to start trial
2. Introduce green object
3. Press `e` when it enters
4. Wait for robot to stop
5. Remove object
6. Repeat for 10+ trials

### Analyze Results

```bash
cd ~/Workspace/Class/hri_ece598
python3 analyze_results.py mp1_experiment_data_*.csv
```

### Test Before Real Experiment

```bash
python3 analyze_results.py sample_data.csv
```

## 🎯 What Gets Measured

| Metric | How It's Measured | Target |
|--------|------------------|---------|
| **Detection Success** | % of trials with successful detection | ≥95% (acceptable: ≥90%) |
| **Detection Latency** | Entry to detection (ms) | <150ms |
| **Stop Latency** | Detection to stop (ms) | <500ms |
| **Total Response** | Entry to stop (ms) | <500ms (acceptable: <650ms) |
| **Safe Distance** | Min distance when stopped (cm) | >5cm |

## 📊 Output Examples

### CSV Output
```csv
Trial,Entry_Time_s,Detection_Time_s,Stop_Time_s,Detection_Latency_ms,...
1,0.00,0.08,0.45,80,370,450,12.3,✓,
2,0.00,0.09,0.48,90,390,480,11.8,✓,
```

### Analysis Summary
```
DETECTION PERFORMANCE
  Total Trials:       10
  Successful:         9
  Success Rate:       90.0%

DETECTION LATENCY
  Mean:               84.4 ms
  Std Dev:            8.3 ms

TOTAL RESPONSE TIME
  Mean:               465.6 ms
  Std Dev:            26.3 ms

HYPOTHESIS EVALUATION
  Detection Success:  90.0% ~ ACCEPTABLE
  Response Time:      465.6 ms ✓ PASS
  Safe Distance:      12.0 cm ✓ EXCELLENT
```

## ⌨️ Keyboard Controls

| Key | Action |
|-----|--------|
| `s` | Start new trial |
| `e` | Mark entry time |
| `r` | Reset (discard trial) |
| `q` | Quit and save |

## 📁 File Locations

```
Class/hri_ece598/
├── ece598hri-fa25-mps/ws_hri/src/hri/scripts/
│   ├── mp1.py                    # Your safety implementation
│   └── data_collector.py         # Data collection node
│
├── MP1_Report.md                  # Complete report template
├── analyze_results.py             # Analysis script
├── sample_data.csv                # Test data
│
├── QUICK_START.md                 # Quick reference
├── DATA_COLLECTION_GUIDE.md       # Detailed guide
└── README_EXPERIMENT_TOOLS.md     # This file

Data files will be created in ws_hri/ when you run experiments:
└── mp1_experiment_data_YYYYMMDD_HHMMSS.csv
```

## 🔧 Features

### Data Collector
- ✅ Automatic detection timing
- ✅ Automatic stop detection
- ✅ Trial state machine
- ✅ Visual feedback
- ✅ CSV export
- ✅ Manual entry marking
- ✅ Trial reset capability
- ✅ Timeout handling (10s)

### Analysis Script
- ✅ Statistical summaries
- ✅ Hypothesis testing
- ✅ Pass/fail evaluation
- ✅ Formatted report tables
- ✅ No external dependencies (uses standard library only)

## 📝 Workflow Summary

1. **Setup** (one time)
   - Scripts are already executable
   - Just build workspace: `catkin_make`

2. **Run** (for each experiment session)
   - Launch 3 terminals
   - Start robot, mp1.py, data_collector.py

3. **Collect** (10+ trials)
   - Press 's', introduce object, press 'e'
   - Repeat until you have sufficient data

4. **Analyze** (after experiments)
   - Run `analyze_results.py your_data.csv`
   - Copy statistics to report
   - Use formatted table in report

5. **Report** (submission)
   - Use MP1_Report.md as template
   - Replace sample data with your actual results
   - Include analysis output

## ⚠️ Important Notes

### Distance Measurement
The distance measurement is **approximate** based on pixel distances. It's useful for relative comparisons but not absolute measurements. For more accuracy:
- Use physical measurements with ruler/tape
- Implement forward kinematics (advanced)
- Use calibrated depth camera

### Entry Time
- **Option A (Recommended):** Press 'e' when object enters frame
- **Option B (Automatic):** Entry marked on first detection
  - Less accurate but still usable
  - Will underestimate latency slightly

### Trial Ending
Trials end automatically when:
- Robot stops AND object is removed
- OR 10 seconds pass without detection

Manual control:
- Press 'r' to discard bad trial
- Press 'q' to quit (asks about active trial)

## 🎓 Tips for Success

1. **Practice first** - Run a few practice trials to get comfortable with the controls

2. **Consistent method** - Use the same procedure for all trials (entry position, velocity, etc.)

3. **Good lighting** - Ensure consistent lighting for reliable green detection

4. **Clear workspace** - Remove other green objects that could cause false detections

5. **Enough trials** - Run at least 10 trials for meaningful statistics

6. **Note issues** - If something goes wrong, you can add notes in the CSV after

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Data collector won't start | Check mp1.py is running first |
| No detection | Verify green object is visible and in focus |
| Trial won't end | Remove object completely from view |
| Robot doesn't stop | Ensure mp1.py safety function is active |
| CSV not saved | Check write permissions in directory |

## 📧 What to Submit

Your final submission should include:
1. **Report** (based on MP1_Report.md with your data)
2. **CSV data file** (your experimental results)
3. **Code** (mp1.py with your safety implementation)

The analysis script output can be directly copied into your report!

---

## ✨ Everything is Ready!

You now have:
- ✅ Working safety implementation
- ✅ Automated data collection
- ✅ Statistical analysis
- ✅ Report template with sample results
- ✅ Complete documentation

Just run your experiments and collect data. Good luck! 🚀

