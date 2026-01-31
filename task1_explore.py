"""
Task 1: Data Exploration Script
Standalone script to explore the Ethiopia Financial Inclusion dataset
"""

import pandas as pd
import sys
from pathlib import Path

# Get project root
project_root = Path(__file__).parent
data_dir = project_root / "data" / "raw"

print("=" * 80)
print("ETHIOPIA FINANCIAL INCLUSION DATA EXPLORATION")
print("=" * 80)

# Load unified data
print("\nLoading unified data...")
unified_file = data_dir / "ethiopia_fi_unified_data.xlsx"

try:
    # Check available sheets
    xl_file = pd.ExcelFile(unified_file)
    print(f"Available sheets: {xl_file.sheet_names}")
    
    # Load main data (first sheet)
    main_data = pd.read_excel(unified_file, sheet_name=0)
    print(f"\nMain data shape: {main_data.shape}")
    print(f"Columns: {main_data.columns.tolist()}")
    
    # Try to load second sheet if it exists
    impact_links = None
    if len(xl_file.sheet_names) > 1:
        impact_links = pd.read_excel(unified_file, sheet_name=1)
        print(f"\nImpact links shape: {impact_links.shape}")
    else:
        # Check if impact_links are in main data
        if 'record_type' in main_data.columns:
            impact_links = main_data[main_data['record_type'] == 'impact_link'].copy()
            main_data = main_data[main_data['record_type'] != 'impact_link'].copy()
            print(f"\nSeparated impact links: {len(impact_links)} records")
    
    # Load reference codes
    print("\nLoading reference codes...")
    ref_file = data_dir / "reference_codes.xlsx"
    ref_codes = pd.read_excel(ref_file)
    print(f"Reference codes shape: {ref_codes.shape}")
    
    # EXPLORATION
    print("\n" + "=" * 80)
    print("1. RECORD TYPE DISTRIBUTION")
    print("=" * 80)
    if 'record_type' in main_data.columns:
        print(main_data['record_type'].value_counts())
    
    print("\n" + "=" * 80)
    print("2. PILLAR DISTRIBUTION (observations only)")
    print("=" * 80)
    if 'record_type' in main_data.columns and 'pillar' in main_data.columns:
        obs = main_data[main_data['record_type'] == 'observation']
        print(obs['pillar'].value_counts())
    
    print("\n" + "=" * 80)
    print("3. TEMPORAL RANGE")
    print("=" * 80)
    date_cols = [col for col in main_data.columns if 'date' in col.lower()]
    for col in date_cols:
        if main_data[col].notna().any():
            dates = pd.to_datetime(main_data[col], errors='coerce').dropna()
            if len(dates) > 0:
                print(f"\n{col}:")
                print(f"  Min: {dates.min()}")
                print(f"  Max: {dates.max()}")
                print(f"  Unique values: {dates.nunique()}")
    
    print("\n" + "=" * 80)
    print("4. INDICATORS")
    print("=" * 80)
    if 'indicator_code' in main_data.columns:
        indicators = main_data[main_data['indicator_code'].notna()]['indicator_code'].unique()
        print(f"Total unique indicators: {len(indicators)}")
        print("\nSample indicators:")
        for ind in sorted(indicators)[:10]:
            count = len(main_data[main_data['indicator_code'] == ind])
            print(f"  {ind}: {count} records")
    
    print("\n" + "=" * 80)
    print("5. EVENTS")
    print("=" * 80)
    if 'record_type' in main_data.columns:
        events = main_data[main_data['record_type'] == 'event']
        print(f"Total events: {len(events)}")
        if 'category' in events.columns:
            print("\nEvents by category:")
            print(events['category'].value_counts())
        if len(events) > 0:
            print("\nSample events:")
            event_cols = [c for c in ['record_id', 'indicator', 'category', 'observation_date'] if c in events.columns]
            print(events[event_cols].head(10).to_string())
    
    print("\n" + "=" * 80)
    print("6. IMPACT LINKS")
    print("=" * 80)
    if impact_links is not None and len(impact_links) > 0:
        print(f"Total impact links: {len(impact_links)}")
        if 'pillar' in impact_links.columns:
            print("\nImpact links by pillar:")
            print(impact_links['pillar'].value_counts())
        if 'impact_direction' in impact_links.columns:
            print("\nImpact direction:")
            print(impact_links['impact_direction'].value_counts())
    
    print("\n" + "=" * 80)
    print("7. DATA QUALITY - MISSING VALUES")
    print("=" * 80)
    missing = main_data.isnull().sum()
    missing_pct = (missing / len(main_data)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    if len(missing_df) > 0:
        print(missing_df.head(15).to_string())
    else:
        print("No missing values!")
    
    print("\n" + "=" * 80)
    print("8. SAMPLE DATA")
    print("=" * 80)
    print("\nFirst few rows of main data:")
    print(main_data.head(3).to_string())
    
    print("\n" + "=" * 80)
    print("EXPLORATION COMPLETE")
    print("=" * 80)
    
except FileNotFoundError as e:
    print(f"Error: File not found - {e}")
    print(f"Looking for files in: {data_dir}")
    print(f"Files in data/raw: {list(data_dir.glob('*'))}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
