#!/usr/bin/env python3
"""
Tests for the Validator class.

Tests validation of job title standardization results to ensure
taxonomy compliance and data quality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from src.validator import Validator, ValidationResult, ValidationSeverity
from src.classifiers.rule_classifier import ClassificationResult


class TestValidator(unittest.TestCase):
    """Test cases for the Validator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator_strict = Validator(strict_mode=True)
        self.validator_lenient = Validator(strict_mode=False)
    
    def test_valid_classification(self):
        """Test that a valid classification passes validation."""
        result = self.validator_strict.validate(
            department="Engineering & Technical",
            function="Software Development",
            seniority="Senior",
            confidence=0.95,
            method="rule"
        )
        
        self.assertTrue(result.is_valid)
        self.assertFalse(result.has_errors())
        self.assertEqual(len(result.issues), 0)
    
    def test_invalid_department(self):
        """Test that an invalid department is caught."""
        result = self.validator_strict.validate(
            department="Invalid Department",
            function="Software Development",
            seniority="Senior",
            confidence=0.95
        )
        
        self.assertFalse(result.is_valid)
        self.assertTrue(result.has_errors())
        self.assertTrue(any("Invalid department" in issue.message for issue in result.issues))
    
    def test_invalid_function(self):
        """Test that an invalid function is caught."""
        result = self.validator_strict.validate(
            department="Engineering & Technical",
            function="Invalid Function",
            seniority="Senior",
            confidence=0.95
        )
        
        self.assertFalse(result.is_valid)
        self.assertTrue(result.has_errors())
        self.assertTrue(any("Invalid function" in issue.message for issue in result.issues))
    
    def test_function_wrong_department(self):
        """Test that a function belonging to wrong department is caught."""
        result = self.validator_strict.validate(
            department="Sales",
            function="Software Development",  # Belongs to Engineering & Technical
            seniority="Senior",
            confidence=0.95
        )
        
        self.assertFalse(result.is_valid)
        self.assertTrue(result.has_errors())
        self.assertTrue(any("belongs to department" in issue.message for issue in result.issues))
    
    def test_invalid_seniority(self):
        """Test that an invalid seniority level is caught."""
        result = self.validator_strict.validate(
            department="Engineering & Technical",
            function="Software Development",
            seniority="Invalid Seniority",
            confidence=0.95
        )
        
        self.assertFalse(result.is_valid)
        self.assertTrue(result.has_errors())
        self.assertTrue(any("Invalid seniority" in issue.message for issue in result.issues))
    
    def test_low_confidence_warning(self):
        """Test that low confidence generates a warning."""
        result = self.validator_strict.validate(
            department="Engineering & Technical",
            function="Software Development",
            seniority="Senior",
            confidence=0.3  # Below threshold
        )
        
        # Low confidence is a warning, not an error
        self.assertTrue(result.is_valid)  # Still valid
        self.assertTrue(result.has_warnings())
        self.assertTrue(any("Low confidence" in issue.message for issue in result.issues))
    
    def test_invalid_confidence_range(self):
        """Test that confidence outside 0.0-1.0 is caught."""
        # Test confidence > 1.0
        result = self.validator_strict.validate(
            department="Engineering & Technical",
            function="Software Development",
            seniority="Senior",
            confidence=1.5
        )
        
        self.assertFalse(result.is_valid)
        self.assertTrue(result.has_errors())
        self.assertTrue(any("Confidence score must be between" in issue.message for issue in result.issues))
        
        # Test confidence < 0.0
        result = self.validator_strict.validate(
            department="Engineering & Technical",
            function="Software Development",
            seniority="Senior",
            confidence=-0.1
        )
        
        self.assertFalse(result.is_valid)
        self.assertTrue(result.has_errors())
    
    def test_missing_fields_strict_mode(self):
        """Test that missing fields fail in strict mode."""
        # Missing department
        result = self.validator_strict.validate(
            department=None,
            function="Software Development",
            seniority="Senior",
            confidence=0.95
        )
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Department is required" in issue.message for issue in result.issues))
        
        # Missing function
        result = self.validator_strict.validate(
            department="Engineering & Technical",
            function=None,
            seniority="Senior",
            confidence=0.95
        )
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Function is required" in issue.message for issue in result.issues))
        
        # Missing seniority
        result = self.validator_strict.validate(
            department="Engineering & Technical",
            function="Software Development",
            seniority=None,
            confidence=0.95
        )
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Seniority is required" in issue.message for issue in result.issues))
    
    def test_missing_fields_lenient_mode(self):
        """Test that missing fields are allowed in lenient mode."""
        result = self.validator_lenient.validate(
            department=None,
            function="Software Development",
            seniority="Senior",
            confidence=0.95
        )
        
        # Should be valid (no errors), but may have warnings
        self.assertTrue(result.is_valid)
        self.assertFalse(result.has_errors())
    
    def test_function_without_department_warning(self):
        """Test that a function without department generates a warning."""
        result = self.validator_lenient.validate(
            department=None,
            function="Software Development",
            seniority="Senior",
            confidence=0.95
        )
        
        self.assertTrue(result.is_valid)  # No errors
        self.assertTrue(result.has_warnings())  # But has warnings
        self.assertTrue(any("no department specified" in issue.message.lower() for issue in result.issues))
    
    def test_all_valid_departments(self):
        """Test that all valid departments pass validation."""
        for department in Validator.VALID_DEPARTMENTS:
            result = self.validator_strict.validate(
                department=department,
                function=None,  # Skip function validation for this test
                seniority=None,
                confidence=0.95
            )
            # Should not have department-related errors
            dept_errors = [issue for issue in result.issues if issue.field == "department"]
            self.assertEqual(len(dept_errors), 0, f"Department '{department}' should be valid")
    
    def test_all_valid_seniority_levels(self):
        """Test that all valid seniority levels pass validation."""
        for seniority in Validator.VALID_SENIORITY_LEVELS:
            result = self.validator_strict.validate(
                department=None,
                function=None,
                seniority=seniority,
                confidence=0.95
            )
            # Should not have seniority-related errors
            seniority_errors = [issue for issue in result.issues if issue.field == "seniority"]
            self.assertEqual(len(seniority_errors), 0, f"Seniority '{seniority}' should be valid")
    
    def test_all_department_function_combinations(self):
        """Test that all valid department-function combinations pass validation."""
        for department, functions in Validator.DEPARTMENT_FUNCTIONS.items():
            for function in functions:
                result = self.validator_strict.validate(
                    department=department,
                    function=function,
                    seniority="Senior",
                    confidence=0.95
                )
                # Should not have function-related errors
                func_errors = [issue for issue in result.issues if issue.field == "function"]
                self.assertEqual(
                    len(func_errors), 0,
                    f"Function '{function}' should belong to department '{department}'"
                )
    
    def test_validate_classification_result(self):
        """Test validation using ClassificationResult object."""
        classification = ClassificationResult(
            department="Sales",
            function="Sales",
            seniority="Head",
            confidence=0.92,
            method="rule"
        )
        
        result = self.validator_strict.validate_classification_result(classification)
        self.assertTrue(result.is_valid)
        self.assertFalse(result.has_errors())
    
    def test_unknown_method_warning(self):
        """Test that unknown classification method generates a warning."""
        result = self.validator_strict.validate(
            department="Engineering & Technical",
            function="Software Development",
            seniority="Senior",
            confidence=0.95,
            method="unknown_method"
        )
        
        self.assertTrue(result.is_valid)  # Still valid
        self.assertTrue(result.has_warnings())
        self.assertTrue(any("Unknown classification method" in issue.message for issue in result.issues))
    
    def test_valid_methods(self):
        """Test that valid methods don't generate warnings."""
        valid_methods = ["rule", "llm_gpt35", "llm_gpt4", "spacy", "llama", "unknown"]
        
        for method in valid_methods:
            result = self.validator_strict.validate(
                department="Engineering & Technical",
                function="Software Development",
                seniority="Senior",
                confidence=0.95,
                method=method
            )
            
            method_warnings = [issue for issue in result.issues if issue.field == "method"]
            self.assertEqual(len(method_warnings), 0, f"Method '{method}' should not generate warnings")
    
    def test_multiple_errors(self):
        """Test that multiple validation errors are all reported."""
        result = self.validator_strict.validate(
            department="Invalid Department",
            function="Invalid Function",
            seniority="Invalid Seniority",
            confidence=1.5  # Also invalid
        )
        
        self.assertFalse(result.is_valid)
        self.assertTrue(len(result.issues) >= 4)  # At least 4 errors
        errors = [issue for issue in result.issues if issue.severity == ValidationSeverity.ERROR]
        self.assertTrue(len(errors) >= 4)
    
    def test_edge_case_empty_strings(self):
        """Test that empty strings are treated as None."""
        result = self.validator_strict.validate(
            department="",
            function="",
            seniority="",
            confidence=0.95
        )
        
        # Empty strings should be treated as missing in strict mode
        self.assertFalse(result.is_valid)
        self.assertTrue(result.has_errors())
    
    def test_real_world_examples(self):
        """Test validation with real-world classification examples."""
        examples = [
            # Example from PROJECT_DESCRIPTION.md
            {
                "department": "Engineering & Technical",
                "function": "Software Development",
                "seniority": "Entry",
                "confidence": 0.90,
                "should_be_valid": True
            },
            {
                "department": "Sales",
                "function": "Sales",
                "seniority": "Head",
                "confidence": 0.95,
                "should_be_valid": True
            },
            {
                "department": "Sales",
                "function": "Sales",
                "seniority": "Entry",
                "confidence": 0.88,
                "should_be_valid": True
            },
            {
                "department": "Engineering & Technical",
                "function": "Software Development",
                "seniority": "Intern",
                "confidence": 0.92,
                "should_be_valid": True
            },
        ]
        
        for example in examples:
            result = self.validator_strict.validate(
                department=example["department"],
                function=example["function"],
                seniority=example["seniority"],
                confidence=example["confidence"]
            )
            
            self.assertEqual(
                result.is_valid,
                example["should_be_valid"],
                f"Example {example} validation failed: {result.issues}"
            )


