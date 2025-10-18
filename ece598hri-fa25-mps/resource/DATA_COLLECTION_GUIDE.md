# MP1 Data Collection Guide

## Overview
The `data_collector.py` script automates most of the experimental data collection for MP1. It runs alongside your `mp1.py` node and records timing data, detection success, and other metrics to a CSV file.

## Setup

1. **Make the script executable:**
```bash
cd ~/Workspace/Class/hri_ece598/ece598hri-fa25-mps/ws_hri
chmod +x src/hri/scripts/data_collector.py
```

2. **Ensure your workspace is built:**
```bash
cd ~/Workspace/Class/hri_ece598/ece598hri-fa25-mps/ws_hri
catkin_make
source devel/setup.bash
```

## Running an Experiment

### Terminal 1: Start Robot Driver
```bash
cd ws_hri && source devel/setup.bash
roslaunch ur3_driver vision_driver.launch
```

### Terminal 2: Start MP1 Node
```bash
cd ws_hri && source devel/setup.bash
rosrun hri mp1.py
```

### Terminal 3: Start Data Collector
```bash
cd ws_hri && source devel/setup.bash
rosrun hri data_collector.py
```

## How to Use

### Interactive Controls

The data collector has a simple keyboard interface:

- **'s'** - **START** a new trial
- **'e'** - **MARK ENTRY** time (when object enters workspace)
- **'r'** - **RESET** current trial (discard without saving)
- **'q'** - **QUIT** and save all data

### Running a Trial

1. **Press 's'** to start a new trial
   - The window will show "Trial X - ACTIVE"
   - Trial counter increments

2. **Introduce the green object into the workspace**
   - **Option A (Recommended):** Press **'e'** the moment the object enters the frame
   - **Option B (Automatic):** Entry time will be auto-marked on first detection
   
3. **The script automatically records:**
   - Detection time (when green object is first detected)
   - Stop time (when robot velocity drops below threshold)
   - Minimum distance (approximate, based on pixel distance)

4. **Trial ends automatically when:**
   - Robot stops AND object is removed from workspace
   - OR 10 seconds pass without detection (timeout)

5. **Data is automatically saved to CSV**

### Manual Trial Control

If you need to end a trial early:
- Press **'r'** to reset and discard the trial
- Press **'q'** to quit (you'll be prompted to save active trial)

## What Gets Recorded

The CSV file contains:
- **Trial number**
- **Entry time** (0.00 as reference)
- **Detection time** (seconds after entry)
- **Stop time** (seconds after entry)
- **Detection latency** (milliseconds)
- **Stop latency** (milliseconds from detection to stop)
- **Total response time** (milliseconds from entry to stop)
- **Minimum distance** (approximate, in cm)
- **Detection success** (✓ or ✗)
- **Notes** (for timeouts or issues)

## Output

Data is saved to: `mp1_experiment_data_YYYYMMDD_HHMMSS.csv`

Example output:
```csv
Trial,Entry_Time_s,Detection_Time_s,Stop_Time_s,Detection_Latency_ms,Stop_Latency_ms,Total_Response_ms,Min_Distance_cm,Detection_Success,Notes
1,0.00,0.08,0.45,80,370,450,12.3,✓,
2,0.00,0.09,0.48,90,390,480,11.8,✓,
3,0.00,,,,,,,✗,Timeout - no detection
```

## Tips for Best Results

1. **Consistent entry timing**: Try to press 'e' as precisely as possible when the object enters the camera frame

2. **Wait for robot motion**: Start trial only when robot is already moving between goals

3. **Clear removal**: After robot stops, clearly remove the object so the trial can auto-end

4. **Object visibility**: Ensure green object is clearly visible and not occluded

5. **Lighting**: Keep lighting consistent across all trials

6. **Notes**: If something goes wrong, you can add notes in the CSV file afterward

## Troubleshooting

### Trial won't end automatically
- Make sure the object is removed from view after robot stops
- Check that robot actually stopped (look at joint values)
- Press 'r' to reset and try again

### Detection not working
- Verify green object is in camera view
- Check color thresholds in `blob_search.py`
- Ensure lighting is adequate

### CSV file not created
- Check file permissions in the directory
- Verify script has write access
- Check console for error messages

### Robot doesn't stop
- Make sure `mp1.py` is running (not just data_collector.py)
- The data collector only records; mp1.py controls the robot

## Example Experimental Session

```bash
# Terminal 3 (after starting driver and mp1.py)
$ rosrun hri data_collector.py

[INFO] MP1 Data Collector Initialized
[INFO] Data will be saved to: mp1_experiment_data_20251018_143052.csv
[INFO] Press 's' to START a new trial

# Press 's'
[INFO] TRIAL 1 STARTED
[INFO] Press 'e' when object ENTERS the workspace

# Introduce object, press 'e'
[INFO] [DATA] Entry time marked: 1729271452.384

# Object detected
[INFO] [DATA] Detection at t=0.087s

# Robot stops
[INFO] [DATA] Robot stopped at t=0.453s

# Remove object
[INFO] Trial conditions met. Ending trial...
[INFO] TRIAL 1 COMPLETE
[INFO]   Detection Success: YES
[INFO]   Detection Latency: 87 ms
[INFO]   Total Response: 453 ms
[INFO]   Min Distance: 12.1 cm (approximate)

# Press 's' for next trial...
```

## Post-Processing

After collecting all data, you can:

1. **Open CSV in Excel/Google Sheets** for analysis
2. **Calculate statistics:**
   - Mean and standard deviation
   - Success rate
   - Min/max values
3. **Create visualizations:**
   - Response time distribution
   - Detection success rate
   - Distance vs. response time correlation

## Notes on Distance Calculation

⚠️ **Important**: The distance calculation in this script is approximate and based on pixel distances. For accurate 3D distances, you would need:
- Forward kinematics for robot end-effector position
- Camera calibration for 3D reconstruction
- Proper coordinate transformations

The current implementation provides a relative metric for comparison across trials but should not be considered absolute measurements.

For more accurate distance measurements, consider:
1. Using markers at known positions
2. Manual measurement with measuring tape
3. Implementing forward kinematics (more advanced)

