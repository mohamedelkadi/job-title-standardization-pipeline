====================================================================================================
CLASSIFIER COMPARISON REPORT
Rule-based vs spaCy-based Job Title Classification
====================================================================================================

## OVERALL STATISTICS
----------------------------------------------------------------------------------------------------
Total Titles Tested: 30

### Classification Coverage
  Rule Classifier: 28/30 (93.3%)
  spaCy Classifier: 25/30 (83.3%)

### Average Confidence Scores
  Rule Classifier: 0.808
  spaCy Classifier: 0.784
  Difference: 0.024

### Performance (Average Time per Title)
  Rule Classifier: 0.108 ms
  spaCy Classifier: 3.471 ms
  Speed Ratio: 32.09x slower

## AGREEMENT ANALYSIS
----------------------------------------------------------------------------------------------------
Full Agreement (Dept + Function + Seniority): 22/30 (73.3%)
Department Agreement: 25/30 (83.3%)
Function Agreement: 22/30 (73.3%)
Seniority Agreement: 30/30 (100.0%)

## DETAILED COMPARISON
----------------------------------------------------------------------------------------------------
Title                                         Rule Dept            spaCy Dept           Match   
----------------------------------------------------------------------------------------------------
Backend Engineer                              Engineering & Techn  Engineering & Techn  ✓       
Head of Sales                                 Sales                Sales                ✓       
Sales Executive                               Sales                Sales                ✓       
SWE Intern                                    Engineering & Techn  Engineering & Techn  ✓       
Senior Software Engineer                      Engineering & Techn  Engineering & Techn  ✓       
VP of Engineering                             Engineering & Techn  N/A                  ✗       
CEO                                           C-Suite              C-Suite              ✓       
Founder                                       C-Suite              C-Suite              ✓       
Product Manager                               Engineering & Techn  Engineering & Techn  ✓       
Data Scientist                                Engineering & Techn  Engineering & Techn  ✓       
Public Relations                              Marketing            Marketing            ✓       
Compliance Manager                            Operations           Operations           ✓       
Technical Account Manager                     Sales                Sales                ✓       
Sr Program Manager at Amazon Web Services (A  Engineering & Techn  Engineering & Techn  ✓       
Owner, VITAL AZ LLC                           N/A                  N/A                  ✓       
General Partner of Top of the World Media     N/A                  N/A                  ✓       
Communications Consultant at Vanguard         Marketing            Consulting           ✗       
Crisis Assessment and Intervention Clinician  Medical & Health     Medical & Health     ✓       
Health Safety Environment Coordinator         Operations           Operations           ✓       
TRiO Upward Bound Specialist                  Education            N/A                  ✗       
Administrative Assistant                      Operations           N/A                  ✗       
Fashion, Portrait & Interior Photographer     Design               Design               ✓       
Director of Marketing                         Marketing            Marketing            ✓       
Senior Sales Manager                          Sales                Sales                ✓       
Junior Developer                              Engineering & Techn  Engineering & Techn  ✓       
QA Engineer                                   Engineering & Techn  Engineering & Techn  ✓       
UX Designer                                   Engineering & Techn  Design               ✗       
Customer Success Manager                      Sales                Sales                ✓       
HR Manager                                    Human Resources      Human Resources      ✓       
Finance Director                              Finance              Finance              ✓       

## DISAGREEMENTS
----------------------------------------------------------------------------------------------------
Found 8 titles with disagreements:

Title: VP of Engineering
  Rule:    Dept=Engineering & Technical, Func=Engineering & Technical, Seniority=VP, Conf=0.82
  spaCy:   Dept=None, Func=None, Seniority=VP, Conf=0.66

Title: Public Relations
  Rule:    Dept=Marketing, Func=Public Relations, Seniority=Entry, Conf=0.70
  spaCy:   Dept=Marketing, Func=Marketing, Seniority=Entry, Conf=0.70

Title: Compliance Manager
  Rule:    Dept=Operations, Func=Compliance, Seniority=Manager, Conf=0.90
  spaCy:   Dept=Operations, Func=Operations, Seniority=Manager, Conf=0.88

Title: Communications Consultant at Vanguard
  Rule:    Dept=Marketing, Func=Public Relations, Seniority=Entry, Conf=0.70
  spaCy:   Dept=Consulting, Func=Management Consulting, Seniority=Entry, Conf=0.68

Title: Health Safety Environment Coordinator
  Rule:    Dept=Operations, Func=Safety, Seniority=Entry, Conf=0.80
  spaCy:   Dept=Operations, Func=Operations, Seniority=Entry, Conf=0.80

Title: TRiO Upward Bound Specialist
  Rule:    Dept=Education, Func=Teacher, Seniority=Entry, Conf=0.80
  spaCy:   Dept=None, Func=None, Seniority=Entry, Conf=0.49

Title: Administrative Assistant
  Rule:    Dept=Operations, Func=Operations, Seniority=Entry, Conf=0.70
  spaCy:   Dept=None, Func=None, Seniority=Entry, Conf=0.49

Title: UX Designer
  Rule:    Dept=Engineering & Technical, Func=UI / UX, Seniority=Entry, Conf=0.70
  spaCy:   Dept=Design, Func=Product or UI/UX Design, Seniority=Entry, Conf=0.70

## DISTRIBUTION COMPARISON
----------------------------------------------------------------------------------------------------
### Department Distribution
Department                     Rule       spaCy      Diff      
------------------------------------------------------------
C-Suite                        2          2          0         
Consulting                     0          1          -1        
Design                         1          2          -1        
Education                      1          0          +1        
Engineering & Technical        10         8          +2        
Finance                        1          1          0         
Human Resources                1          1          0         
Marketing                      3          2          +1        
Medical & Health               1          1          0         
Operations                     3          2          +1        
Sales                          5          5          0         

### Seniority Distribution
Seniority            Rule       spaCy      Diff      
--------------------------------------------------
C-suite              1          1          0         
Director             2          2          0         
Entry                13         13         0         
Founder              1          1          0         
Head                 1          1          0         
Intern               1          1          0         
Manager              7          7          0         
Owner                1          1          0         
Partner              1          1          0         
Senior               1          1          0         
VP                   1          1          0         

## CONFIDENCE ANALYSIS
----------------------------------------------------------------------------------------------------
### Confidence Distribution
Level           Rule       spaCy     
-----------------------------------
High (≥0.8)     19         17        
Medium (0.5-0.8) 11         11        
Low (<0.5)      0          2         

## SUMMARY & RECOMMENDATIONS
----------------------------------------------------------------------------------------------------
⚠ Moderate agreement - some differences in classification

✓ Rule classifier is faster (0.11ms vs 3.47ms per title)

✓ Rule classifier has better coverage (28 vs 25 classifications)

====================================================================================================