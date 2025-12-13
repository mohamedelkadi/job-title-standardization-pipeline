#!/usr/bin/env python3
"""
Test script for Llama-3.2-1B-Instruct classifier on sample data.

This script tests the Llama classifier on the same sample titles used
in the comparison report and generates detailed results.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
from typing import List, Dict
from src.classifiers.llama_classifier import LlamaClassifier, ClassificationResult
from experiments.compare_classifiers import get_test_titles


def test_llama_classifier():
    """Test Llama classifier on sample titles."""
    print("=" * 100)
    print("LLAMA-3.2-1B-INSTRUCT CLASSIFIER TEST")
    print("=" * 100)
    
    # Check authentication first
    print("\n[1/4] Checking HuggingFace authentication...")
    try:
        from huggingface_hub import HfFolder
        token = HfFolder.get_token()
        if not token:
            print("⚠ No HuggingFace token found.")
            print("\nTo use this model, you need to:")
            print("1. Get a HuggingFace token: https://huggingface.co/settings/tokens")
            print("2. Log in: huggingface-cli login")
            print("3. Request access: https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct")
            print("   (Click 'Agree and access repository')")
            print("4. Run this script again")
            sys.exit(1)
        else:
            print("✓ Authentication token found")
    except ImportError:
        print("⚠ huggingface_hub not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub"])
        print("✓ Installed. Please run this script again.")
        sys.exit(1)
    
    # Initialize classifier
    print("\n[2/4] Initializing Llama classifier...")
    try:
        classifier = LlamaClassifier()
        print("✓ Classifier initialized")
    except Exception as e:
        print(f"✗ Error initializing classifier: {e}")
        sys.exit(1)
    
    # Get test titles
    print("\n[3/4] Loading test titles...")
    test_titles = get_test_titles()
    print(f"✓ Loaded {len(test_titles)} test titles")
    
    # Run classification
    print("\n[4/4] Running classifications...")
    print("This may take a while (Llama inference is slower than rule-based methods)...\n")
    
    results = []
    times = []
    
    for i, title in enumerate(test_titles, 1):
        print(f"[{i}/{len(test_titles)}] Classifying: {title[:60]}")
        start_time = time.time()
        try:
            result = classifier.classify(title)
            elapsed = time.time() - start_time
            times.append(elapsed)
            
            results.append({
                'title': title,
                'department': result.department,
                'function': result.function,
                'seniority': result.seniority,
                'confidence': result.confidence,
                'time': elapsed
            })
            
            # Print quick result
            dept = result.department or 'N/A'
            seniority = result.seniority or 'N/A'
            print(f"    → Dept: {dept}, Seniority: {seniority}, Conf: {result.confidence:.2f}, Time: {elapsed:.2f}s")
        except Exception as e:
            print(f"    ✗ Error: {e}")
            results.append({
                'title': title,
                'department': None,
                'function': None,
                'seniority': None,
                'confidence': 0.0,
                'time': 0.0
            })
            times.append(0.0)
    
    # Generate report
    print("\n" + "=" * 100)
    print("RESULTS SUMMARY")
    print("=" * 100)
    
    total = len(results)
    classified = sum(1 for r in results if r['department'] is not None)
    avg_conf = sum(r['confidence'] for r in results) / total if total > 0 else 0
    avg_time = sum(times) / len(times) if times else 0
    total_time = sum(times)
    
    print(f"\nTotal Titles Tested: {total}")
    print(f"Successfully Classified: {classified}/{total} ({classified/total*100:.1f}%)")
    print(f"Average Confidence: {avg_conf:.3f}")
    print(f"Average Time per Title: {avg_time*1000:.2f} ms")
    print(f"Total Processing Time: {total_time:.2f} s")
    
    # Detailed results table
    print("\n" + "=" * 100)
    print("DETAILED RESULTS")
    print("=" * 100)
    print(f"{'Title':<50} {'Department':<25} {'Function':<30} {'Seniority':<15} {'Confidence':<10}")
    print("-" * 130)
    
    for r in results:
        dept = r['department'] or 'N/A'
        func = r['function'] or 'N/A'
        seniority = r['seniority'] or 'N/A'
        conf = r['confidence']
        
        print(f"{r['title'][:49]:<50} {dept[:24]:<25} {func[:29]:<30} {seniority[:14]:<15} {conf:.2f}")
    
    # Distribution analysis
    print("\n" + "=" * 100)
    print("DISTRIBUTION ANALYSIS")
    print("=" * 100)
    
    # Department distribution
    dept_dist = {}
    for r in results:
        if r['department']:
            dept_dist[r['department']] = dept_dist.get(r['department'], 0) + 1
    
    print("\nDepartment Distribution:")
    if dept_dist:
        for dept, count in sorted(dept_dist.items(), key=lambda x: -x[1]):
            print(f"  {dept}: {count}")
    else:
        print("  No classifications")
    
    # Seniority distribution
    seniority_dist = {}
    for r in results:
        if r['seniority']:
            seniority_dist[r['seniority']] = seniority_dist.get(r['seniority'], 0) + 1
    
    print("\nSeniority Distribution:")
    if seniority_dist:
        for seniority, count in sorted(seniority_dist.items(), key=lambda x: -x[1]):
            print(f"  {seniority}: {count}")
    else:
        print("  No classifications")
    
    # Confidence analysis
    high_conf = sum(1 for r in results if r['confidence'] >= 0.8)
    medium_conf = sum(1 for r in results if 0.5 <= r['confidence'] < 0.8)
    low_conf = sum(1 for r in results if r['confidence'] < 0.5)
    
    print("\nConfidence Distribution:")
    print(f"  High (≥0.8): {high_conf}")
    print(f"  Medium (0.5-0.8): {medium_conf}")
    print(f"  Low (<0.5): {low_conf}")
    
    print("\n" + "=" * 100)
    
    # Save results to file
    output_file = "LLAMA_CLASSIFIER_TEST_RESULTS.md"
    with open(output_file, 'w') as f:
        f.write("# Llama-3.2-1B-Instruct Classifier Test Results\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Titles Tested:** {total}\n")
        f.write(f"**Successfully Classified:** {classified}/{total} ({classified/total*100:.1f}%)\n")
        f.write(f"**Average Confidence:** {avg_conf:.3f}\n")
        f.write(f"**Average Time per Title:** {avg_time*1000:.2f} ms\n")
        f.write(f"**Total Processing Time:** {total_time:.2f} s\n\n")
        
        f.write("## Detailed Results\n\n")
        f.write("| Title | Department | Function | Seniority | Confidence |\n")
        f.write("|-------|------------|----------|-----------|------------|\n")
        
        for r in results:
            dept = r['department'] or 'N/A'
            func = r['function'] or 'N/A'
            seniority = r['seniority'] or 'N/A'
            conf = r['confidence']
            f.write(f"| {r['title']} | {dept} | {func} | {seniority} | {conf:.2f} |\n")
    
    print(f"\n✓ Results saved to {output_file}")
    
    return results


if __name__ == '__main__':
    test_llama_classifier()
