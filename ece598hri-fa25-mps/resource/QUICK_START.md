# MP1 Quick Start Guide

## 🚀 Running Your Experiment

### Step 1: Setup (One Time)
```bash
cd ~/Workspace/Class/hri_ece598/ece598hri-fa25-mps/ws_hri
chmod +x src/hri/scripts/data_collector.py
catkin_make
```

### Step 2: Launch System (3 Terminals)

**Terminal 1 - Robot Driver:**
```bash
cd ws_hri && source devel/setup.bash
roslaunch ur3_driver vision_driver.launch
```
Wait for: `Got connection` messages

**Terminal 2 - MP1 Node:**
```bash
cd ws_hri && source devel/setup.bash
rosrun hri mp1.py
```
Robot starts moving

**Terminal 3 - Data Collector:**
```bash
cd ws_hri && source devel/setup.bash
rosrun hri data_collector.py
```

### Step 3: Run Trials

1. Press **'s'** to start trial
2. Introduce green object
3. Press **'e'** when object enters (or it auto-marks)
4. Wait for robot to stop
5. Remove object
6. Trial auto-saves
7. Repeat!

**Keyboard Commands:**
- `s` = Start new trial
- `e` = Mark entry time
- `r` = Reset/discard trial
- `q` = Quit and save

### Step 4: Analyze Results

```bash
cd ~/Workspace/Class/hri_ece598
python3 analyze_results.py mp1_experiment_data_*.csv
```

## 📊 What You Get

**CSV File:**
- All trial data
- Timestamps, latencies, distances
- Success/failure indicators

**Analysis Output:**
- Mean ± StdDev for all metrics
- Success rate
- Pass/Fail vs. hypothesis targets
- Formatted table for your report

## 🎯 Experiment Tips

1. **Start trial when robot is already moving**
2. **Press 'e' precisely when object enters camera view**
3. **Remove object clearly after robot stops**
4. **Keep lighting consistent**
5. **Run 10+ trials for good statistics**

## 📝 Files Created

```
ws_hri/
└── mp1_experiment_data_YYYYMMDD_HHMMSS.csv  ← Your data

MP1_Report.md          ← Report template
DATA_COLLECTION_GUIDE.md  ← Detailed guide
analyze_results.py     ← Analysis script
```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Trial won't end | Remove object from view, or press 'r' |
| No detection | Check green object visibility & lighting |
| Robot doesn't stop | Ensure mp1.py is running |
| CSV not created | Check write permissions |

## 📈 Example Session

```
$ rosrun hri data_collector.py
Press 's' to start trial

[Press 's']
TRIAL 1 STARTED
Press 'e' when object ENTERS

[Introduce object, press 'e']
[DATA] Entry time marked
[DATA] Detection at t=0.087s
[DATA] Robot stopped at t=0.453s

[Remove object]
TRIAL 1 COMPLETE
  Detection Success: YES
  Detection Latency: 87 ms
  Total Response: 453 ms

[Press 's' for next trial...]
```

That's it! Happy experimenting! 🤖

