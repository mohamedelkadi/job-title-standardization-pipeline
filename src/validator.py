#!/usr/bin/env python3
"""
Validator for Job Title Standardization

Ensures that all standardized job titles comply with the defined taxonomy.
This component performs final validation checks to guarantee that the output
meets quality standards and taxonomy requirements before storage.
"""

from typing import Optional, List, Dict, Set
from dataclasses import dataclass, field
from enum import Enum


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"
    WARNING = "warning"


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    severity: ValidationSeverity
    field: str
    message: str


@dataclass
class ValidationResult:
    """Result of validation checks."""
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    
    def add_error(self, field: str, message: str):
        """Add an error to the validation result."""
        self.issues.append(ValidationIssue(ValidationSeverity.ERROR, field, message))
        self.is_valid = False
    
    def add_warning(self, field: str, message: str):
        """Add a warning to the validation result."""
        self.issues.append(ValidationIssue(ValidationSeverity.WARNING, field, message))
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return any(issue.severity == ValidationSeverity.ERROR for issue in self.issues)
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return any(issue.severity == ValidationSeverity.WARNING for issue in self.issues)


class Validator:
    """
    Validator for job title standardization results.
    
    Ensures that classification results comply with the defined taxonomy:
    - Valid department names
    - Valid function names
    - Valid seniority levels
    - Function belongs to correct department
    - Confidence scores are valid
    - Required fields are present
    """
    
    # Valid seniority levels
    VALID_SENIORITY_LEVELS = {
        "Owner", "Founder", "C-suite", "Partner", "VP", "Head",
        "Director", "Manager", "Senior", "Entry", "Intern"
    }
    
    # Valid departments
    VALID_DEPARTMENTS = {
        "C-Suite", "Engineering & Technical", "Design", "Education",
        "Finance", "Human Resources", "Information Technology", "Legal",
        "Marketing", "Medical & Health", "Operations", "Sales", "Consulting"
    }
    
    # Department -> Functions mapping
    # This maps each department to its valid functions
    DEPARTMENT_FUNCTIONS: Dict[str, Set[str]] = {
        "C-Suite": {
            "Executive", "Finance Executive", "Founder", "Human Resources Executive",
            "Information Technology Executive", "Legal Executive", "Marketing Executive",
            "Medical & Health Executive", "Operations Executive", "Sales Leader"
        },
        "Engineering & Technical": {
            "Artificial Intelligence / Machine Learning", "Bioengineering", "Biometrics",
            "Business Intelligence", "Chemical Engineering", "Cloud / Mobility", "Data Science",
            "DevOps", "Digital Transformation", "Emerging Technology / Innovation",
            "Engineering & Technical", "Industrial Engineering", "Mechanic",
            "Mobile Development", "Product Development", "Product Management",
            "Project Management", "Research & Development", "Scrum Master / Agile Coach",
            "Software Development", "Support / Technical Services", "Technician",
            "Technology Operations", "Test / Quality Assurance", "UI / UX", "Web Development"
        },
        "Design": {
            "All Design", "Product or UI/UX Design", "Graphic / Visual / Brand Design"
        },
        "Education": {
            "Teacher", "Principal", "Superintendent", "Professor"
        },
        "Finance": {
            "Accounting", "Finance", "Financial Planning & Analysis", "Financial Reporting",
            "Financial Strategy", "Financial Systems", "Internal Audit & Control",
            "Investor Relations", "Mergers & Acquisitions", "Real Estate Finance",
            "Financial Risk", "Shared Services", "Sourcing / Procurement", "Tax", "Treasury"
        },
        "Human Resources": {
            "Compensation & Benefits", "Culture, Diversity & Inclusion",
            "Employee & Labor Relations", "Health & Safety",
            "Human Resource Information System", "Human Resources", "HR Business Partner",
            "Learning & Development", "Organizational Development",
            "Recruiting & Talent Acquisition", "Talent Management", "Workforce Management",
            "People Operations"
        },
        "Information Technology": {
            "Application Development", "Business Service Management / ITSM",
            "Collaboration & Web App", "Data Center", "Data Warehouse",
            "Database Administration", "eCommerce Development", "Enterprise Architecture",
            "Help Desk / Desktop Services", "HR / Financial / ERP Systems",
            "Information Security", "Information Technology", "Infrastructure",
            "IT Asset Management", "IT Audit / IT Compliance", "IT Operations",
            "IT Procurement", "IT Strategy", "IT Training", "Networking",
            "Project & Program Management", "Quality Assurance", "Retail / Store Systems",
            "Servers", "Storage & Disaster Recovery", "Telecommunications", "Virtualization"
        },
        "Legal": {
            "Acquisitions", "Compliance", "Contracts", "Corporate Secretary", "eDiscovery",
            "Ethics", "Governance", "Governmental Affairs & Regulatory Law",
            "Intellectual Property & Patent", "Labor & Employment", "Lawyer / Attorney",
            "Legal", "Legal Counsel", "Legal Operations", "Litigation", "Privacy"
        },
        "Marketing": {
            "Advertising", "Brand Management", "Content Marketing", "Customer Experience",
            "Customer Marketing", "Demand Generation", "Digital Marketing",
            "eCommerce Marketing", "Event Marketing", "Field Marketing", "Lead Generation",
            "Marketing", "Marketing Analytics / Insights", "Marketing Communications",
            "Marketing Operations", "Product Marketing", "Public Relations",
            "Search Engine Optimization / Pay Per Click", "Social Media Marketing",
            "Strategic Communications", "Technical Marketing"
        },
        "Medical & Health": {
            "Anesthesiology", "Chiropractics", "Clinical Systems", "Dentistry", "Dermatology",
            "Doctors / Physicians", "Epidemiology", "First Responder", "Infectious Disease",
            "Medical Administration", "Medical Education & Training", "Medical Research",
            "Medicine", "Neurology", "Nursing", "Nutrition & Dietetics",
            "Obstetrics / Gynecology", "Oncology", "Ophthalmology", "Optometry",
            "Orthopedics", "Pathology", "Pediatrics", "Pharmacy", "Physical Therapy",
            "Psychiatry", "Psychology", "Public Health", "Radiology", "Social Work"
        },
        "Operations": {
            "Call Center", "Construction", "Corporate Strategy", "Customer Service / Support",
            "Enterprise Resource Planning", "Facilities Management", "Leasing", "Logistics",
            "Office Operations", "Operations", "Physical Security", "Project Development",
            "Quality Management", "Real Estate", "Safety", "Store Operations", "Supply Chain"
        },
        "Sales": {
            "Account Management", "Business Development", "Channel Sales",
            "Customer Retention & Development", "Customer Success", "Field / Outside Sales",
            "Inside Sales", "Partnerships", "Revenue Operations", "Sales", "Sales Enablement",
            "Sales Engineering", "Sales Operations", "Sales Training"
        },
        "Consulting": {
            "Business Strategy Consulting", "Change Management Consulting",
            "Customer Experience Consulting", "Data Analytics Consulting",
            "Digital Transformation Consulting", "Environmental Consulting",
            "Financial Advisory Consulting", "Healthcare Consulting",
            "Human Resources Consulting", "Information Technology Consulting",
            "Management Consulting", "Marketing Consulting",
            "Mergers & Acquisitions Consulting", "Organizational Development Consulting",
            "Process Improvement Consulting", "Risk Management Consulting",
            "Sales Strategy Consulting", "Supply Chain Consulting", "Sustainability Consulting",
            "Tax Consulting", "Technology Implementation Consulting",
            "Training & Development Consulting"
        }
    }
    
    # Minimum confidence threshold for warnings
    MIN_CONFIDENCE_THRESHOLD = 0.5
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize the validator.
        
        Args:
            strict_mode: If True, requires all fields (department, function, seniority).
                         If False, allows partial classifications.
        """
        self.strict_mode = strict_mode
    
    def validate(self, department: Optional[str], function: Optional[str],
                 seniority: Optional[str], confidence: float = 0.0,
                 method: str = "unknown") -> ValidationResult:
        """
        Validate a classification result.
        
        Args:
            department: Department name (can be None if not classified)
            function: Function name (can be None if not classified)
            seniority: Seniority level (can be None if not classified)
            confidence: Confidence score (0.0 to 1.0)
            method: Classification method used
            
        Returns:
            ValidationResult with validation status and any issues found
        """
        result = ValidationResult(is_valid=True)
        
        # Validate required fields in strict mode
        if self.strict_mode:
            if not department:
                result.add_error("department", "Department is required in strict mode")
            if not function:
                result.add_error("function", "Function is required in strict mode")
            if not seniority:
                result.add_error("seniority", "Seniority is required in strict mode")
        
        # Validate department
        if department:
            if department not in self.VALID_DEPARTMENTS:
                result.add_error(
                    "department",
                    f"Invalid department: '{department}'. Must be one of: {sorted(self.VALID_DEPARTMENTS)}"
                )
        
        # Validate function
        if function:
            # Check if function exists in any department
            function_found = False
            function_department = None
            
            for dept, functions in self.DEPARTMENT_FUNCTIONS.items():
                if function in functions:
                    function_found = True
                    function_department = dept
                    break
            
            if not function_found:
                result.add_error(
                    "function",
                    f"Invalid function: '{function}'. Function not found in taxonomy."
                )
            elif department and function_department != department:
                # Function doesn't belong to the specified department
                result.add_error(
                    "function",
                    f"Function '{function}' belongs to department '{function_department}', "
                    f"but classification specifies department '{department}'"
                )
            elif not department and function_found:
                # Function is valid but no department specified - this is a warning
                result.add_warning(
                    "function",
                    f"Function '{function}' is valid but no department specified. "
                    f"Expected department: '{function_department}'"
                )
        
        # Validate seniority
        if seniority:
            if seniority not in self.VALID_SENIORITY_LEVELS:
                result.add_error(
                    "seniority",
                    f"Invalid seniority: '{seniority}'. Must be one of: {sorted(self.VALID_SENIORITY_LEVELS)}"
                )
        
        # Validate confidence score
        if confidence < 0.0 or confidence > 1.0:
            result.add_error(
                "confidence",
                f"Confidence score must be between 0.0 and 1.0, got {confidence}"
            )
        elif confidence < self.MIN_CONFIDENCE_THRESHOLD:
            result.add_warning(
                "confidence",
                f"Low confidence score: {confidence:.2f}. Consider re-classifying."
            )
        
        # Validate method
        valid_methods = {"rule", "llm_gpt35", "llm_gpt4", "spacy", "llama", "unknown"}
        if method not in valid_methods:
            result.add_warning(
                "method",
                f"Unknown classification method: '{method}'. Expected one of: {valid_methods}"
            )
        
        # Cross-field validation warnings
        if department and function:
            # Check if function belongs to department (already checked above, but add helpful warning)
            if function in self.DEPARTMENT_FUNCTIONS.get(department, set()):
                # Valid combination
                pass
            elif department in self.DEPARTMENT_FUNCTIONS:
                # Department exists but function doesn't belong to it
                # This was already caught as an error above, so skip
                pass
        
        return result
    
    def validate_classification_result(self, classification_result) -> ValidationResult:
        """
        Validate a ClassificationResult object.
        
        Args:
            classification_result: ClassificationResult instance
            
        Returns:
            ValidationResult with validation status and any issues found
        """
        return self.validate(
            department=classification_result.department,
            function=classification_result.function,
            seniority=classification_result.seniority,
            confidence=classification_result.confidence,
            method=getattr(classification_result, 'method', 'unknown')
        )


def main():
    """Test the validator with example classifications."""
    from src.classifiers.rule_classifier import ClassificationResult
    
    validator = Validator(strict_mode=True)
    
    # Test cases
    test_cases = [
        # Valid classification
        ClassificationResult(
            department="Engineering & Technical",
            function="Software Development",
            seniority="Senior",
            confidence=0.95,
            method="rule"
        ),
        # Invalid department
        ClassificationResult(
            department="Invalid Department",
            function="Software Development",
            seniority="Senior",
            confidence=0.95,
            method="rule"
        ),
        # Invalid function
        ClassificationResult(
            department="Engineering & Technical",
            function="Invalid Function",
            seniority="Senior",
            confidence=0.95,
            method="rule"
        ),
        # Function doesn't belong to department
        ClassificationResult(
            department="Sales",
            function="Software Development",  # This belongs to Engineering & Technical
            seniority="Senior",
            confidence=0.95,
            method="rule"
        ),
        # Invalid seniority
        ClassificationResult(
            department="Engineering & Technical",
            function="Software Development",
            seniority="Invalid Seniority",
            confidence=0.95,
            method="rule"
        ),
        # Low confidence
        ClassificationResult(
            department="Engineering & Technical",
            function="Software Development",
            seniority="Senior",
            confidence=0.3,
            method="rule"
        ),
        # Missing fields (should fail in strict mode)
        ClassificationResult(
            department="Engineering & Technical",
            function=None,
            seniority="Senior",
            confidence=0.95,
            method="rule"
        ),
    ]
    
    print("Validator Test Results\n" + "=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"  Department: {test_case.department}")
        print(f"  Function: {test_case.function}")
        print(f"  Seniority: {test_case.seniority}")
        print(f"  Confidence: {test_case.confidence}")
        
        result = validator.validate_classification_result(test_case)
        
        print(f"  Valid: {result.is_valid}")
        if result.issues:
            print(f"  Issues:")
            for issue in result.issues:
                severity_icon = "❌" if issue.severity == ValidationSeverity.ERROR else "⚠️"
                print(f"    {severity_icon} [{issue.severity.value.upper()}] {issue.field}: {issue.message}")
        else:
            print(f"  ✅ No issues found")


if __name__ == "__main__":
    main()
