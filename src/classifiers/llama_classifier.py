#!/usr/bin/env python3
"""
Llama-3.2-1B-Instruct Classifier for Job Title Standardization

Uses Meta's Llama-3.2-1B-Instruct model to classify job titles into
department, function, and seniority using LLM-based reasoning.
"""

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from typing import Optional
from dataclasses import dataclass
import re
import json
import time


@dataclass
class ClassificationResult:
    """Result of a job title classification."""
    department: Optional[str]
    function: Optional[str]
    seniority: Optional[str]
    confidence: float
    method: str = "llama"


class LlamaClassifier:
    """
    Llama-3.2-1B-Instruct-based classifier for job titles.
    
    Uses the Llama model to classify job titles into:
    - Department (e.g., "Sales", "Engineering & Technical")
    - Function (e.g., "Software Development", "Sales")
    - Seniority (e.g., "Senior", "Manager", "Director")
    """
    
    # Valid taxonomy values
    SENIORITY_LEVELS = [
        "Owner", "Founder", "C-suite", "Partner", "VP", "Head",
        "Director", "Manager", "Senior", "Entry", "Intern"
    ]
    
    DEPARTMENTS = [
        "C-Suite", "Engineering & Technical", "Design", "Education",
        "Finance", "Human Resources", "Information Technology", "Legal",
        "Marketing", "Medical & Health", "Operations", "Sales", "Consulting"
    ]
    
    def __init__(self, model_name: str = "meta-llama/Llama-3.2-1B-Instruct"):
        """
        Initialize the Llama classifier.
        
        Args:
            model_name: HuggingFace model identifier
        """
        print(f"Loading model {model_name}...")
        self.model_name = model_name
        
        # Load tokenizer and model
        try:
            # Check for HuggingFace token
            from huggingface_hub import HfFolder
            token = HfFolder.get_token()
            if not token:
                print("⚠ Warning: No HuggingFace token found.")
                print("  This model requires authentication. Please run:")
                print("    huggingface-cli login")
                print("  Or set HF_TOKEN environment variable")
                print("  You can get a token at: https://huggingface.co/settings/tokens")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.bfloat16,
                device_map="auto",
            )
            print("✓ Model loaded successfully")
        except Exception as e:
            error_msg = str(e)
            if "gated" in error_msg.lower() or "401" in error_msg or "access" in error_msg.lower():
                raise RuntimeError(
                    f"Failed to access model {model_name}: {e}\n\n"
                    "This model requires authentication. Please:\n"
                    "1. Get a HuggingFace token: https://huggingface.co/settings/tokens\n"
                    "2. Log in: huggingface-cli login\n"
                    "3. Request access: https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct\n"
                    "   (Click 'Agree and access repository')\n"
                    "4. Run this script again"
                )
            else:
                raise RuntimeError(f"Failed to load model {model_name}: {e}")
        
        # Build classification prompt template
        self._build_prompt_template()
    
    def _build_prompt_template(self):
        """Build the prompt template for classification."""
        self.prompt_template = """You are a job title classifier. Classify the given job title into:
1. Department (choose ONE from: C-Suite, Engineering & Technical, Design, Education, Finance, Human Resources, Information Technology, Legal, Marketing, Medical & Health, Operations, Sales, Consulting)
2. Function (choose the most specific function within the department)
3. Seniority (choose ONE from: Owner, Founder, C-suite, Partner, VP, Head, Director, Manager, Senior, Entry, Intern)

Job Title: {title}

Respond ONLY with a JSON object in this exact format:
{{
  "department": "Department Name",
  "function": "Function Name",
  "seniority": "Seniority Level",
  "confidence": 0.0-1.0
}}

JSON:"""
    
    def _create_prompt(self, title: str) -> str:
        """Create a classification prompt for the given title."""
        return self.prompt_template.format(title=title)
    
    def _parse_response(self, response_text: str) -> dict:
        """
        Parse the LLM response to extract classification.
        
        Returns:
            Dictionary with department, function, seniority, confidence
        """
        # Try to extract JSON from the response
        json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                
                # Validate and normalize values
                department = result.get('department', '').strip()
                function = result.get('function', '').strip()
                seniority = result.get('seniority', '').strip()
                confidence = float(result.get('confidence', 0.5))
                
                # Normalize department names
                department = self._normalize_department(department)
                seniority = self._normalize_seniority(seniority)
                
                return {
                    'department': department if department else None,
                    'function': function if function else None,
                    'seniority': seniority if seniority else None,
                    'confidence': max(0.0, min(1.0, confidence))
                }
            except json.JSONDecodeError:
                pass
        
        # Fallback: try to extract values using regex
        dept_match = re.search(r'"department"\s*:\s*"([^"]+)"', response_text, re.IGNORECASE)
        func_match = re.search(r'"function"\s*:\s*"([^"]+)"', response_text, re.IGNORECASE)
        seniority_match = re.search(r'"seniority"\s*:\s*"([^"]+)"', response_text, re.IGNORECASE)
        conf_match = re.search(r'"confidence"\s*:\s*([0-9.]+)', response_text, re.IGNORECASE)
        
        department = dept_match.group(1).strip() if dept_match else None
        function = func_match.group(1).strip() if func_match else None
        seniority = seniority_match.group(1).strip() if seniority_match else None
        confidence = float(conf_match.group(1)) if conf_match else 0.5
        
        if department:
            department = self._normalize_department(department)
        if seniority:
            seniority = self._normalize_seniority(seniority)
        
        return {
            'department': department if department else None,
            'function': function if function else None,
            'seniority': seniority if seniority else None,
            'confidence': max(0.0, min(1.0, confidence))
        }
    
    def _normalize_department(self, dept: str) -> Optional[str]:
        """Normalize department name to match taxonomy."""
        dept_lower = dept.lower().strip()
        
        # Map variations to standard names
        dept_mapping = {
            'c-suite': 'C-Suite',
            'c suite': 'C-Suite',
            'engineering & technical': 'Engineering & Technical',
            'engineering and technical': 'Engineering & Technical',
            'engineering': 'Engineering & Technical',
            'technical': 'Engineering & Technical',
            'design': 'Design',
            'education': 'Education',
            'finance': 'Finance',
            'human resources': 'Human Resources',
            'hr': 'Human Resources',
            'information technology': 'Information Technology',
            'it': 'Information Technology',
            'legal': 'Legal',
            'marketing': 'Marketing',
            'medical & health': 'Medical & Health',
            'medical and health': 'Medical & Health',
            'medical': 'Medical & Health',
            'health': 'Medical & Health',
            'operations': 'Operations',
            'sales': 'Sales',
            'consulting': 'Consulting',
        }
        
        return dept_mapping.get(dept_lower, dept if dept in self.DEPARTMENTS else None)
    
    def _normalize_seniority(self, seniority: str) -> Optional[str]:
        """Normalize seniority level to match taxonomy."""
        seniority_lower = seniority.lower().strip()
        
        # Map variations to standard names
        seniority_mapping = {
            'owner': 'Owner',
            'founder': 'Founder',
            'c-suite': 'C-suite',
            'c suite': 'C-suite',
            'partner': 'Partner',
            'vp': 'VP',
            'vice president': 'VP',
            'head': 'Head',
            'director': 'Director',
            'manager': 'Manager',
            'senior': 'Senior',
            'entry': 'Entry',
            'intern': 'Intern',
        }
        
        return seniority_mapping.get(seniority_lower, seniority if seniority in self.SENIORITY_LEVELS else None)
    
    def classify(self, title: str) -> ClassificationResult:
        """
        Classify a job title.
        
        Args:
            title: Job title to classify
            
        Returns:
            ClassificationResult with department, function, seniority, and confidence
        """
        if not title or not title.strip():
            return ClassificationResult(
                department=None,
                function=None,
                seniority=None,
                confidence=0.0
            )
        
        # Create prompt
        prompt = self._create_prompt(title.strip())
        
        # Format for Llama chat template
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Tokenize and generate
        try:
            input_ids = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(self.model.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_new_tokens=256,
                    temperature=0.1,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)
            
            # Parse response
            parsed = self._parse_response(response)
            
            return ClassificationResult(
                department=parsed['department'],
                function=parsed['function'],
                seniority=parsed['seniority'],
                confidence=parsed['confidence']
            )
            
        except Exception as e:
            print(f"Error classifying '{title}': {e}")
            return ClassificationResult(
                department=None,
                function=None,
                seniority=None,
                confidence=0.0
            )


