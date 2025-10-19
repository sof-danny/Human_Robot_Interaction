# Safety Region Setup Guide

## Changes Made to `mp1.py`

### 1. Added Safety Region Definition
```python
# Line 35 in mp1.py
self.safety_region = (100, 100, 540, 380)  # (x_min, y_min, x_max, y_max)
```

### 2. Added Visualization
The camera view now shows:
- **Red rectangle**: Safety region boundary
- **Red circles**: Objects INSIDE safety region (robot stops)
- **Green circles**: Objects OUTSIDE safety region (robot continues)
- **Text labels**: "IN SAFETY ZONE" or "OUTSIDE" for each object

### 3. Updated Safety Logic
Now correctly handles:
- ✅ **Single object**: Stops if in safety region
- ✅ **Multiple objects**: Stops if ANY object is in safety region
- ✅ **Multiple objects outside**: Continues if ALL objects are outside
- ✅ **Status logging**: Shows "X/Y objects in safety region"

---

## How to Adjust the Safety Region

### Step 1: Run the System
```bash
cd ws_hri && source devel/setup.bash
roslaunch ur3_driver vision_driver.launch

# In another terminal:
rosrun hri mp1.py
```

### Step 2: View the Camera Window
Look at the "Vision Safety" window - you'll see:
- The camera view with detected green objects
- A **RED RECTANGLE** showing the current safety region

### Step 3: Adjust Safety Region Coordinates

Edit line 35 in `mp1.py`:

```python
self.safety_region = (x_min, y_min, x_max, y_max)
```

**Coordinate System:**
- `(0, 0)` = Top-left corner of camera image
- `x` increases to the right
- `y` increases downward
- Typical camera resolution: 640x480

**Example Adjustments:**

```python
# Default (covers center ~70% of frame)
self.safety_region = (100, 100, 540, 380)

# Larger region (covers ~90% of frame)
self.safety_region = (50, 50, 590, 430)

# Smaller region (covers center ~50%)
self.safety_region = (150, 150, 490, 330)

# Full frame (entire camera view)
self.safety_region = (0, 0, 640, 480)

# Upper half only
self.safety_region = (0, 0, 640, 240)

# Lower half only  
self.safety_region = (0, 240, 640, 480)

# Left side
self.safety_region = (0, 0, 320, 480)

# Right side
self.safety_region = (320, 0, 640, 480)
```

### Step 4: Verify Coverage

**Important**: The safety region should cover the **entire possible span of robot motion** as viewed from the camera.

To verify:
1. Run the robot through its full motion range (goal 1 ↔ goal 2)
2. Watch the camera view
3. Make sure the red rectangle encompasses all areas where the robot can move
4. If robot motion extends outside the red rectangle, **expand the safety region**

---

## Demo Checklist (Per Instructor Requirements)

### Part 1: Verify Safety Region Coverage
- [ ] Start system, view camera window
- [ ] Red rectangle is clearly visible
- [ ] Move robot through full range of motion
- [ ] Verify safety region covers entire robot motion span
- [ ] If not, adjust coordinates and restart

### Part 2: Single Object Test
- [ ] Robot is moving between goals
- [ ] Move one green block INTO safety region
- [ ] ✅ Robot should STOP (red circle, "IN SAFETY ZONE" label)
- [ ] Move block OUTSIDE safety region  
- [ ] ✅ Robot should RESUME (green circle, "OUTSIDE" label)

### Part 3: Multiple Objects Test

**Test Case 1: Both outside**
- [ ] Place 2 green blocks OUTSIDE safety region
- [ ] ✅ Both show green circles
- [ ] ✅ Robot continues moving

**Test Case 2: One inside, one outside**
- [ ] Move ONE block into safety region
- [ ] ✅ One shows red circle, one shows green circle
- [ ] ✅ Robot STOPS (log: "1/2 object(s) in safety region")

**Test Case 3: Both inside**
- [ ] Move BOTH blocks into safety region
- [ ] ✅ Both show red circles  
- [ ] ✅ Robot remains STOPPED (log: "2/2 object(s) in safety region")

