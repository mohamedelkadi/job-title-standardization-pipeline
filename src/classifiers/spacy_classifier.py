#!/usr/bin/env python3
"""
spaCy-based Classifier for Job Title Standardization

Uses spaCy's NLP capabilities including Matcher, tokenization, and linguistic features
to classify job titles into department, function, and seniority.
"""

import spacy
from spacy.matcher import Matcher
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
import re


@dataclass
class ClassificationResult:
    """Result of a job title classification."""
    department: Optional[str]
    function: Optional[str]
    seniority: Optional[str]
    confidence: float
    method: str = "spacy"


class SpacyClassifier:
    """
    spaCy-based classifier for job titles.
    
    Uses spaCy's Matcher and linguistic features to classify job titles into:
    - Department (e.g., "Sales", "Engineering & Technical")
    - Function (e.g., "Software Development", "Sales")
    - Seniority (e.g., "Senior", "Manager", "Director")
    """
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize the spaCy classifier.
        
        Args:
            model_name: Name of the spaCy model to use
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            raise OSError(
                f"spaCy model '{model_name}' not found. "
                f"Please install it with: python -m spacy download {model_name}"
            )
        
        self.matcher = Matcher(self.nlp.vocab)
        self._build_seniority_patterns()
        self._build_department_function_patterns()
    
    def _build_seniority_patterns(self):
        """Build spaCy Matcher patterns for detecting seniority levels."""
        # Store patterns as (pattern_id, pattern, seniority_level, confidence)
        self.seniority_patterns = []
        
        # Owner/Founder patterns
        self.seniority_patterns.append((
            "OWNER",
            [{"LOWER": {"IN": ["owner", "proprietor"]}}],
            "Owner",
            0.95
        ))
        self.seniority_patterns.append((
            "FOUNDER",
            [{"LOWER": {"IN": ["founder", "co-founder", "cofounder"]}}],
            "Founder",
            0.95
        ))
        
        # C-suite patterns
        c_suite_terms = ["ceo", "cto", "cfo", "coo", "chro", "cmo", "cso"]
        c_suite_expanded = [
            "chief executive officer", "chief technology officer",
            "chief financial officer", "chief operating officer",
            "chief human resources officer", "chief marketing officer",
            "chief sales officer"
        ]
        self.seniority_patterns.append((
            "C_SUITE_ACRONYM",
            [{"LOWER": {"IN": c_suite_terms}}],
            "C-suite",
            0.95
        ))
        self.seniority_patterns.append((
            "C_SUITE_FULL",
            [{"LOWER": "chief"}, {"LOWER": {"IN": ["executive", "technology", "financial", "operating"]}}, {"LOWER": "officer"}],
            "C-suite",
            0.95
        ))
        self.seniority_patterns.append((
            "CHIEF_GENERIC",
            [{"LOWER": "chief"}, {"POS": {"IN": ["NOUN", "PROPN"]}}],
            "C-suite",
            0.90
        ))
        
        # Partner patterns
        self.seniority_patterns.append((
            "PARTNER",
            [{"LOWER": {"IN": ["partner", "managing", "general", "equity"]}}],
            "Partner",
            0.95
        ))
        self.seniority_patterns.append((
            "MANAGING_PARTNER",
            [{"LOWER": "managing"}, {"LOWER": "partner"}],
            "Partner",
            0.95
        ))
        
        # VP patterns
        vp_patterns = [
            [{"LOWER": {"IN": ["vp", "v.p.", "vice"]}}, {"LOWER": "president", "OP": "?"}],
            [{"LOWER": {"IN": ["svp", "senior"]}}, {"LOWER": "vice"}, {"LOWER": "president"}],
            [{"LOWER": "executive"}, {"LOWER": "vice"}, {"LOWER": "president"}]
        ]
        for i, pattern in enumerate(vp_patterns):
            self.seniority_patterns.append((
                f"VP_{i}",
                pattern,
                "VP",
                0.95
            ))
        
        # Head patterns
        self.seniority_patterns.append((
            "HEAD",
            [{"LOWER": "head"}, {"LOWER": "of", "OP": "?"}],
            "Head",
            0.90
        ))
        
        # Director patterns
        self.seniority_patterns.append((
            "DIRECTOR",
            [{"LOWER": "director"}],
            "Director",
            0.90
        ))
        self.seniority_patterns.append((
            "MANAGING_DIRECTOR",
            [{"LOWER": "managing"}, {"LOWER": "director"}],
            "Director",
            0.90
        ))
        self.seniority_patterns.append((
            "EXECUTIVE_DIRECTOR",
            [{"LOWER": "executive"}, {"LOWER": "director"}],
            "Director",
            0.90
        ))
        self.seniority_patterns.append((
            "SENIOR_DIRECTOR",
            [{"LOWER": "senior"}, {"LOWER": "director"}],
            "Director",
            0.90
        ))
        
        # Manager patterns
        self.seniority_patterns.append((
            "MANAGER",
            [{"LOWER": "manager"}],
            "Manager",
            0.85
        ))
        self.seniority_patterns.append((
            "MANAGING",
            [{"LOWER": "managing"}],
            "Manager",
            0.85
        ))
        self.seniority_patterns.append((
            "GENERAL_MANAGER",
            [{"LOWER": "general"}, {"LOWER": "manager"}],
            "Manager",
            0.85
        ))
        self.seniority_patterns.append((
            "PRODUCT_MANAGER",
            [{"LOWER": "product"}, {"LOWER": "manager"}],
            "Manager",
            0.85
        ))
        self.seniority_patterns.append((
            "PROJECT_MANAGER",
            [{"LOWER": "project"}, {"LOWER": "manager"}],
            "Manager",
            0.85
        ))
        self.seniority_patterns.append((
            "PROGRAM_MANAGER",
            [{"LOWER": "program"}, {"LOWER": "manager"}],
            "Manager",
            0.85
        ))
        self.seniority_patterns.append((
            "ACCOUNT_MANAGER",
            [{"LOWER": "account"}, {"LOWER": "manager"}],
            "Manager",
            0.85
        ))
        self.seniority_patterns.append((
            "SALES_MANAGER",
            [{"LOWER": "sales"}, {"LOWER": "manager"}],
            "Manager",
            0.85
        ))
        self.seniority_patterns.append((
            "ENGINEERING_MANAGER",
            [{"LOWER": "engineering"}, {"LOWER": "manager"}],
            "Manager",
            0.85
        ))
        
        # Senior patterns
        self.seniority_patterns.append((
            "SENIOR",
            [{"LOWER": {"IN": ["senior", "sr.", "sr", "lead", "principal", "staff"]}}],
            "Senior",
            0.80
        ))
        
        # Intern patterns
        self.seniority_patterns.append((
            "INTERN",
            [{"LOWER": {"IN": ["intern", "internship", "trainee"]}}],
            "Intern",
            0.95
        ))
        
        # Entry patterns
        self.seniority_patterns.append((
            "ENTRY",
            [{"LOWER": {"IN": ["associate", "junior", "entry", "assistant", "coordinator", "specialist", "analyst", "representative", "executive"]}}],
            "Entry",
            0.70
        ))
        
        # Add patterns to matcher
        for pattern_id, pattern, _, _ in self.seniority_patterns:
            self.matcher.add(pattern_id, [pattern])
    
    def _build_department_function_patterns(self):
        """Build spaCy Matcher patterns for detecting departments and functions."""
        self.dept_function_patterns = []
        
        # Sales patterns
        sales_patterns = [
            ([{"LOWER": "sales"}, {"LOWER": {"IN": ["executive", "manager", "rep", "representative", "person", "specialist", "director"]}}], 0.95),
            ([{"LOWER": "sales"}], 0.90),
            ([{"LOWER": "account"}, {"LOWER": {"IN": ["executive", "manager"]}}], 0.90),
        ]
        for pattern, conf in sales_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Sales',
                'function': 'Sales',
                'confidence': conf
            })
        
        # Customer Success
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": "customer"}, {"LOWER": "success"}],
            'department': 'Sales',
            'function': 'Customer Success',
            'confidence': 0.90
        })
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": "cs"}],
            'department': 'Sales',
            'function': 'Customer Success',
            'confidence': 0.85
        })
        
        # Sales Engineering
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": "sales"}, {"LOWER": {"IN": ["engineer", "engineering"]}}],
            'department': 'Sales',
            'function': 'Sales Engineering',
            'confidence': 0.90
        })
        
        # Business Development
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": "business"}, {"LOWER": "development"}],
            'department': 'Sales',
            'function': 'Business Development',
            'confidence': 0.90
        })
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": "bd"}],
            'department': 'Sales',
            'function': 'Business Development',
            'confidence': 0.85
        })
        
        # C-Suite
        c_suite_patterns = [
            ([{"LOWER": {"IN": ["ceo", "cto", "cfo", "coo", "chro", "cmo", "cso"]}}], 0.95),
            ([{"LOWER": "chief"}, {"POS": {"IN": ["NOUN", "PROPN"]}}, {"LOWER": "officer", "OP": "?"}], 0.90),
            ([{"LOWER": "executive"}, {"LOWER": {"IN": ["director", "vp", "vice", "manager"]}}], 0.85),
        ]
        for pattern, conf in c_suite_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'C-Suite',
                'function': 'Executive',
                'confidence': conf
            })
        
        # Founder
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": {"IN": ["founder", "co-founder", "cofounder"]}}],
            'department': 'C-Suite',
            'function': 'Founder',
            'confidence': 0.95
        })
        
        # Engineering & Technical - Software Development
        eng_patterns = [
            ([{"LOWER": {"IN": ["software", "backend", "frontend", "full-stack", "fullstack"]}}, {"LOWER": {"IN": ["engineer", "developer"]}}], 0.90),
            ([{"LOWER": {"IN": ["devops", "sre"]}}, {"LOWER": "engineer", "OP": "?"}], 0.90),
            ([{"LOWER": {"IN": ["engineer", "developer", "programmer", "coder", "swe"]}}], 0.90),
            ([{"LOWER": {"IN": ["backend", "frontend", "full-stack", "devops", "sre"]}}], 0.85),
        ]
        for pattern, conf in eng_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Engineering & Technical',
                'function': 'Software Development',
                'confidence': conf
            })
        
        # Data Science
        data_patterns = [
            ([{"LOWER": "data"}, {"LOWER": {"IN": ["scientist", "engineer", "analyst"]}}], 0.90),
            ([{"LOWER": {"IN": ["ml", "machine"]}}, {"LOWER": {"IN": ["learning", "engineer"]}}], 0.90),
            ([{"LOWER": {"IN": ["ai", "artificial"]}}, {"LOWER": "intelligence", "OP": "?"}], 0.90),
        ]
        for pattern, conf in data_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Engineering & Technical',
                'function': 'Data Science',
                'confidence': conf
            })
        
        # Product Management
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": "product"}, {"LOWER": {"IN": ["manager", "pm", "owner", "lead"]}}],
            'department': 'Engineering & Technical',
            'function': 'Product Management',
            'confidence': 0.90
        })
        
        # Project Management
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": {"IN": ["project", "program"]}}, {"LOWER": {"IN": ["manager", "pm", "pmo"]}}],
            'department': 'Engineering & Technical',
            'function': 'Project Management',
            'confidence': 0.90
        })
        
        # QA/Testing
        qa_patterns = [
            ([{"LOWER": {"IN": ["qa", "quality"]}}, {"LOWER": {"IN": ["engineer", "assurance"]}}], 0.95),
            ([{"LOWER": {"IN": ["qa", "quality", "tester", "testing"]}}], 0.90),
        ]
        for pattern, conf in qa_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Engineering & Technical',
                'function': 'Test / Quality Assurance',
                'confidence': conf
            })
        
        # UI/UX
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": {"IN": ["ui", "ux", "user"]}}, {"LOWER": {"IN": ["experience", "interface", "designer", "engineer"], "OP": "?"}}],
            'department': 'Engineering & Technical',
            'function': 'UI / UX',
            'confidence': 0.90
        })
        
        # DevOps
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": {"IN": ["devops", "infrastructure", "platform", "cloud"]}}, {"LOWER": "engineer", "OP": "?"}],
            'department': 'Engineering & Technical',
            'function': 'DevOps',
            'confidence': 0.90
        })
        
        # Marketing
        marketing_patterns = [
            ([{"LOWER": "marketing"}], 0.90),
            ([{"LOWER": "public"}, {"LOWER": "relations"}], 0.90),
            ([{"LOWER": "content"}, {"LOWER": {"IN": ["marketing", "manager", "creator", "strategist"]}}], 0.90),
            ([{"LOWER": {"IN": ["digital", "seo", "ppc", "social"]}}, {"LOWER": "marketing", "OP": "?"}], 0.90),
        ]
        for pattern, conf in marketing_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Marketing',
                'function': 'Marketing' if conf == 0.90 else 'Marketing',
                'confidence': conf
            })
        
        # Finance
        finance_patterns = [
            ([{"LOWER": {"IN": ["finance", "financial"]}}], 0.90),
            ([{"LOWER": {"IN": ["accountant", "accounting", "bookkeeper", "cpa", "controller"]}}], 0.90),
            ([{"LOWER": {"IN": ["fp&a", "financial"]}}, {"LOWER": {"IN": ["planning", "analysis"]}}], 0.90),
        ]
        for pattern, conf in finance_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Finance',
                'function': 'Finance',
                'confidence': conf
            })
        
        # Human Resources
        hr_patterns = [
            ([{"LOWER": {"IN": ["hr", "human"]}}, {"LOWER": "resources", "OP": "?"}], 0.90),
            ([{"LOWER": {"IN": ["people", "talent"]}}, {"LOWER": {"IN": ["ops", "operations", "acquisition"]}}], 0.90),
            ([{"LOWER": {"IN": ["recruiter", "recruiting"]}}], 0.90),
        ]
        for pattern, conf in hr_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Human Resources',
                'function': 'Human Resources',
                'confidence': conf
            })
        
        # Operations
        ops_patterns = [
            ([{"LOWER": {"IN": ["operations", "ops"]}}], 0.90),
            ([{"LOWER": {"IN": ["customer"]}}, {"LOWER": {"IN": ["service", "support", "care"]}}], 0.90),
            ([{"LOWER": "compliance"}], 0.90),
            ([{"LOWER": {"IN": ["safety", "hse", "health"]}}, {"LOWER": "safety", "OP": "?"}], 0.90),
        ]
        for pattern, conf in ops_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Operations',
                'function': 'Operations',
                'confidence': conf
            })
        
        # Legal
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": {"IN": ["lawyer", "attorney", "legal", "counsel", "paralegal"]}}],
            'department': 'Legal',
            'function': 'Legal',
            'confidence': 0.90
        })
        
        # Medical & Health
        medical_patterns = [
            ([{"LOWER": {"IN": ["doctor", "physician", "md", "nurse", "nursing", "clinician", "medical", "healthcare"]}}], 0.90),
        ]
        for pattern, conf in medical_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Medical & Health',
                'function': 'Medicine',
                'confidence': conf
            })
        
        # IT
        it_patterns = [
            ([{"LOWER": {"IN": ["it", "information"]}}, {"LOWER": "technology", "OP": "?"}], 0.90),
            ([{"LOWER": {"IN": ["security", "cybersecurity", "infosec"]}}], 0.90),
        ]
        for pattern, conf in it_patterns:
            self.dept_function_patterns.append({
                'pattern': pattern,
                'department': 'Information Technology',
                'function': 'Information Technology',
                'confidence': conf
            })
        
        # Design
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": {"IN": ["designer", "design", "photographer"]}}],
            'department': 'Design',
            'function': 'Product or UI/UX Design',
            'confidence': 0.90
        })
        
        # Consulting
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": {"IN": ["consultant", "consulting"]}}],
            'department': 'Consulting',
            'function': 'Management Consulting',
            'confidence': 0.85
        })
        
        # Education
        self.dept_function_patterns.append({
            'pattern': [{"LOWER": {"IN": ["teacher", "educator", "instructor", "professor", "lecturer"]}}],
            'department': 'Education',
            'function': 'Teacher',
            'confidence': 0.90
        })
    
    def normalize_title(self, title: str) -> str:
        """
        Normalize a job title for processing.
        
        Args:
            title: Raw job title string
            
        Returns:
            Normalized title string
        """
        if not title:
            return ""
        
        # Basic normalization
        normalized = title.lower().strip()
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = normalized.replace(',', ' ')
        normalized = normalized.replace('.', ' ')
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized.strip()
    
    def classify_seniority(self, doc) -> Tuple[Optional[str], float]:
        """
        Classify seniority level using spaCy Matcher.
        
        Args:
            doc: spaCy Doc object
            
        Returns:
            Tuple of (seniority_level, confidence)
        """
        if not doc or len(doc) == 0:
            return None, 0.0
        
        matches = self.matcher(doc)
        
        if not matches:
            return 'Entry', 0.50
        
        # Create a mapping from pattern_id to (seniority, confidence)
        pattern_map = {}
        for pid, _, seniority, confidence in self.seniority_patterns:
            pattern_map[pid] = (seniority, confidence)
        
        # Find the best match (highest confidence)
        best_seniority = None
        best_confidence = 0.0
        
        for match_id, start, end in matches:
            # Get the pattern ID string
            pattern_id = self.nlp.vocab.strings[match_id]
            
            # Look up the seniority and confidence for this pattern
            if pattern_id in pattern_map:
                seniority, confidence = pattern_map[pattern_id]
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_seniority = seniority
        
        return best_seniority or 'Entry', best_confidence or 0.50
    
    def classify_department_function(self, doc) -> Tuple[Optional[str], Optional[str], float]:
        """
        Classify department and function using pattern matching.
        
        Args:
            doc: spaCy Doc object
            
        Returns:
            Tuple of (department, function, confidence)
        """
        if not doc or len(doc) == 0:
            return None, None, 0.0
        
        best_match = None
        best_confidence = 0.0
        
        # Create a temporary matcher for department/function patterns
        dept_func_matcher = Matcher(self.nlp.vocab)
        
        for idx, dept_func in enumerate(self.dept_function_patterns):
            pattern_id = f"DEPT_FUNC_{idx}"
            try:
                dept_func_matcher.add(pattern_id, [dept_func['pattern']])
            except Exception as e:
                # Skip invalid patterns
                continue
        
        matches = dept_func_matcher(doc)
        
        for match_id, start, end in matches:
            try:
                pattern_id_str = self.nlp.vocab.strings[match_id]
                pattern_idx = int(pattern_id_str.split('_')[-1])
                
                if 0 <= pattern_idx < len(self.dept_function_patterns):
                    dept_func = self.dept_function_patterns[pattern_idx]
                    
                    if dept_func['confidence'] > best_confidence:
                        best_match = (dept_func['department'], dept_func['function'])
                        best_confidence = dept_func['confidence']
            except (ValueError, IndexError):
                continue
        
        if best_match:
            return best_match[0], best_match[1], best_confidence
        
        return None, None, 0.0
    
    def classify(self, title: str) -> ClassificationResult:
        """
        Classify a job title into department, function, and seniority.
        
        Args:
            title: Raw job title string
            
        Returns:
            ClassificationResult with department, function, seniority, and confidence
        """
        if not title or not title.strip():
            return ClassificationResult(
                department=None,
                function=None,
                seniority=None,
                confidence=0.0,
                method="spacy"
            )
        
        # Process with spaCy
        doc = self.nlp(title)
        
        # Classify seniority
        seniority, seniority_conf = self.classify_seniority(doc)
        
        # Classify department and function
        department, function, dept_func_conf = self.classify_department_function(doc)
        
        # Calculate overall confidence
        if seniority and department:
            overall_confidence = (seniority_conf + dept_func_conf) / 2.0
        elif seniority:
            overall_confidence = seniority_conf * 0.7
        elif department:
            overall_confidence = dept_func_conf * 0.7
        else:
            overall_confidence = 0.0
        
        return ClassificationResult(
            department=department,
            function=function,
            seniority=seniority,
            confidence=overall_confidence,
            method="spacy"
        )


