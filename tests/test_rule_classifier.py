#!/usr/bin/env python3
"""
Test Rule Classifier on Database Samples

Fetches sample job titles from the database and runs the rule classifier on them.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import psycopg2
from psycopg2.extras import RealDictCursor
from src.classifiers.rule_classifier import RuleClassifier

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'linkedin_members',
    'user': 'mo'
}


def get_db_connection():
    """Connect to PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def get_sample_titles(conn, limit=50):
    """Fetch sample job titles from database."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT title
            FROM (
                SELECT DISTINCT title
                FROM member
                WHERE title IS NOT NULL 
                  AND title != ''
                  AND deleted = FALSE
            ) AS distinct_titles
            ORDER BY RANDOM()
            LIMIT %s
        """, (limit,))
        return [row['title'] for row in cur.fetchall()]


def main():
    """Main function to test rule classifier on database samples."""
    print("=" * 100)
    print("RULE CLASSIFIER - DATABASE SAMPLE TEST")
    print("=" * 100)
    
    # Connect to database
    print("\n[1/3] Connecting to database...")
    conn = get_db_connection()
    if not conn:
        print("❌ Failed to connect to database. Using hardcoded samples instead.")
        # Fallback to hardcoded samples
        sample_titles = [
            "Backend Engineer",
            "Head of Sales",
            "Sales Executive",
            "Senior Software Engineer",
            "CEO",
            "Product Manager",
        ]
    else:
        print("✓ Connected to database")
        
        # Fetch sample titles
        print("\n[2/3] Fetching sample titles from database...")
        sample_titles = get_sample_titles(conn, limit=50)
        conn.close()
        print(f"✓ Fetched {len(sample_titles)} titles")
    
    if not sample_titles:
        print("No titles found!")
        return
    
    # Initialize classifier
    print("\n[3/3] Initializing rule classifier...")
    classifier = RuleClassifier()
    print("✓ Classifier ready")
    
    # Classify titles
    print(f"\nClassifying {len(sample_titles)} titles...\n")
    
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
    print(f"{'Title':<60} {'Department':<25} {'Function':<30} {'Seniority':<15} {'Confidence':<10}")
    print("-" * 140)
    
    for r in results:
        dept = r['department'] or 'N/A'
        func = r['function'] or 'N/A'
        seniority = r['seniority'] or 'N/A'
        conf = f"{r['confidence']:.2f}"
        
        # Truncate long titles
        title_display = r['title'][:58] + '..' if len(r['title']) > 60 else r['title']
        
        print(f"{title_display:<60} {dept:<25} {func:<30} {seniority:<15} {conf:<10}")
    
    # Statistics
    print("\n" + "=" * 100)
    print("STATISTICS")
    print("=" * 100)
    
    total = len(results)
    classified = sum(1 for r in results if r['department'] is not None)
    avg_confidence = sum(r['confidence'] for r in results) / total if total > 0 else 0
    
    high_confidence = sum(1 for r in results if r['confidence'] >= 0.8)
    medium_confidence = sum(1 for r in results if 0.5 <= r['confidence'] < 0.8)
    low_confidence = sum(1 for r in results if r['confidence'] < 0.5)
    
    print(f"Total titles: {total}")
    print(f"Successfully classified: {classified} ({classified/total*100:.1f}%)")
    print(f"Average confidence: {avg_confidence:.2f}")
    print(f"\nConfidence distribution:")
    print(f"  High (≥0.8): {high_confidence} ({high_confidence/total*100:.1f}%)")
    print(f"  Medium (0.5-0.8): {medium_confidence} ({medium_confidence/total*100:.1f}%)")
    print(f"  Low (<0.5): {low_confidence} ({low_confidence/total*100:.1f}%)")
    
    # Distribution by department
    dept_dist = {}
    for r in results:
        if r['department']:
            dept_dist[r['department']] = dept_dist.get(r['department'], 0) + 1
    
    if dept_dist:
        print(f"\nDistribution by Department:")
        for dept, count in sorted(dept_dist.items(), key=lambda x: -x[1]):
            print(f"  {dept}: {count} ({count/total*100:.1f}%)")
    
    # Distribution by seniority
    seniority_dist = {}
    for r in results:
        if r['seniority']:
            seniority_dist[r['seniority']] = seniority_dist.get(r['seniority'], 0) + 1
    
    if seniority_dist:
        print(f"\nDistribution by Seniority:")
        for seniority, count in sorted(seniority_dist.items(), key=lambda x: -x[1]):
            print(f"  {seniority}: {count} ({count/total*100:.1f}%)")
    
    # Show unclassified titles
    unclassified = [r for r in results if r['department'] is None]
    if unclassified:
        print(f"\nUnclassified Titles ({len(unclassified)}):")
        for r in unclassified[:10]:  # Show first 10
            print(f"  - {r['title']}")
        if len(unclassified) > 10:
            print(f"  ... and {len(unclassified) - 10} more")
    
    print("\n" + "=" * 100)


if __name__ == '__main__':
    main()
