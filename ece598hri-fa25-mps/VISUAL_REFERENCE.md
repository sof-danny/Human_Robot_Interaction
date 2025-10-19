# Visual Reference - What You'll See

## Camera Window: "Vision Safety"

```
┌─────────────────────────────────────────────────────────┐
│                  Vision Safety Window                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│         "SAFETY REGION" (red text)                       │
│         ┌────────────────────────────────┐              │
│         │                                │              │
│         │    RED RECTANGLE (thick)       │              │
│         │    Safety Region Boundary      │              │
│    ●    │                                │              │
│  GREEN  │         ⚫ RED                 │              │
│ CIRCLE  │        (object inside)         │              │
│ (outside)│     "IN SAFETY ZONE"           │              │
│         │                                │              │
│         │                                │              │
│         └────────────────────────────────┘              │
│                                                          │
│   Robot base/workspace visible in center                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Color Legend

| Visual Element | Color | Meaning |
|----------------|-------|---------|
| **Rectangle Border** | 🔴 **RED** (thick, 3px) | Safety region boundary |
| **"SAFETY REGION" text** | 🔴 **RED** | Label for safety zone |
| **Circle around object** | 🔴 **RED** (thick, 3px) | Object IN safety region → DANGER |
| **Circle around object** | 🟢 **GREEN** (thick, 3px) | Object OUTSIDE region → SAFE |
| **"IN SAFETY ZONE"** | 🔴 **RED** | Warning label on dangerous object |
| **"OUTSIDE"** | 🟢 **GREEN** | Safe label on objects outside region |
| **Blue dots** | 🔵 **BLUE** (small) | Blob detection keypoints (background) |

---

## Example Scenarios

### Scenario 1: No Objects
```
┌───────────────────────────────────────┐
│  "SAFETY REGION"                      │
│  ┌──────────────────────────────┐     │
│  │                              │     │
│  │    (Empty safety region)     │     │
│  │                              │     │
│  │      RED RECTANGLE           │     │
│  │                              │     │
│  └──────────────────────────────┘     │
│                                       │
│  Status: Robot MOVING                 │
│  Console: "No objects detected"       │
└───────────────────────────────────────┘
```

### Scenario 2: One Object Inside
```
┌───────────────────────────────────────┐
│  "SAFETY REGION"                      │
│  ┌──────────────────────────────┐     │
│  │                              │     │
│  │       ⚫ RED CIRCLE          │     │
│  │    "IN SAFETY ZONE"          │     │
│  │                              │     │
│  │      RED RECTANGLE           │     │
│  └──────────────────────────────┘     │
│                                       │
│  Status: Robot STOPPED ⛔            │
│  Console: "1/1 object(s) in region"   │
└───────────────────────────────────────┘
```

### Scenario 3: One Object Outside
```
┌───────────────────────────────────────┐
│  "SAFETY REGION"                      │
│  ┌──────────────────────────────┐     │
│  │                              │     │
│  │    (Empty safety region)     │     │
│  │                              │     │
│  │      RED RECTANGLE           │     │
│  └──────────────────────────────┘     │
│    ● GREEN CIRCLE                     │
│   "OUTSIDE"                           │
│  Status: Robot MOVING ✓               │
│  Console: "1 object(s) outside"       │
└───────────────────────────────────────┘
```

### Scenario 4: Two Objects - One In, One Out
```
┌───────────────────────────────────────┐
│  "SAFETY REGION"                      │
│  ┌──────────────────────────────┐     │
│  │                              │     │
│  │       ⚫ RED CIRCLE          │     │
│  │    "IN SAFETY ZONE"          │     │
│  │                              │     │
│  │      RED RECTANGLE           │     │
│  └──────────────────────────────┘     │
│    ● GREEN CIRCLE                     │
│   "OUTSIDE"                           │
│  Status: Robot STOPPED ⛔            │
│  Console: "1/2 object(s) in region"   │
└───────────────────────────────────────┘
```

### Scenario 5: Two Objects - Both Inside
```
┌───────────────────────────────────────┐
│  "SAFETY REGION"                      │
│  ┌──────────────────────────────┐     │
│  │   ⚫ RED        ⚫ RED       │     │
│  │  "IN ZONE"   "IN ZONE"       │     │
│  │                              │     │
│  │      RED RECTANGLE           │     │
│  │                              │     │
│  └──────────────────────────────┘     │
│                                       │
│  Status: Robot STOPPED ⛔            │
│  Console: "2/2 object(s) in region"   │
└───────────────────────────────────────┘
```

### Scenario 6: Two Objects - Both Outside
```
┌───────────────────────────────────────┐
│  "SAFETY REGION"                      │
│  ┌──────────────────────────────┐     │
│  │                              │     │
│  │    (Empty safety region)     │     │
│  │                              │     │
│  │      RED RECTANGLE           │     │
│  └──────────────────────────────┘     │
│  ● GREEN      ● GREEN                 │
│ "OUTSIDE"    "OUTSIDE"                │
│  Status: Robot MOVING ✓               │
│  Console: "2 object(s) outside"       │
└───────────────────────────────────────┘
```

---

## Real-World Camera View

Your actual camera view will show:
- The UR3 robot (typically center/bottom of frame)
- Workspace surface (table/desk)
- Green blocks when placed
- The red safety rectangle overlay
- Colored circles and text on detected blocks

**Important**: 
- The red rectangle should **cover all areas where the robot can move**
- If you see robot parts moving outside the red rectangle, **expand the safety region**

---

## Coordinate System Reference

```
(0,0) ────────────── X increases ──────────────→
  │
  │     Camera Image (typical: 640 x 480)
  │
  Y     ┌─────────────────────────────────┐
  │     │   Top-Left                      │
  │     │                                 │