def main():
    """Test the spaCy classifier on sample titles."""
    try:
        classifier = SpacyClassifier()
    except OSError as e:
        print(f"Error: {e}")
        return
    
    # Sample titles from the database and common patterns
    sample_titles = [
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
    
    print("=" * 100)
    print("SPACY CLASSIFIER - TEST RESULTS")
    print("=" * 100)
    print(f"\nTesting {len(sample_titles)} job titles...\n")
    
    results = []
    for title in sample_titles:
        result = classifier.classify(title)
        results.append({
            'title': title,
            'department': result.department,
            'function': result.function,
            'seniority': result.seniority,
            'confidence': result.confidence
        })
    
    # Print results in a table format
    print(f"{'Title':<50} {'Department':<25} {'Function':<30} {'Seniority':<15} {'Confidence':<10}")
    print("-" * 130)
    
    for r in results:
        dept = r['department'] or 'N/A'
        func = r['function'] or 'N/A'
        seniority = r['seniority'] or 'N/A'
        conf = f"{r['confidence']:.2f}"
        
        print(f"{r['title']:<50} {dept:<25} {func:<30} {seniority:<15} {conf:<10}")
    
    # Statistics
    print("\n" + "=" * 100)
    print("STATISTICS")
    print("=" * 100)
    
    total = len(results)
    classified = sum(1 for r in results if r['department'] is not None)
    avg_confidence = sum(r['confidence'] for r in results) / total if total > 0 else 0
    
    print(f"Total titles: {total}")
    print(f"Successfully classified: {classified} ({classified/total*100:.1f}%)")
    print(f"Average confidence: {avg_confidence:.2f}")
    
    # Distribution by department
    dept_dist = {}
    for r in results:
        if r['department']:
            dept_dist[r['department']] = dept_dist.get(r['department'], 0) + 1
    
    print(f"\nDistribution by Department:")
    for dept, count in sorted(dept_dist.items(), key=lambda x: -x[1]):
        print(f"  {dept}: {count}")
    
    # Distribution by seniority
    seniority_dist = {}
    for r in results:
        if r['seniority']:
            seniority_dist[r['seniority']] = seniority_dist.get(r['seniority'], 0) + 1
    
    print(f"\nDistribution by Seniority:")
    for seniority, count in sorted(seniority_dist.items(), key=lambda x: -x[1]):
        print(f"  {seniority}: {count}")
    
    print("\n" + "=" * 100)


if __name__ == '__main__':
    main()
