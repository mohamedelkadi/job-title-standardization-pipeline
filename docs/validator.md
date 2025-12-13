# Validator Component

## Overview

The `Validator` component ensures that all standardized job titles comply with the defined taxonomy. It performs final validation checks to guarantee that classification outputs meet quality standards and taxonomy requirements before storage.

## Features

- ✅ **Taxonomy Validation**: Validates department, function, and seniority against the defined taxonomy
- ✅ **Relationship Validation**: Ensures functions belong to the correct department
- ✅ **Confidence Validation**: Validates confidence scores are within valid range (0.0-1.0)
- ✅ **Strict/Lenient Modes**: Supports both strict validation (all fields required) and lenient mode (partial classifications allowed)
- ✅ **Error Reporting**: Provides detailed error and warning messages
- ✅ **Integration Ready**: Works seamlessly with `ClassificationResult` objects from classifiers

## Usage

### Basic Usage

```python
from validator import Validator
from rule_classifier import RuleClassifier

# Initialize components
classifier = RuleClassifier()
validator = Validator(strict_mode=True)

# Classify a job title
classification = classifier.classify("Senior Software Engineer")

# Validate the classification
result = validator.validate_classification_result(classification)

if result.is_valid:
    print("✅ Classification is valid - ready to store")
else:
    print("❌ Classification has errors:")
    for issue in result.issues:
        if issue.severity.value == "error":
            print(f"  - {issue.field}: {issue.message}")
```

### Direct Validation

```python
from validator import Validator

validator = Validator(strict_mode=True)

result = validator.validate(
    department="Engineering & Technical",
    function="Software Development",
    seniority="Senior",
    confidence=0.95,
    method="rule"
)

if result.is_valid:
    print("Valid!")
else:
    for issue in result.issues:
        print(f"{issue.severity.value}: {issue.field} - {issue.message}")
```

### Pipeline Integration

```python
# In your pipeline workflow:
for title in job_titles:
    # Step 1: Classify
    classification = classifier.classify(title)
    
    # Step 2: Validate
    validation = validator.validate_classification_result(classification)
    
    # Step 3: Store or reject
    if validation.is_valid:
        store_in_database(classification)
    else:
        flag_for_review(title, classification, validation)
```

## Validation Rules

### Department Validation
- Must be one of the 13 valid departments:
  - C-Suite, Engineering & Technical, Design, Education, Finance,
  - Human Resources, Information Technology, Legal, Marketing,
  - Medical & Health, Operations, Sales, Consulting

### Function Validation
- Must exist in the taxonomy
- Must belong to the specified department
- If department is not specified, generates a warning with expected department

### Seniority Validation
- Must be one of the 11 valid seniority levels:
  - Owner, Founder, C-suite, Partner, VP, Head, Director,
  - Manager, Senior, Entry, Intern

### Confidence Validation
- Must be between 0.0 and 1.0
- Values below 0.5 generate a warning (configurable via `MIN_CONFIDENCE_THRESHOLD`)

### Strict Mode
- When `strict_mode=True`: All fields (department, function, seniority) are required
- When `strict_mode=False`: Partial classifications are allowed (warnings may be generated)

## Validation Result Structure

```python
@dataclass
class ValidationResult:
    is_valid: bool  # True if no errors (warnings don't invalidate)
    issues: List[ValidationIssue]  # List of errors and warnings

@dataclass
class ValidationIssue:
    severity: ValidationSeverity  # ERROR or WARNING
    field: str  # Field name (department, function, seniority, confidence, method)
    message: str  # Human-readable error/warning message
```

## Examples

### Valid Classification
```python
result = validator.validate(
    department="Engineering & Technical",
    function="Software Development",
    seniority="Senior",
    confidence=0.95
)
# result.is_valid = True
# result.issues = []
```

### Invalid Department
```python
result = validator.validate(
    department="Invalid Department",
    function="Software Development",
    seniority="Senior",
    confidence=0.95
)
# result.is_valid = False
# result.issues = [
#   ValidationIssue(ERROR, "department", "Invalid department: 'Invalid Department'...")
# ]
```

### Function Wrong Department
```python
result = validator.validate(
    department="Sales",
    function="Software Development",  # Belongs to Engineering & Technical
    seniority="Senior",
    confidence=0.95
)
# result.is_valid = False
# Error: Function 'Software Development' belongs to department 'Engineering & Technical',
#        but classification specifies department 'Sales'
```

### Low Confidence Warning
```python
result = validator.validate(
    department="Engineering & Technical",
    function="Software Development",
    seniority="Senior",
    confidence=0.3  # Below threshold
)
# result.is_valid = True  # Still valid
# result.has_warnings() = True
# Warning: Low confidence score: 0.30. Consider re-classifying.
```

## Testing

### Run Unit Tests
```bash
python3 -m unittest test_validator -v
```

### Run Integration Tests
```bash
python3 test_validator_integration.py
```

### Run Example
```bash
python3 validator.py
```

## Test Coverage

The validator includes comprehensive test coverage:
- ✅ All valid taxonomy values pass validation
- ✅ Invalid values are caught
- ✅ Department-function relationships are validated
- ✅ Confidence score validation
- ✅ Strict vs lenient mode behavior
- ✅ Error and warning reporting
- ✅ Integration with classifier outputs
- ✅ Real-world examples from PROJECT_DESCRIPTION.md

## Files

- `validator.py` - Main Validator class implementation
- `test_validator.py` - Unit tests (23 test cases)
- `test_validator_integration.py` - Integration tests with classifiers

## Architecture Position

The Validator sits in the pipeline after classification:

```
Change Detector → Queue → Normalizer → Cache → Rules → LLM → Validator → Database
                                                                          ↓
                                                                    Query API
```

It ensures that only valid, taxonomy-compliant classifications are stored in the database.
