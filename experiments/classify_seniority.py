#!/usr/bin/env python3
"""
Classify member titles to seniority levels using BART-large-MNLI model.
Generates a report of classifications.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from transformers import pipeline
import pandas as pd
from datetime import datetime

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'linkedin_members',
    'user': 'mo'
}

# Seniority levels from the taxonomy
SENIORITY_LEVELS = [
    'Owner',
    'Founder',
    'C-suite',
    'Partner',
    'VP',
    'Head',
    'Director',
    'Manager',
    'Senior',
    'Entry',
    'Intern'
]


def get_db_connection():
    """Connect to PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)


def get_member_titles(conn, limit=100):
    """Fetch member titles from database."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, title, name
            FROM member
            WHERE title IS NOT NULL 
              AND title != ''
              AND deleted = FALSE
            ORDER BY id
            LIMIT %s
        """, (limit,))
        return cur.fetchall()


def get_seniority_levels(conn):
    """Fetch seniority levels from database."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, name
            FROM member_seniority_levels
            ORDER BY id
        """)
        return cur.fetchall()


def classify_title(classifier, title, candidate_labels):
    """Classify a title to a seniority level using BART-large-MNLI."""
    if not title or not title.strip():
        return None, 0.0
    
    try:
        result = classifier(title, candidate_labels)
        
        # Get the top prediction
        if result['labels'] and result['scores']:
            predicted_label = result['labels'][0]
            confidence = result['scores'][0]
            return predicted_label, confidence
        else:
            return None, 0.0
    except Exception as e:
        print(f"Error classifying '{title}': {e}")
        return None, 0.0


