#!/usr/bin/env python3
"""
Rule Classifier for Job Title Standardization

Performs fast pattern matching on job titles using predefined rules.
This component handles straightforward title classifications efficiently,
providing quick results for titles that match known patterns.
"""

import re
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class ClassificationResult:
    """Result of a job title classification."""
    department: Optional[str]
    function: Optional[str]
    seniority: Optional[str]
    confidence: float
    method: str = "rule"


class RuleClassifier:
    """
    Fast pattern-matching classifier for job titles.
    
    Uses predefined rules and patterns to classify job titles into:
    - Department (e.g., "Sales", "Engineering & Technical")
    - Function (e.g., "Software Development", "Sales")
    - Seniority (e.g., "Senior", "Manager", "Director")
    """
    
    def __init__(self):
        """Initialize the rule classifier with predefined patterns."""
        self._build_seniority_patterns()
        self._build_department_function_patterns()
    
    def _build_seniority_patterns(self):
        """Build patterns for detecting seniority levels."""
        # Order matters - check more specific patterns first
        self.seniority_patterns = [
            # Owner/Founder patterns
            (r'\b(owner|proprietor)\b', 'Owner', 0.95),
            (r'\b(founder|co-founder|cofounder)\b', 'Founder', 0.95),
            
            # C-suite patterns
            (r'\b(ceo|chief executive officer|cto|chief technology officer|cfo|chief financial officer|coo|chief operating officer|chro|chief human resources officer|cmo|chief marketing officer|cso|chief sales officer)\b', 'C-suite', 0.95),
            (r'\b(chief\s+\w+\s+officer)\b', 'C-suite', 0.95),
            (r'\b(chief\s+\w+)\b', 'C-suite', 0.90),
            
            # Partner patterns
            (r'\b(partner|managing partner|general partner|equity partner)\b', 'Partner', 0.95),
            
            # VP patterns
            (r'\b(vp|v\.p\.|vice president|svp|senior vice president|evp|executive vice president)\b', 'VP', 0.95),
            
            # Head patterns
            (r'\b(head\s+of|head\s+\w+)\b', 'Head', 0.90),
            
            # Director patterns
            (r'\b(director|director\s+of|managing director|executive director|senior director)\b', 'Director', 0.90),
            
            # Manager patterns
            (r'\b(manager|managing|general manager|product manager|project manager|program manager|account manager|sales manager|engineering manager)\b', 'Manager', 0.85),
            
            # Senior patterns
            (r'\b(senior|sr\.|sr\s+|lead|principal|staff)\b', 'Senior', 0.80),
            
            # Intern patterns
            (r'\b(intern|internship|trainee)\b', 'Intern', 0.95),
            
            # Entry patterns (default for titles without seniority indicators)
            (r'\b(associate|junior|entry|assistant|coordinator|specialist|analyst|representative|executive)\b', 'Entry', 0.70),
        ]
    
    def _build_department_function_patterns(self):
        """Build patterns for detecting departments and functions."""
        # Department -> Function mappings with patterns
        # Order matters: more specific patterns should come first
        self.dept_function_patterns = [
            # Sales (check before generic Executive)
            {
                'department': 'Sales',
                'function': 'Sales',
                'patterns': [
                    (r'\b(sales\s+(executive|manager|rep|representative|person|specialist|director|vp|vice president)|salesperson|sales rep|sales representative|account executive|ae)\b', 0.95),
                    (r'\b(sales|account manager)\b', 0.90),
                ]
            },
            {
                'department': 'Sales',
                'function': 'Customer Success',
                'patterns': [
                    (r'\b(customer success|cs|account manager)\b', 0.90),
                ]
            },
            {
                'department': 'Sales',
                'function': 'Sales Engineering',
                'patterns': [
                    (r'\b(sales engineer|sales engineering|pre.?sales|technical sales)\b', 0.90),
                ]
            },
            {
                'department': 'Sales',
                'function': 'Business Development',
                'patterns': [
                    (r'\b(business development|bd|partnerships|partnership manager)\b', 0.90),
                ]
            },
            
            # C-Suite (after Sales to avoid conflicts)
            {
                'department': 'C-Suite',
                'function': 'Executive',
                'patterns': [
                    (r'\b(ceo|chief executive officer|cto|chief technology officer|cfo|chief financial officer|coo|chief operating officer|chro|chief human resources officer|cmo|chief marketing officer|cso|chief sales officer)\b', 0.95),
                    (r'\b(chief\s+\w+\s+officer|chief\s+\w+)\b', 0.90),
                    (r'\b(executive\s+(director|vp|vice president|manager))\b', 0.85),
                    (r'\b(executive)\b', 0.70),  # Lower confidence for generic "executive"
                ]
            },
            {
                'department': 'C-Suite',
                'function': 'Founder',
                'patterns': [
                    (r'\b(founder|co-founder|cofounder)\b', 0.95),
                ]
            },
            
            # Engineering & Technical
            {
                'department': 'Engineering & Technical',
                'function': 'Software Development',
                'patterns': [
                    (r'\b(software engineer|software developer|backend engineer|frontend engineer|full.?stack engineer|devops engineer|sre|site reliability engineer|engineer|developer|programmer|coder|swe)\b', 0.90),
                    (r'\b(backend|frontend|full.?stack|devops|sre)\b', 0.85),
                ]
            },
            {
                'department': 'Engineering & Technical',
                'function': 'Data Science',
                'patterns': [
                    (r'\b(data scientist|data engineer|data analyst|ml engineer|machine learning engineer|ai engineer|artificial intelligence)\b', 0.90),
                    (r'\b(data science|machine learning|ml|ai)\b', 0.85),
                ]
            },
            {
                'department': 'Engineering & Technical',
                'function': 'Product Management',
                'patterns': [
                    (r'\b(product manager|pm|product owner|product lead)\b', 0.90),
                ]
            },
            {
                'department': 'Engineering & Technical',
                'function': 'Project Management',
                'patterns': [
                    (r'\b(project manager|program manager|pmo|project management)\b', 0.90),
                ]
            },
            {
                'department': 'Engineering & Technical',
                'function': 'Test / Quality Assurance',
                'patterns': [
                    (r'\b(qa\s+engineer|quality assurance engineer|test engineer|qa engineer|quality engineer)\b', 0.95),
                    (r'\b(qa|quality assurance|tester|testing)\b', 0.90),
                ]
            },
            {
                'department': 'Engineering & Technical',
                'function': 'UI / UX',
                'patterns': [
                    (r'\b(ui|ux|ui/ux|user experience|user interface|ui engineer|ux engineer|ui designer|ux designer)\b', 0.90),
                ]
            },
            {
                'department': 'Engineering & Technical',
                'function': 'DevOps',
                'patterns': [
                    (r'\b(devops|dev ops|infrastructure engineer|platform engineer|cloud engineer)\b', 0.90),
                ]
            },
            {
                'department': 'Engineering & Technical',
                'function': 'Engineering & Technical',
                'patterns': [
                    (r'\b(engineering|technical|tech|technology)\b', 0.70),
                ]
            },
            
            # Marketing
            {
                'department': 'Marketing',
                'function': 'Marketing',
                'patterns': [
                    (r'\b(marketing|marketer|marketing manager|marketing specialist|digital marketing|content marketing)\b', 0.90),
                ]
            },
            {
                'department': 'Marketing',
                'function': 'Public Relations',
                'patterns': [
                    (r'\b(public relations|pr|communications|comms|communications consultant)\b', 0.90),
                ]
            },
            {
                'department': 'Marketing',
                'function': 'Content Marketing',
                'patterns': [
                    (r'\b(content marketing|content manager|content creator|content strategist)\b', 0.90),
                ]
            },
            {
                'department': 'Marketing',
                'function': 'Digital Marketing',
                'patterns': [
                    (r'\b(digital marketing|seo|search engine optimization|ppc|pay per click|social media)\b', 0.90),
                ]
            },
            
            # Finance
            {
                'department': 'Finance',
                'function': 'Finance',
                'patterns': [
                    (r'\b(finance|financial|financier|financial analyst|financial manager)\b', 0.90),
                ]
            },
            {
                'department': 'Finance',
                'function': 'Accounting',
                'patterns': [
                    (r'\b(accountant|accounting|bookkeeper|cpa|controller|comptroller)\b', 0.90),
                ]
            },
            {
                'department': 'Finance',
                'function': 'Financial Planning & Analysis',
                'patterns': [
                    (r'\b(fp&a|financial planning|financial analysis|fpa)\b', 0.90),
                ]
            },
            
            # Human Resources
            {
                'department': 'Human Resources',
                'function': 'Human Resources',
                'patterns': [
                    (r'\b(hr|human resources|people ops|people operations|talent|recruiter|recruiting)\b', 0.90),
                ]
            },
            {
                'department': 'Human Resources',
                'function': 'Recruiting & Talent Acquisition',
                'patterns': [
                    (r'\b(recruiter|recruiting|talent acquisition|talent acquisition specialist|talent sourcer)\b', 0.90),
                ]
            },
            
            # Operations
            {
                'department': 'Operations',
                'function': 'Operations',
                'patterns': [
                    (r'\b(operations|ops|operations manager|operations specialist)\b', 0.90),
                ]
            },
            {
                'department': 'Operations',
                'function': 'Customer Service / Support',
                'patterns': [
                    (r'\b(customer service|customer support|support|help desk|customer care)\b', 0.90),
                ]
            },
            {
                'department': 'Operations',
                'function': 'Compliance',
                'patterns': [
                    (r'\b(compliance\s+(manager|officer|specialist|director))\b', 0.95),
                    (r'\b(compliance)\b', 0.90),
                ]
            },
            {
                'department': 'Operations',
                'function': 'Safety',
                'patterns': [
                    (r'\b(safety|health safety|hse|health safety environment|safety coordinator|safety manager)\b', 0.90),
                ]
            },
            {
                'department': 'Operations',
                'function': 'Operations',
                'patterns': [
                    (r'\b(coordinator|specialist|administrative assistant|admin|assistant)\b', 0.70),
                ]
            },
            
            # Legal
            {
                'department': 'Legal',
                'function': 'Legal',
                'patterns': [
                    (r'\b(lawyer|attorney|legal|counsel|legal counsel|paralegal)\b', 0.90),
                ]
            },
            
            # Medical & Health
            {
                'department': 'Medical & Health',
                'function': 'Medicine',
                'patterns': [
                    (r'\b(doctor|physician|md|nurse|nursing|clinician|medical|healthcare|health care)\b', 0.90),
                ]
            },
            {
                'department': 'Medical & Health',
                'function': 'Nursing',
                'patterns': [
                    (r'\b(nurse|nursing|rn|registered nurse|nurse practitioner)\b', 0.90),
                ]
            },
            
            # Information Technology
            {
                'department': 'Information Technology',
                'function': 'Information Technology',
                'patterns': [
                    (r'\b(it|information technology|it manager|it specialist|it support|systems administrator|sysadmin)\b', 0.90),
                ]
            },
            {
                'department': 'Information Technology',
                'function': 'Information Security',
                'patterns': [
                    (r'\b(security|cybersecurity|information security|infosec|security engineer|security analyst)\b', 0.90),
                ]
            },
            
            # Design
            {
                'department': 'Design',
                'function': 'Product or UI/UX Design',
                'patterns': [
                    (r'\b(ui designer|ux designer|product designer|graphic designer|photographer|designer)\b', 0.90),
                    (r'\b(design|ui|ux)\b', 0.85),
                ]
            },
            
            # Consulting
            {
                'department': 'Consulting',
                'function': 'Management Consulting',
                'patterns': [
                    (r'\b(consultant|consulting|management consultant|strategy consultant)\b', 0.85),
                ]
            },
            
            # Education
            {
                'department': 'Education',
                'function': 'Teacher',
                'patterns': [
                    (r'\b(teacher|educator|instructor|professor|lecturer|specialist|trio|upward bound)\b', 0.90),
                ]
            },
        ]
    
    def normalize_title(self, title: str) -> str:
        """
        Normalize a job title for pattern matching.
        
        Args:
            title: Raw job title string
            
        Returns:
            Normalized title string (lowercase, cleaned)
        """
        if not title:
            return ""
        
        # Convert to lowercase
        normalized = title.lower().strip()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Remove common punctuation that doesn't affect meaning
        normalized = normalized.replace(',', ' ')
        normalized = normalized.replace('.', ' ')
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized.strip()
    
    def classify_seniority(self, normalized_title: str) -> Tuple[Optional[str], float]:
        """
        Classify seniority level from normalized title.
        
        Args:
            normalized_title: Normalized job title
            
        Returns:
            Tuple of (seniority_level, confidence)
        """
        if not normalized_title:
            return None, 0.0
        
        # Check patterns in order (most specific first)
        for pattern, seniority, base_confidence in self.seniority_patterns:
            if re.search(pattern, normalized_title, re.IGNORECASE):
                # Adjust confidence based on pattern match quality
                matches = re.findall(pattern, normalized_title, re.IGNORECASE)
                if matches:
                    # Exact word match gets higher confidence
                    confidence = base_confidence
                    return seniority, confidence
        
        # Default to Entry if no seniority indicators found
        return 'Entry', 0.50
    
    def classify_department_function(self, normalized_title: str) -> Tuple[Optional[str], Optional[str], float]:
        """
        Classify department and function from normalized title.
        
        Args:
            normalized_title: Normalized job title
            
        Returns:
            Tuple of (department, function, confidence)
        """
        if not normalized_title:
            return None, None, 0.0
        
        best_match = None
        best_confidence = 0.0
        
        # Check all department/function patterns
        for dept_func in self.dept_function_patterns:
            department = dept_func['department']
            function = dept_func['function']
            patterns = dept_func['patterns']
            
            for pattern, base_confidence in patterns:
                if re.search(pattern, normalized_title, re.IGNORECASE):
                    # Use the highest confidence match
                    if base_confidence > best_confidence:
                        best_match = (department, function)
                        best_confidence = base_confidence
                    break  # Found a match for this dept/func, move to next
        
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
                method="rule"
            )
        
        # Normalize title
        normalized = self.normalize_title(title)
        
        # Classify seniority
        seniority, seniority_conf = self.classify_seniority(normalized)
        
        # Classify department and function
        department, function, dept_func_conf = self.classify_department_function(normalized)
        
        # Calculate overall confidence
        # If we have both seniority and department/function, average them
        # If we only have one, use that confidence
        if seniority and department:
            overall_confidence = (seniority_conf + dept_func_conf) / 2.0
        elif seniority:
            overall_confidence = seniority_conf * 0.7  # Lower confidence if missing dept/func
        elif department:
            overall_confidence = dept_func_conf * 0.7  # Lower confidence if missing seniority
        else:
            overall_confidence = 0.0
        
        return ClassificationResult(
            department=department,
            function=function,
            seniority=seniority,
            confidence=overall_confidence,
            method="rule"
        )


def main():
    """Test the rule classifier on sample titles."""
    classifier = RuleClassifier()
    
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
    print("RULE CLASSIFIER - TEST RESULTS")
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
