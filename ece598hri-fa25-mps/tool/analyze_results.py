#!/usr/bin/env python3
"""
Analysis script for MP1 experimental data.
Calculates statistics and generates summary from CSV data.
"""

import csv
import sys
import math
from pathlib import Path

def load_data(csv_file):
    """Load data from CSV file"""
    data = {
        'trials': [],
        'detection_latency': [],
        'stop_latency': [],
        'total_response': [],
        'min_distance': [],
        'successes': 0,
        'failures': 0
    }
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['trials'].append(int(row['Trial']))
            
            # Parse numeric values
            if row['Detection_Latency_ms']:
                data['detection_latency'].append(float(row['Detection_Latency_ms']))
            
            if row['Stop_Latency_ms']:
                data['stop_latency'].append(float(row['Stop_Latency_ms']))
            
            if row['Total_Response_ms']:
                data['total_response'].append(float(row['Total_Response_ms']))
            
            if row['Min_Distance_cm']:
                data['min_distance'].append(float(row['Min_Distance_cm']))
            
            # Count successes
            if row['Detection_Success'] == '✓':
                data['successes'] += 1
            else:
                data['failures'] += 1
    
    return data

def calculate_stats(values):
    """Calculate mean and std dev"""
    if not values:
        return None, None
    
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std_dev = math.sqrt(variance)
    
    return mean, std_dev

def print_summary(data):
    """Print statistical summary"""
    total_trials = len(data['trials'])
    
    print("="*70)
    print("MP1 EXPERIMENTAL RESULTS SUMMARY")
    print("="*70)
    print()
    
    # Detection Success Rate
    success_rate = (data['successes'] / total_trials) * 100 if total_trials > 0 else 0
    print(f"DETECTION PERFORMANCE")
    print(f"  Total Trials:       {total_trials}")
    print(f"  Successful:         {data['successes']}")
    print(f"  Failed:             {data['failures']}")
    print(f"  Success Rate:       {success_rate:.1f}%")
    print()
    
    # Detection Latency
    det_mean, det_std = calculate_stats(data['detection_latency'])
    if det_mean:
        print(f"DETECTION LATENCY")
        print(f"  Mean:               {det_mean:.1f} ms")
        print(f"  Std Dev:            {det_std:.1f} ms")
        print(f"  Min:                {min(data['detection_latency']):.1f} ms")
        print(f"  Max:                {max(data['detection_latency']):.1f} ms")
        print()
    
    # Stop Latency
    stop_mean, stop_std = calculate_stats(data['stop_latency'])
    if stop_mean:
        print(f"STOP LATENCY (Detection to Stop)")
        print(f"  Mean:               {stop_mean:.1f} ms")
        print(f"  Std Dev:            {stop_std:.1f} ms")
        print(f"  Min:                {min(data['stop_latency']):.1f} ms")
        print(f"  Max:                {max(data['stop_latency']):.1f} ms")
        print()
    
    # Total Response Time
    total_mean, total_std = calculate_stats(data['total_response'])
    if total_mean:
        print(f"TOTAL RESPONSE TIME (Entry to Stop)")
        print(f"  Mean:               {total_mean:.1f} ms")
        print(f"  Std Dev:            {total_std:.1f} ms")
        print(f"  Min:                {min(data['total_response']):.1f} ms")
        print(f"  Max:                {max(data['total_response']):.1f} ms")
        print()
    
    # Minimum Distance
    dist_mean, dist_std = calculate_stats(data['min_distance'])
    if dist_mean:
        print(f"MINIMUM SAFE DISTANCE")
        print(f"  Mean:               {dist_mean:.1f} cm")
        print(f"  Std Dev:            {dist_std:.1f} cm")
        print(f"  Min:                {min(data['min_distance']):.1f} cm")
        print(f"  Max:                {max(data['min_distance']):.1f} cm")
        print()
    
    # Hypothesis Testing
    print("="*70)
    print("HYPOTHESIS EVALUATION")
    print("="*70)
    
    target_success = 95.0
    target_response = 500.0
    target_distance = 5.0
    
    print(f"  Detection Success:  {success_rate:.1f}% ", end="")
    if success_rate >= target_success:
        print("✓ PASS (target: ≥95%)")
    elif success_rate >= 90.0:
        print("~ ACCEPTABLE (target: ≥95%, acceptable: ≥90%)")
    else:
        print("✗ FAIL (target: ≥95%)")
    
    if total_mean:
        print(f"  Response Time:      {total_mean:.1f} ms ", end="")
        if total_mean < target_response:
            print("✓ PASS (target: <500ms)")
        elif total_mean < 650:
            print("~ ACCEPTABLE (target: <500ms, acceptable: <650ms)")
        else:
            print("✗ FAIL (target: <500ms)")
    
    if dist_mean:
        print(f"  Safe Distance:      {dist_mean:.1f} cm ", end="")
        if dist_mean > 10.0:
            print("✓ EXCELLENT (target: >5cm)")
        elif dist_mean > target_distance:
            print("✓ PASS (target: >5cm)")
        else:
            print("✗ FAIL (target: >5cm)")
    
    print()
    print("="*70)

def generate_table(data):
    """Generate formatted table for report"""
    print("\nFORMATTED TABLE FOR REPORT")
    print("-"*120)
    print(f"{'Trial':<8}{'Entry':<12}{'Detection':<14}{'Stop':<12}{'Det Lat':<12}{'Stop Lat':<12}{'Total':<12}{'Distance':<12}{'Success':<10}")
    print(f"{'':8}{'Time (s)':<12}{'Time (s)':<14}{'Time (s)':<12}{'(ms)':<12}{'(ms)':<12}{'Resp (ms)':<12}{'(cm)':<12}{'':10}")
    print("-"*120)
    
    with open(sys.argv[1], 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trial = row['Trial']
            entry = row['Entry_Time_s']
            detection = row['Detection_Time_s'] if row['Detection_Time_s'] else '—'
            stop = row['Stop_Time_s'] if row['Stop_Time_s'] else '—'
            det_lat = row['Detection_Latency_ms'] if row['Detection_Latency_ms'] else '—'
            stop_lat = row['Stop_Latency_ms'] if row['Stop_Latency_ms'] else '—'
            total = row['Total_Response_ms'] if row['Total_Response_ms'] else '—'
            distance = row['Min_Distance_cm'] if row['Min_Distance_cm'] else '—'
            success = row['Detection_Success']
            
            print(f"{trial:<8}{entry:<12}{detection:<14}{stop:<12}{det_lat:<12}{stop_lat:<12}{total:<12}{distance:<12}{success:<10}")
    
    print("-"*120)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_results.py <csv_file>")
        print("\nExample:")
        print("  python3 analyze_results.py mp1_experiment_data_20251018_143052.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not Path(csv_file).exists():
        print(f"Error: File '{csv_file}' not found")
        sys.exit(1)
    
    # Load and analyze data
    data = load_data(csv_file)
    
    # Print summary
    print_summary(data)
    
    # Generate table
    generate_table(data)
    
    print("\nAnalysis complete!")

if __name__ == '__main__':
    main()

