#!/usr/bin/env python3
"""
Integration tests for Validator with actual classifier outputs.

Demonstrates how the Validator works in the pipeline with real classifier results.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.validator import Validator
from src.classifiers.rule_classifier import RuleClassifier, ClassificationResult


def test_validator_with_rule_classifier():
    """Test validator with RuleClassifier outputs."""
    print("=" * 70)
    print("Integration Test: Validator + Rule Classifier")
    print("=" * 70)
    
    # Initialize components
    classifier = RuleClassifier()
    validator = Validator(strict_mode=True)
    
    # Test titles
    test_titles = [
        "Senior Software Engineer",
        "Head of Sales",
        "VP of Engineering",
        "Invalid Title That Should Fail",
        "Sales Manager",
        "Backend Engineer",
    ]
    
    print(f"\nTesting {len(test_titles)} job titles...\n")
    
    valid_count = 0
    invalid_count = 0
    
    for title in test_titles:
        print(f"Title: '{title}'")
        print("-" * 70)
        
        # Classify
        classification = classifier.classify(title)
        
        print(f"  Classification:")
        print(f"    Department: {classification.department}")
        print(f"    Function: {classification.function}")
        print(f"    Seniority: {classification.seniority}")
        print(f"    Confidence: {classification.confidence:.2f}")
        print(f"    Method: {classification.method}")
        
        # Validate
        validation_result = validator.validate_classification_result(classification)
        
        print(f"  Validation:")
        print(f"    Valid: {validation_result.is_valid}")
        
        if validation_result.issues:
            print(f"    Issues ({len(validation_result.issues)}):")
            for issue in validation_result.issues:
                severity_icon = "❌" if issue.severity.value == "error" else "⚠️"
                print(f"      {severity_icon} [{issue.severity.value.upper()}] {issue.field}: {issue.message}")
        else:
            print(f"    ✅ No issues found")
        
        if validation_result.is_valid:
            valid_count += 1
        else:
            invalid_count += 1
        
        print()
    
    print("=" * 70)
    print(f"Summary: {valid_count} valid, {invalid_count} invalid out of {len(test_titles)} classifications")
    print("=" * 70)


def test_validator_pipeline_workflow():
    """Demonstrate validator in a pipeline workflow."""
    print("\n" + "=" * 70)
    print("Pipeline Workflow Example: Classify -> Validate -> Store")
    print("=" * 70)
    
    classifier = RuleClassifier()
    validator = Validator(strict_mode=True)
    
    # Simulate processing a batch of titles
    titles = [
        "Senior Software Engineer",
        "Sales Director",
        "Marketing Manager",
    ]
    
    results = []
    
    for title in titles:
        # Step 1: Classify
        classification = classifier.classify(title)
        
        # Step 2: Validate
        validation = validator.validate_classification_result(classification)
        
        # Step 3: Decide whether to store
        if validation.is_valid:
            # Store in database
            results.append({
                "title": title,
                "classification": classification,
                "status": "stored",
                "validation": validation
            })
        else:
            # Reject or flag for review
            results.append({
                "title": title,
                "classification": classification,
                "status": "rejected",
                "validation": validation
            })
    
    print("\nPipeline Results:")
    print("-" * 70)
    for result in results:
        status_icon = "✅" if result["status"] == "stored" else "❌"
        print(f"{status_icon} {result['title']}")
        print(f"   Status: {result['status']}")
        if result['status'] == "rejected":
            errors = [issue for issue in result['validation'].issues if issue.severity.value == "error"]
            print(f"   Errors: {len(errors)}")
            for error in errors[:2]:  # Show first 2 errors
                print(f"     - {error.field}: {error.message}")
        print()


if __name__ == "__main__":
    test_validator_with_rule_classifier()
    test_validator_pipeline_workflow()
