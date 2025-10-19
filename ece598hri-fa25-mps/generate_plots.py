#!/usr/bin/env python3
"""
Generate plots and figures for MP1 report from experimental data.
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_data(csv_file):
    """Load experimental data from CSV"""
    data = {
        'trials': [],
        'detection_latency': [],
        'stop_latency': [],
        'total_response': [],
        'min_distance': [],
        'successes': []
    }
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['trials'].append(int(row['Trial']))
            
            if row['Detection_Latency_ms']:
                data['detection_latency'].append(float(row['Detection_Latency_ms']))
            else:
                data['detection_latency'].append(None)
            
            if row['Stop_Latency_ms']:
                data['stop_latency'].append(float(row['Stop_Latency_ms']))
            else:
                data['stop_latency'].append(None)
            
            if row['Total_Response_ms']:
                data['total_response'].append(float(row['Total_Response_ms']))
            else:
                data['total_response'].append(None)
            
            if row['Min_Distance_cm']:
                data['min_distance'].append(float(row['Min_Distance_cm']))
            else:
                data['min_distance'].append(None)
            
            data['successes'].append(row['Detection_Success'] == '✓')
    
    return data

def plot_response_times_over_trials(data, output_dir):
    """Plot response times across all trials"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    trials = data['trials']
    
    # Filter out None values
    det_lat = [d if d is not None else 0 for d in data['detection_latency']]
    stop_lat = [s if s is not None else 0 for s in data['stop_latency']]
    total_resp = [t if t is not None else 0 for t in data['total_response']]
    
    ax.plot(trials, det_lat, 'o-', label='Detection Latency', linewidth=2, markersize=8)
    ax.plot(trials, stop_lat, 's-', label='Stop Latency', linewidth=2, markersize=8)
    ax.plot(trials, total_resp, '^-', label='Total Response Time', linewidth=2, markersize=8)
    
    ax.set_xlabel('Trial Number', fontsize=14)
    ax.set_ylabel('Time (ms)', fontsize=14)
    ax.set_title('Response Times Across All Trials', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(trials)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'response_times_trials.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created: response_times_trials.png")

def plot_response_time_distribution(data, output_dir):
    """Plot histogram of total response times"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Filter out None and zero values for better visualization
    total_resp = [t for t in data['total_response'] if t is not None and t > 0]
    
    # Histogram
    ax1.hist(total_resp, bins=15, edgecolor='black', alpha=0.7, color='steelblue')
    ax1.axvline(np.mean(total_resp), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(total_resp):.0f} ms')
    ax1.axvline(np.median(total_resp), color='green', linestyle='--', linewidth=2, label=f'Median: {np.median(total_resp):.0f} ms')
    ax1.set_xlabel('Total Response Time (ms)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Distribution of Total Response Times', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    ax2.boxplot(total_resp, vert=True)
    ax2.set_ylabel('Total Response Time (ms)', fontsize=12)
    ax2.set_title('Response Time Box Plot', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'response_time_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created: response_time_distribution.png")

def plot_bimodal_analysis(data, output_dir):
    """Separate fast and slow trials to show bimodal distribution"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    total_resp = [t for t in data['total_response'] if t is not None]
    trials = [i+1 for i, t in enumerate(data['total_response']) if t is not None]
    
    # Classify trials as fast (<1000ms) or slow (>=1000ms)
    fast_trials = [(t, r) for t, r in zip(trials, total_resp) if r < 1000]
    slow_trials = [(t, r) for t, r in zip(trials, total_resp) if r >= 1000]
    
    if fast_trials:
        fast_t, fast_r = zip(*fast_trials)
        ax.scatter(fast_t, fast_r, s=150, c='green', marker='o', label=f'Fast Trials (n={len(fast_trials)})', alpha=0.7, edgecolors='black', linewidths=2)
    
    if slow_trials:
        slow_t, slow_r = zip(*slow_trials)
        ax.scatter(slow_t, slow_r, s=150, c='red', marker='s', label=f'Slow Trials (n={len(slow_trials)})', alpha=0.7, edgecolors='black', linewidths=2)
    
    # Add threshold line
    ax.axhline(1000, color='orange', linestyle='--', linewidth=2, label='1000 ms threshold', alpha=0.7)
    
    ax.set_xlabel('Trial Number', fontsize=14)
    ax.set_ylabel('Total Response Time (ms)', fontsize=14)
    ax.set_title('Bimodal Distribution: Fast vs Slow Trials', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(1, len(trials)+1))
    
    plt.tight_layout()
    plt.savefig(output_dir / 'bimodal_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created: bimodal_analysis.png")

def plot_distance_measurements(data, output_dir):
    """Plot minimum distances over trials"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    trials = data['trials']
    distances = [d if d is not None else 0 for d in data['min_distance']]
    
    ax.bar(trials, distances, color='steelblue', edgecolor='black', alpha=0.7)
    ax.axhline(5, color='red', linestyle='--', linewidth=2, label='Minimum Required (5 cm)')
    ax.axhline(np.mean([d for d in distances if d > 0]), color='green', linestyle='--', 
               linewidth=2, label=f'Mean: {np.mean([d for d in distances if d > 0]):.1f} cm')
    
    ax.set_xlabel('Trial Number', fontsize=14)
    ax.set_ylabel('Minimum Distance (cm)', fontsize=14)
    ax.set_title('Minimum Safe Distance per Trial', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_xticks(trials)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'distance_measurements.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created: distance_measurements.png")

def plot_success_rate(data, output_dir):
    """Plot detection success rate"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    total = len(data['successes'])
    successes = sum(data['successes'])
    failures = total - successes
    
    colors = ['green', 'red']
    labels = [f'Success\n({successes}/{total})', f'Failure\n({failures}/{total})']
    sizes = [successes, failures] if failures > 0 else [successes]
    colors_used = colors if failures > 0 else [colors[0]]
    labels_used = labels if failures > 0 else [labels[0]]
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels_used, colors=colors_used, autopct='%1.1f%%',
                                        startangle=90, textprops={'fontsize': 14, 'weight': 'bold'})
    
    # Make percentage text white for better visibility
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(16)
    
    ax.set_title(f'Detection Success Rate: {successes}/{total} = {100*successes/total:.1f}%', 
                 fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'success_rate.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created: success_rate.png")

def plot_latency_comparison(data, output_dir):
    """Compare detection and stop latencies"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Filter out extreme outliers for better visualization
    det_lat = [d for d in data['detection_latency'] if d is not None and d < 5000]
    stop_lat = [s for s in data['stop_latency'] if s is not None and s < 2000]
    
    bp = ax.boxplot([det_lat, stop_lat], labels=['Detection Latency', 'Stop Latency'],
                     patch_artist=True, showmeans=True, meanline=True)
    
    # Color the boxes
    colors = ['lightblue', 'lightcoral']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Latency (ms)', fontsize=14)
    ax.set_title('Detection vs Stop Latency Comparison', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add statistics
    det_mean = np.mean(det_lat)
    stop_mean = np.mean(stop_lat)
    ax.text(1, det_mean, f'Mean: {det_mean:.0f}ms', ha='center', va='bottom', fontsize=10)
    ax.text(2, stop_mean, f'Mean: {stop_mean:.0f}ms', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'latency_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created: latency_comparison.png")

def plot_system_performance_summary(data, output_dir):
    """Create a summary dashboard of key metrics"""
    fig = plt.figure(figsize=(14, 8))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # 1. Success Rate (pie)
    ax1 = fig.add_subplot(gs[0, 0])
    total = len(data['successes'])
    successes = sum(data['successes'])
    ax1.pie([successes, total-successes] if total > successes else [successes], 
            labels=['Success', 'Failure'] if total > successes else ['Success'],
            colors=['green', 'red'] if total > successes else ['green'],
            autopct='%1.0f%%', startangle=90)
    ax1.set_title(f'Detection Success\n{successes}/{total} trials', fontweight='bold')
    
    # 2. Response Time Stats
    ax2 = fig.add_subplot(gs[0, 1])
    total_resp = [t for t in data['total_response'] if t is not None]
    metrics = ['Mean', 'Median', 'Min', 'Max']
    values = [np.mean(total_resp), np.median(total_resp), np.min(total_resp), np.max(total_resp)]
    bars = ax2.barh(metrics, values, color=['steelblue', 'lightgreen', 'gold', 'salmon'])
    ax2.set_xlabel('Time (ms)')
    ax2.set_title('Response Time Statistics', fontweight='bold')
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax2.text(val, i, f' {val:.0f}ms', va='center', fontweight='bold')
    
    # 3. Distance Stats
    ax3 = fig.add_subplot(gs[0, 2])
    distances = [d for d in data['min_distance'] if d is not None]
    metrics = ['Mean', 'Median', 'Min', 'Max']
    values = [np.mean(distances), np.median(distances), np.min(distances), np.max(distances)]
    bars = ax3.barh(metrics, values, color=['steelblue', 'lightgreen', 'gold', 'salmon'])
    ax3.axvline(5, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Req: 5cm')
    ax3.set_xlabel('Distance (cm)')
    ax3.set_title('Safe Distance Statistics', fontweight='bold')
    ax3.legend(fontsize=8)
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax3.text(val, i, f' {val:.1f}cm', va='center', fontweight='bold')
    
    # 4. Response times over trials
    ax4 = fig.add_subplot(gs[1, :])
    trials = data['trials']
    total_resp = [t if t is not None else 0 for t in data['total_response']]
    colors_list = ['green' if t < 1000 else 'red' for t in total_resp]
    ax4.bar(trials, total_resp, color=colors_list, edgecolor='black', alpha=0.7)
    ax4.axhline(500, color='orange', linestyle='--', linewidth=2, label='Target: 500ms', alpha=0.7)
    ax4.set_xlabel('Trial Number', fontsize=12)
    ax4.set_ylabel('Total Response Time (ms)', fontsize=12)
    ax4.set_title('Response Time per Trial (Green: Fast <1s, Red: Slow ≥1s)', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle('MP1 System Performance Summary', fontsize=18, fontweight='bold', y=0.98)
    
    plt.savefig(output_dir / 'performance_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Created: performance_summary.png")

def main():
    # Paths
    data_file = Path('/Users/samuel/Workspace/Class/hri_ece598/ece598hri-fa25-mps/results/mp1_experiment_data_20251018_164122.csv')
    output_dir = Path('/Users/samuel/Workspace/Class/hri_ece598/ece598hri-fa25-mps/Figures')
    
    print("="*60)
    print("Generating plots for MP1 report...")
    print("="*60)
    
    # Load data
    print(f"\nLoading data from: {data_file.name}")
    data = load_data(data_file)
    print(f"✓ Loaded {len(data['trials'])} trials")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Generate all plots
    print(f"\nGenerating plots in: {output_dir}")
    print("-"*60)
    
    plot_response_times_over_trials(data, output_dir)
    plot_response_time_distribution(data, output_dir)
    plot_bimodal_analysis(data, output_dir)
    plot_distance_measurements(data, output_dir)
    plot_success_rate(data, output_dir)
    plot_latency_comparison(data, output_dir)
    plot_system_performance_summary(data, output_dir)
    
    print("-"*60)
    print(f"\n✅ All plots generated successfully!")
    print(f"📁 Location: {output_dir}")
    print("="*60)
    
    # List all figures
    print("\nAvailable figures:")
    for img in sorted(output_dir.glob('*.png')):
        print(f"  - {img.name}")
    for img in sorted(output_dir.glob('*.JPG')):
        print(f"  - {img.name}")

if __name__ == '__main__':
    main()