increases │   Your Safety Region:           │
  │     │   (x_min, y_min) ──┐            │
  ↓     │                    │            │
        │                    ↓            │
        │              (x_max, y_max)     │
        │                                 │
        │                   Bottom-Right  │
        └─────────────────────────────────┘
```

**Default Safety Region:**
```python
self.safety_region = (100, 100, 540, 380)
                      └─x_min
                           └─y_min
                                └─x_max
                                     └─y_max
```

This creates a rectangle:
- Top-left corner at pixel (100, 100)
- Bottom-right corner at pixel (540, 380)
- Width: 440 pixels
- Height: 280 pixels

---

## Adjusting for Your Setup

### If robot motion exceeds red rectangle:

**Expand horizontally (wider):**
```python
# From: (100, 100, 540, 380)
# To:   (50,  100, 590, 380)  ← Increased width
```

**Expand vertically (taller):**
```python
# From: (100, 100, 540, 380)
# To:   (100, 50,  540, 430)  ← Increased height
```

**Expand both:**
```python
# From: (100, 100, 540, 380)
# To:   (50,  50,  590, 430)  ← Increased both
```

**Make smaller (tighter safety bounds):**
```python
# From: (100, 100, 540, 380)
# To:   (150, 150, 490, 330)  ← Decreased both
```

---

## Testing Visually

### Good Setup ✅
- Red rectangle is clearly visible
- Rectangle covers all robot motion
- Detected objects show colored circles
- Text labels are readable
- Robot stops when red circle appears inside rectangle

### Needs Adjustment ❌
- Can't see red rectangle → Check coordinates are within 0-640, 0-480
- Robot moves outside rectangle → Expand safety region
- Objects not detected → Check `blob_search.py` thresholds
- No colored circles → Check if blob_search is finding objects

---

## Demo Video Frames

Your video should clearly show these transitions:

1. **Start**: Red rectangle visible, robot moving, no objects
2. **Block enters**: Red circle appears, robot stops
3. **Block exits**: Red circle becomes green, robot resumes
4. **Two blocks outside**: Both green circles, robot moving
5. **One enters**: One red, one green, robot stops
6. **Second enters**: Both red, robot stopped
7. **Both exit**: Both green, robot resumes

---

## Console Log Reference

Match these logs with visual changes:

```bash
# Initial state
[INFO] Vision safety initialized.

# Object enters safety region (visual: green→red circle)
[WARN] SAFETY VIOLATION: 1/1 object(s) in safety region! Stopping robot.

# Object exits (visual: red→no circle)
[INFO] No objects detected. Robot can resume.

# Two objects, one enters (visual: one red, one green)
[WARN] SAFETY VIOLATION: 1/2 object(s) in safety region! Stopping robot.

# Two objects, both exit (visual: both green)
[INFO] Safety region clear. 2 object(s) detected outside region. Robot can resume.
```

---

## Quick Verification Checklist

Before recording your demo:

Visual Elements Present:
- [ ] Red rectangle visible and sized correctly
- [ ] "SAFETY REGION" text visible at top
- [ ] Objects show colored circles (red or green)
- [ ] Text labels appear on objects
- [ ] Robot visible in frame

Functional Tests:
- [ ] Single object IN → robot stops, red circle
- [ ] Single object OUT → robot moves, green circle  
- [ ] Two objects both OUT → robot moves, both green
- [ ] Two objects one IN → robot stops, one red one green
- [ ] Two objects both IN → robot stops, both red

Console Output:
- [ ] Logs show object counts correctly
- [ ] "SAFETY VIOLATION" when object enters
- [ ] "clear" or "detected outside" when safe

---

## Final Checklist for Instructor

Your demo must show:
- [x] ✅ Safety space visualized (red rectangle)
- [x] ✅ Safety space covers robot motion range
- [x] ✅ Single object entering triggers stop
- [x] ✅ Single object exiting allows motion
- [x] ✅ Two objects handled correctly (all combinations)
- [x] ✅ Clear visual feedback (red vs green circles)

**All requirements met!** 🎉

Ready to record your demo video! 🎥