def main():
    """Test the Llama classifier on sample titles."""
    try:
        classifier = LlamaClassifier()
    except Exception as e:
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
    print("LLAMA CLASSIFIER - TEST RESULTS")
    print("=" * 100)
    print(f"\nTesting {len(sample_titles)} job titles...\n")
    
    results = []
    times = []
    
    for i, title in enumerate(sample_titles, 1):
        print(f"[{i}/{len(sample_titles)}] Classifying: {title}")
        start_time = time.time()
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
    
    # Print results in a table format
    print("\n" + "=" * 100)
    print(f"{'Title':<50} {'Department':<25} {'Function':<30} {'Seniority':<15} {'Confidence':<10}")
    print("-" * 130)
    
    for r in results:
        dept = r['department'] or 'N/A'
        func = r['function'] or 'N/A'
        seniority = r['seniority'] or 'N/A'
        conf = r['confidence']
        
        print(f"{r['title'][:49]:<50} {dept[:24]:<25} {func[:29]:<30} {seniority[:14]:<15} {conf:.2f}")
    
    # Print statistics
    print("\n" + "=" * 100)
    print("STATISTICS")
    print("=" * 100)
    
    classified = sum(1 for r in results if r['department'] is not None)
    avg_conf = sum(r['confidence'] for r in results) / len(results) if results else 0
    avg_time = sum(times) / len(times) if times else 0
    
    print(f"Total Titles: {len(results)}")
    print(f"Successfully Classified: {classified}/{len(results)} ({classified/len(results)*100:.1f}%)")
    print(f"Average Confidence: {avg_conf:.3f}")
    print(f"Average Time per Title: {avg_time*1000:.2f} ms")
    
    # Distribution by department
    dept_dist = {}
    for r in results:
        if r['department']:
            dept_dist[r['department']] = dept_dist.get(r['department'], 0) + 1
    
    print("\nDepartment Distribution:")
    for dept, count in sorted(dept_dist.items()):
        print(f"  {dept}: {count}")
    
    # Distribution by seniority
    seniority_dist = {}
    for r in results:
        if r['seniority']:
            seniority_dist[r['seniority']] = seniority_dist.get(r['seniority'], 0) + 1
    
    print("\nSeniority Distribution:")
    for seniority, count in sorted(seniority_dist.items()):
        print(f"  {seniority}: {count}")
    
    print("\n" + "=" * 100)


if __name__ == '__main__':
    main()
