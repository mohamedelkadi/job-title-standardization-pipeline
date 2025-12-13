#!/usr/bin/env python3
"""
Comparison script for Rule-based vs spaCy-based classifiers.

Tests both classifiers on the same dataset and generates a detailed comparison report.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import List, Dict
from src.classifiers.rule_classifier import RuleClassifier, ClassificationResult as RuleResult
from src.classifiers.spacy_classifier import SpacyClassifier, ClassificationResult as SpacyResult
import time


def get_test_titles() -> List[str]:
    """Get test titles for comparison."""
    return [
        "Backend Engineer",
        "Head of Sales",
        "Sales Executive",
        "SWE Intern",
        "Senior Software Engineer",
        "VP of Engineering",
        "CEO",
        "Founder",
        "Product Manager",
        "Data Scientist",
        "Public Relations",
        "Compliance Manager",
        "Technical Account Manager",
        "Sr Program Manager at Amazon Web Services (AWS)",
        "Owner, VITAL AZ LLC",
        "General Partner of Top of the World Media",
        "Communications Consultant at Vanguard",
        "Crisis Assessment and Intervention Clinician",
        "Health Safety Environment Coordinator",
        "TRiO Upward Bound Specialist",
        "Administrative Assistant",
        "Fashion, Portrait & Interior Photographer",
        "Director of Marketing",
        "Senior Sales Manager",
        "Junior Developer",
        "QA Engineer",
        "UX Designer",
        "Customer Success Manager",
        "HR Manager",
        "Finance Director",
    ]


def compare_results(rule_result: RuleResult, spacy_result: SpacyResult) -> Dict:
    """
    Compare two classification results.
    
    Returns:
        Dictionary with comparison metrics
    """
    dept_match = rule_result.department == spacy_result.department
    func_match = rule_result.function == spacy_result.function
    seniority_match = rule_result.seniority == spacy_result.seniority
    
    full_match = dept_match and func_match and seniority_match
    
    return {
        'dept_match': dept_match,
        'func_match': func_match,
        'seniority_match': seniority_match,
        'full_match': full_match,
        'rule_confidence': rule_result.confidence,
        'spacy_confidence': spacy_result.confidence,
        'confidence_diff': abs(rule_result.confidence - spacy_result.confidence),
    }


def generate_report(rule_results: List[Dict], spacy_results: List[Dict], 
                   comparisons: List[Dict], rule_times: List[float], 
                   spacy_times: List[float]) -> str:
    """Generate a detailed comparison report."""
    report = []
    report.append("=" * 100)
    report.append("CLASSIFIER COMPARISON REPORT")
    report.append("Rule-based vs spaCy-based Job Title Classification")
    report.append("=" * 100)
    report.append("")
    
    # Overall Statistics
    report.append("## OVERALL STATISTICS")
    report.append("-" * 100)
    
    total = len(rule_results)
    rule_classified = sum(1 for r in rule_results if r['department'] is not None)
    spacy_classified = sum(1 for r in spacy_results if r['department'] is not None)
    
    rule_avg_conf = sum(r['confidence'] for r in rule_results) / total if total > 0 else 0
    spacy_avg_conf = sum(r['confidence'] for r in spacy_results) / total if total > 0 else 0
    
    rule_avg_time = sum(rule_times) / len(rule_times) if rule_times else 0
    spacy_avg_time = sum(spacy_times) / len(spacy_times) if spacy_times else 0
    
    report.append(f"Total Titles Tested: {total}")
    report.append("")
    report.append("### Classification Coverage")
    report.append(f"  Rule Classifier: {rule_classified}/{total} ({rule_classified/total*100:.1f}%)")
    report.append(f"  spaCy Classifier: {spacy_classified}/{total} ({spacy_classified/total*100:.1f}%)")
    report.append("")
    
    report.append("### Average Confidence Scores")
    report.append(f"  Rule Classifier: {rule_avg_conf:.3f}")
    report.append(f"  spaCy Classifier: {spacy_avg_conf:.3f}")
    report.append(f"  Difference: {abs(rule_avg_conf - spacy_avg_conf):.3f}")
    report.append("")
    
    report.append("### Performance (Average Time per Title)")
    report.append(f"  Rule Classifier: {rule_avg_time*1000:.3f} ms")
    report.append(f"  spaCy Classifier: {spacy_avg_time*1000:.3f} ms")
    report.append(f"  Speed Ratio: {spacy_avg_time/rule_avg_time:.2f}x slower" if rule_avg_time > 0 else "  Speed Ratio: N/A")
    report.append("")
    
    # Agreement Analysis
    report.append("## AGREEMENT ANALYSIS")
    report.append("-" * 100)
    
    full_matches = sum(1 for c in comparisons if c['full_match'])
    dept_matches = sum(1 for c in comparisons if c['dept_match'])
    func_matches = sum(1 for c in comparisons if c['func_match'])
    seniority_matches = sum(1 for c in comparisons if c['seniority_match'])
    
    report.append(f"Full Agreement (Dept + Function + Seniority): {full_matches}/{total} ({full_matches/total*100:.1f}%)")
    report.append(f"Department Agreement: {dept_matches}/{total} ({dept_matches/total*100:.1f}%)")
    report.append(f"Function Agreement: {func_matches}/{total} ({func_matches/total*100:.1f}%)")
    report.append(f"Seniority Agreement: {seniority_matches}/{total} ({seniority_matches/total*100:.1f}%)")
    report.append("")
    
    # Detailed Comparison Table
    report.append("## DETAILED COMPARISON")
    report.append("-" * 100)
    report.append(f"{'Title':<45} {'Rule Dept':<20} {'spaCy Dept':<20} {'Match':<8}")
    report.append("-" * 100)
    
    for i, title in enumerate(get_test_titles()):
        rule_dept = rule_results[i]['department'] or 'N/A'
        spacy_dept = spacy_results[i]['department'] or 'N/A'
        match = "✓" if comparisons[i]['dept_match'] else "✗"
        
        report.append(f"{title[:44]:<45} {rule_dept[:19]:<20} {spacy_dept[:19]:<20} {match:<8}")
    
    report.append("")
    report.append("## DISAGREEMENTS")
    report.append("-" * 100)
    
    disagreements = []
    for i, comp in enumerate(comparisons):
        if not comp['full_match']:
            title = get_test_titles()[i]
            rule_r = rule_results[i]
            spacy_r = spacy_results[i]
            
            disagreements.append({
                'title': title,
                'rule': rule_r,
                'spacy': spacy_r,
                'comparison': comp
            })
    
    if disagreements:
        report.append(f"Found {len(disagreements)} titles with disagreements:\n")
        for d in disagreements:
            report.append(f"Title: {d['title']}")
            report.append(f"  Rule:    Dept={d['rule']['department']}, Func={d['rule']['function']}, Seniority={d['rule']['seniority']}, Conf={d['rule']['confidence']:.2f}")
            report.append(f"  spaCy:   Dept={d['spacy']['department']}, Func={d['spacy']['function']}, Seniority={d['spacy']['seniority']}, Conf={d['spacy']['confidence']:.2f}")
            report.append("")
    else:
        report.append("No disagreements found - perfect agreement!")
        report.append("")
    
    # Distribution Comparison
    report.append("## DISTRIBUTION COMPARISON")
    report.append("-" * 100)
    
    # Department distribution
    rule_dept_dist = {}
    spacy_dept_dist = {}
    for i in range(total):
        if rule_results[i]['department']:
            rule_dept_dist[rule_results[i]['department']] = rule_dept_dist.get(rule_results[i]['department'], 0) + 1
        if spacy_results[i]['department']:
            spacy_dept_dist[spacy_results[i]['department']] = spacy_dept_dist.get(spacy_results[i]['department'], 0) + 1
    
    report.append("### Department Distribution")
    report.append(f"{'Department':<30} {'Rule':<10} {'spaCy':<10} {'Diff':<10}")
    report.append("-" * 60)
    
    all_depts = set(list(rule_dept_dist.keys()) + list(spacy_dept_dist.keys()))
    for dept in sorted(all_depts):
        rule_count = rule_dept_dist.get(dept, 0)
        spacy_count = spacy_dept_dist.get(dept, 0)
        diff = rule_count - spacy_count
        diff_str = f"{diff:+d}" if diff != 0 else "0"
        report.append(f"{dept[:29]:<30} {rule_count:<10} {spacy_count:<10} {diff_str:<10}")
    
    report.append("")
    
    # Seniority distribution
    rule_seniority_dist = {}
    spacy_seniority_dist = {}
    for i in range(total):
        if rule_results[i]['seniority']:
            rule_seniority_dist[rule_results[i]['seniority']] = rule_seniority_dist.get(rule_results[i]['seniority'], 0) + 1
        if spacy_results[i]['seniority']:
            spacy_seniority_dist[spacy_results[i]['seniority']] = spacy_seniority_dist.get(spacy_results[i]['seniority'], 0) + 1
    
    report.append("### Seniority Distribution")
    report.append(f"{'Seniority':<20} {'Rule':<10} {'spaCy':<10} {'Diff':<10}")
    report.append("-" * 50)
    
    all_seniorities = set(list(rule_seniority_dist.keys()) + list(spacy_seniority_dist.keys()))
    for seniority in sorted(all_seniorities):
        rule_count = rule_seniority_dist.get(seniority, 0)
        spacy_count = spacy_seniority_dist.get(seniority, 0)
        diff = rule_count - spacy_count
        diff_str = f"{diff:+d}" if diff != 0 else "0"
        report.append(f"{seniority[:19]:<20} {rule_count:<10} {spacy_count:<10} {diff_str:<10}")
    
    report.append("")
    
    # Confidence Analysis
    report.append("## CONFIDENCE ANALYSIS")
    report.append("-" * 100)
    
    high_conf_rule = sum(1 for r in rule_results if r['confidence'] >= 0.8)
    medium_conf_rule = sum(1 for r in rule_results if 0.5 <= r['confidence'] < 0.8)
    low_conf_rule = sum(1 for r in rule_results if r['confidence'] < 0.5)
    
    high_conf_spacy = sum(1 for r in spacy_results if r['confidence'] >= 0.8)
    medium_conf_spacy = sum(1 for r in spacy_results if 0.5 <= r['confidence'] < 0.8)
    low_conf_spacy = sum(1 for r in spacy_results if r['confidence'] < 0.5)
    
    report.append("### Confidence Distribution")
    report.append(f"{'Level':<15} {'Rule':<10} {'spaCy':<10}")
    report.append("-" * 35)
    report.append(f"{'High (≥0.8)':<15} {high_conf_rule:<10} {high_conf_spacy:<10}")
    report.append(f"{'Medium (0.5-0.8)':<15} {medium_conf_rule:<10} {medium_conf_spacy:<10}")
    report.append(f"{'Low (<0.5)':<15} {low_conf_rule:<10} {low_conf_spacy:<10}")
    report.append("")
    
    # Summary and Recommendations
    report.append("## SUMMARY & RECOMMENDATIONS")
    report.append("-" * 100)
    
    if full_matches / total >= 0.8:
        report.append("✓ High agreement between classifiers - both approaches are consistent")
    elif full_matches / total >= 0.6:
        report.append("⚠ Moderate agreement - some differences in classification")
    else:
        report.append("✗ Low agreement - significant differences in classification")
    
    report.append("")
    
    if rule_avg_time < spacy_avg_time:
        report.append(f"✓ Rule classifier is faster ({rule_avg_time*1000:.2f}ms vs {spacy_avg_time*1000:.2f}ms per title)")
    else:
        report.append(f"✓ spaCy classifier is faster ({spacy_avg_time*1000:.2f}ms vs {rule_avg_time*1000:.2f}ms per title)")
    
    report.append("")
    
    if rule_classified > spacy_classified:
        report.append(f"✓ Rule classifier has better coverage ({rule_classified} vs {spacy_classified} classifications)")
    elif spacy_classified > rule_classified:
        report.append(f"✓ spaCy classifier has better coverage ({spacy_classified} vs {rule_classified} classifications)")
    else:
        report.append(f"✓ Both classifiers have equal coverage ({rule_classified} classifications)")
    
    report.append("")
    report.append("=" * 100)
    
    return "\n".join(report)


def main():
    """Main comparison function."""
    print("Initializing classifiers...")
    
    # Initialize rule classifier
    rule_classifier = RuleClassifier()
    print("✓ Rule classifier initialized")
    
    # Initialize spaCy classifier
    try:
        spacy_classifier = SpacyClassifier()
        print("✓ spaCy classifier initialized")
    except OSError as e:
        print(f"✗ Error initializing spaCy classifier: {e}")
        print("\nPlease install the spaCy model:")
        print("  python -m spacy download en_core_web_sm")
        sys.exit(1)
    
    # Get test titles
    test_titles = get_test_titles()
    print(f"\nTesting {len(test_titles)} titles...\n")
    
    # Run rule classifier
    print("Running rule classifier...")
    rule_results = []
    rule_times = []
    
    for title in test_titles:
        start = time.time()
        result = rule_classifier.classify(title)
        elapsed = time.time() - start
        
        rule_results.append({
            'title': title,
            'department': result.department,
            'function': result.function,
            'seniority': result.seniority,
            'confidence': result.confidence
        })
        rule_times.append(elapsed)
    
    print("✓ Rule classifier completed")
    
    # Run spaCy classifier
    print("Running spaCy classifier...")
    spacy_results = []
    spacy_times = []
    
    for title in test_titles:
        start = time.time()
        result = spacy_classifier.classify(title)
        elapsed = time.time() - start
        
        spacy_results.append({
            'title': title,
            'department': result.department,
            'function': result.function,
            'seniority': result.seniority,
            'confidence': result.confidence
        })
        spacy_times.append(elapsed)
    
    print("✓ spaCy classifier completed")
    
    # Compare results
    print("\nComparing results...")
    comparisons = []
    for i in range(len(test_titles)):
        rule_r = rule_classifier.classify(test_titles[i])
        spacy_r = spacy_classifier.classify(test_titles[i])
        comp = compare_results(rule_r, spacy_r)
        comparisons.append(comp)
    
    # Generate report
    report = generate_report(rule_results, spacy_results, comparisons, rule_times, spacy_times)
    
    # Print report
    print("\n" + report)
    
    # Save report to file
    report_file = "SPACY_CLASSIFIER_COMPARISON_REPORT.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n✓ Report saved to {report_file}")


if __name__ == '__main__':
    main()