def generate_report(results, output_file='seniority_classification_report.html'):
    """Generate an HTML report of the classifications."""
    
    # Create DataFrame for easier analysis
    df = pd.DataFrame(results)
    
    # Calculate statistics
    total_titles = len(df)
    successful_classifications = len(df[df['predicted_seniority'].notna()])
    avg_confidence = df['confidence'].mean()
    
    # Distribution by seniority
    seniority_dist = df['predicted_seniority'].value_counts()
    
    # Confidence distribution
    high_confidence = len(df[df['confidence'] >= 0.7])
    medium_confidence = len(df[(df['confidence'] >= 0.5) & (df['confidence'] < 0.7)])
    low_confidence = len(df[df['confidence'] < 0.5])
    
    # Generate HTML report
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Seniority Classification Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-card h3 {{
            margin: 0;
            font-size: 2em;
        }}
        .stat-card p {{
            margin: 5px 0 0 0;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .confidence-high {{
            color: #4CAF50;
            font-weight: bold;
        }}
        .confidence-medium {{
            color: #FF9800;
            font-weight: bold;
        }}
        .confidence-low {{
            color: #f44336;
            font-weight: bold;
        }}
        .timestamp {{
            color: #888;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Seniority Classification Report</h1>
        <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        
        <h2>Summary Statistics</h2>
        <div class="stats">
            <div class="stat-card">
                <h3>{total_titles}</h3>
                <p>Total Titles</p>
            </div>
            <div class="stat-card">
                <h3>{successful_classifications}</h3>
                <p>Successful Classifications</p>
            </div>
            <div class="stat-card">
                <h3>{avg_confidence:.2%}</h3>
                <p>Average Confidence</p>
            </div>
            <div class="stat-card">
                <h3>{high_confidence}</h3>
                <p>High Confidence (≥70%)</p>
            </div>
        </div>
        
        <h2>Confidence Distribution</h2>
        <table>
            <tr>
                <th>Confidence Level</th>
                <th>Count</th>
                <th>Percentage</th>
            </tr>
            <tr>
                <td>High (≥70%)</td>
                <td>{high_confidence}</td>
                <td>{(high_confidence/total_titles*100):.1f}%</td>
            </tr>
            <tr>
                <td>Medium (50-69%)</td>
                <td>{medium_confidence}</td>
                <td>{(medium_confidence/total_titles*100):.1f}%</td>
            </tr>
            <tr>
                <td>Low (&lt;50%)</td>
                <td>{low_confidence}</td>
                <td>{(low_confidence/total_titles*100):.1f}%</td>
            </tr>
        </table>
        
        <h2>Distribution by Seniority Level</h2>
        <table>
            <tr>
                <th>Seniority Level</th>
                <th>Count</th>
                <th>Percentage</th>
            </tr>
"""
    
    for seniority, count in seniority_dist.items():
        percentage = (count / total_titles * 100)
        html_content += f"""
            <tr>
                <td>{seniority}</td>
                <td>{count}</td>
                <td>{percentage:.1f}%</td>
            </tr>
"""
    
    html_content += """
        </table>
        
        <h2>Detailed Classifications</h2>
        <table>
            <tr>
                <th>Member ID</th>
                <th>Name</th>
                <th>Title</th>
                <th>Predicted Seniority</th>
                <th>Confidence</th>
            </tr>
"""
    
    for _, row in df.iterrows():
        confidence_class = 'confidence-high' if row['confidence'] >= 0.7 else ('confidence-medium' if row['confidence'] >= 0.5 else 'confidence-low')
        predicted = row['predicted_seniority'] if pd.notna(row['predicted_seniority']) else 'N/A'
        
        html_content += f"""
            <tr>
                <td>{row['member_id']}</td>
                <td>{row['name']}</td>
                <td>{row['title']}</td>
                <td>{predicted}</td>
                <td class="{confidence_class}">{row['confidence']:.2%}</td>
            </tr>
"""
    
    html_content += """
        </table>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nReport saved to: {output_file}")
    
    # Also save CSV for easy analysis
    csv_file = output_file.replace('.html', '.csv')
    df.to_csv(csv_file, index=False)
    print(f"CSV export saved to: {csv_file}")
    
    # Also print summary to console
    print("\n" + "="*80)
    print("CLASSIFICATION SUMMARY")
    print("="*80)
    print(f"Total titles processed: {total_titles}")
    print(f"Successful classifications: {successful_classifications}")
    print(f"Average confidence: {avg_confidence:.2%}")
    print(f"\nConfidence distribution:")
    print(f"  High (≥70%): {high_confidence} ({(high_confidence/total_titles*100):.1f}%)")
    print(f"  Medium (50-69%): {medium_confidence} ({(medium_confidence/total_titles*100):.1f}%)")
    print(f"  Low (<50%): {low_confidence} ({(low_confidence/total_titles*100):.1f}%)")
    print(f"\nDistribution by seniority level:")
    for seniority, count in seniority_dist.items():
        print(f"  {seniority}: {count} ({(count/total_titles*100):.1f}%)")


def main():
    """Main function to classify titles and generate report."""
    print("="*80)
    print("Seniority Classification using BART-large-MNLI")
    print("="*80)
    
    # Connect to database
    print("\n[1/4] Connecting to database...")
    conn = get_db_connection()
    print("✓ Connected to database")
    
    # Fetch titles
    print("\n[2/4] Fetching member titles...")
    titles = get_member_titles(conn, limit=100)
    print(f"✓ Fetched {len(titles)} titles")
    
    if not titles:
        print("No titles found in database!")
        conn.close()
        return
    
    # Fetch seniority levels
    print("\n[3/4] Fetching seniority levels...")
    seniority_levels = get_seniority_levels(conn)
    conn.close()
    
    # Use database seniority levels if available, otherwise use hardcoded list
    if seniority_levels:
        candidate_labels = [level['name'] for level in seniority_levels]
        print(f"✓ Found {len(candidate_labels)} seniority levels in database")
    else:
        candidate_labels = SENIORITY_LEVELS
        print(f"✓ Using hardcoded seniority levels ({len(candidate_labels)} levels)")
    
    # Initialize classifier
    print("\n[4/4] Loading BART-large-MNLI model...")
    print("This may take a few minutes on first run (downloading model)...")
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )
    print("✓ Model loaded")
    
    # Classify titles
    print(f"\nClassifying {len(titles)} titles...")
    results = []
    
    for i, member in enumerate(titles, 1):
        title = member['title']
        predicted_seniority, confidence = classify_title(classifier, title, candidate_labels)
        
        results.append({
            'member_id': member['id'],
            'name': member['name'] or 'N/A',
            'title': title,
            'predicted_seniority': predicted_seniority,
            'confidence': confidence
        })
        
        if i % 10 == 0:
            print(f"  Processed {i}/{len(titles)} titles...")
    
    print(f"✓ Classification complete")
    
    # Generate report
    print("\nGenerating report...")
    generate_report(results)
    print("\n✓ Done!")


if __name__ == '__main__':
    main()