**Test Case 4: Return to both outside**
- [ ] Move both blocks outside safety region
- [ ] ✅ Both show green circles
- [ ] ✅ Robot RESUMES (log: "2 object(s) detected outside region")

---

## Recording the Demo Video

### Setup
1. Position your phone camera to capture the computer screen
2. Make sure the "Vision Safety" window is clearly visible
3. The red safety rectangle should be obvious in the video

### Recording Script

**1. Show Safety Region (10 seconds)**
```
"Here you can see the camera view with the red safety region 
covering the robot's motion range."
```

**2. Single Object Demo (20 seconds)**
```
"Moving a green block into the safety region... [robot stops]
Now removing it... [robot resumes]"
```

**3. Two Objects - Both Outside (10 seconds)**
```
"With two blocks outside the safety region, the robot continues."
```

**4. Two Objects - One Inside (10 seconds)**
```
"When one block enters the safety region... [robot stops]
Even though the other block is outside."
```

**5. Two Objects - Both Inside (10 seconds)**
```
"With both blocks in the safety region, robot remains stopped."
```

**6. Return to Normal (10 seconds)**
```
"Removing both blocks from the safety region... [robot resumes]"
```

**Total Video Length**: ~60 seconds

---

## Console Output Examples

You'll see these logs as you test:

```
[INFO] Vision safety initialized.

# When object enters safety region:
[WARN] SAFETY VIOLATION: 1/1 object(s) in safety region! Stopping robot.

# When object exits safety region:
[INFO] Safety region clear. 0 object(s) detected outside region. Robot can resume.

# With 2 objects, 1 in region:
[WARN] SAFETY VIOLATION: 1/2 object(s) in safety region! Stopping robot.

# With 2 objects, both outside:
[INFO] Safety region clear. 2 object(s) detected outside region. Robot can resume.
```

---

## Troubleshooting

### Problem: Safety region too small
**Symptom**: Robot moves outside visible red rectangle
**Solution**: Increase safety_region coordinates to cover more area

### Problem: Can't see red rectangle
**Symptom**: No red outline visible in camera view
**Solution**: 
- Check if robot is blocking camera view
- Verify coordinates are within camera resolution (typically 640x480)
- Try larger, more centered coordinates

### Problem: Multiple objects not detected
**Symptom**: Only one blob shown even with 2 blocks
**Solution**: 
- Check color thresholds in `blob_search.py`
- Ensure both blocks are clearly green and visible
- Check lighting - may need to adjust HSV thresholds

### Problem: False detections
**Symptom**: Random green objects triggering stops
**Solution**:
- Remove green items from camera view
- Adjust blob size filtering in `blob_search.py` (lines 11-12)
- Current: 500-700 pixels, increase minArea to filter smaller objects

### Problem: Objects not tracked consistently
**Symptom**: Blobs appearing/disappearing rapidly
**Solution**:
- Improve lighting conditions
- Use solid, uniformly green blocks
- Adjust exposure on camera if available

---

## Key Features of Updated System

✅ **Visible Safety Region**: Red rectangle always shown  
✅ **Multi-Object Support**: Handles 1, 2, or more green blocks  
✅ **Clear Status Indicators**: Red (danger) vs Green (safe) circles  
✅ **Informative Logging**: Shows count of objects in/out of region  
✅ **Conservative Safety**: Stops if ANY object is in region  
✅ **Easy to Adjust**: Simple coordinate tuning  

---

## For Your Report/Presentation

Include screenshots showing:
1. **Setup view**: Camera with red safety region visible
2. **Single object inside**: Red circle, robot stopped
3. **Two objects - one inside**: One red, one green circle
4. **Two objects outside**: Both green circles, robot moving

These visuals clearly demonstrate:
- Defined safety space (not just entire frame)
- Multi-object handling capability
- Clear visual feedback system
- Proper safety logic implementation

Good luck with your demo! 🎥🤖