class TestValidationResult(unittest.TestCase):
    """Test cases for ValidationResult class."""
    
    def test_add_error(self):
        """Test adding errors to validation result."""
        result = ValidationResult(is_valid=True)
        self.assertTrue(result.is_valid)
        
        result.add_error("field", "Error message")
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.issues), 1)
        self.assertEqual(result.issues[0].severity, ValidationSeverity.ERROR)
    
    def test_add_warning(self):
        """Test adding warnings to validation result."""
        result = ValidationResult(is_valid=True)
        result.add_warning("field", "Warning message")
        
        self.assertTrue(result.is_valid)  # Warnings don't invalidate
        self.assertEqual(len(result.issues), 1)
        self.assertEqual(result.issues[0].severity, ValidationSeverity.WARNING)
    
    def test_has_errors(self):
        """Test checking for errors."""
        result = ValidationResult(is_valid=True)
        self.assertFalse(result.has_errors())
        
        result.add_error("field", "Error")
        self.assertTrue(result.has_errors())
        
        result.add_warning("field2", "Warning")
        self.assertTrue(result.has_errors())  # Still has errors
    
    def test_has_warnings(self):
        """Test checking for warnings."""
        result = ValidationResult(is_valid=True)
        self.assertFalse(result.has_warnings())
        
        result.add_warning("field", "Warning")
        self.assertTrue(result.has_warnings())
        
        result.add_error("field2", "Error")
        self.assertTrue(result.has_warnings())  # Still has warnings


if __name__ == "__main__":
    unittest.main()
