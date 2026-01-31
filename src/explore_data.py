"""
Data exploration script for Task 1: Data Exploration and Enrichment
"""

import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import load_unified_data, load_reference_codes, load_additional_data_guide


def explore_schema(df, impact_links, ref_codes):
    """Explore the schema and structure of the data"""
    print("=" * 80)
    print("SCHEMA EXPLORATION")
    print("=" * 80)
    
    print("\n1. MAIN DATA STRUCTURE")
    print("-" * 80)
    print(f"Total records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nData types:\n{df.dtypes}")
    
    print("\n2. RECORD TYPE DISTRIBUTION")
    print("-" * 80)
    print(df['record_type'].value_counts())
    
    print("\n3. PILLAR DISTRIBUTION (for observations)")
    print("-" * 80)
    obs_df = df[df['record_type'] == 'observation']
    if 'pillar' in obs_df.columns:
        print(obs_df['pillar'].value_counts())
    
    print("\n4. SOURCE TYPE DISTRIBUTION")
    print("-" * 80)
    if 'source_type' in df.columns:
        print(df['source_type'].value_counts())
    
    print("\n5. CONFIDENCE LEVEL DISTRIBUTION")
    print("-" * 80)
    if 'confidence' in df.columns:
        print(df['confidence'].value_counts())
    
    print("\n6. TEMPORAL RANGE")
    print("-" * 80)
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    for col in date_cols:
        if df[col].notna().any():
            print(f"\n{col}:")
            print(f"  Min: {df[col].min()}")
            print(f"  Max: {df[col].max()}")
            print(f"  Unique values: {df[col].nunique()}")
    
    print("\n7. INDICATORS COVERAGE")
    print("-" * 80)
    if 'indicator_code' in df.columns:
        indicators = df[df['indicator_code'].notna()]['indicator_code'].unique()
        print(f"Total unique indicators: {len(indicators)}")
        print("\nIndicators by record type:")
        for rt in df['record_type'].unique():
            rt_indicators = df[(df['record_type'] == rt) & (df['indicator_code'].notna())]['indicator_code'].unique()
            print(f"  {rt}: {len(rt_indicators)} indicators")
            if len(rt_indicators) <= 20:
                for ind in sorted(rt_indicators):
                    print(f"    - {ind}")
    
    print("\n8. EVENTS CATALOG")
    print("-" * 80)
    events = df[df['record_type'] == 'event']
    if len(events) > 0:
        print(f"Total events: {len(events)}")
        if 'category' in events.columns:
            print("\nEvents by category:")
            print(events['category'].value_counts())
        print("\nEvent details:")
        event_cols = ['record_id', 'indicator', 'category', 'observation_date'] if 'indicator' in events.columns else events.columns[:10]
        print(events[event_cols].to_string())
    
    print("\n9. IMPACT LINKS")
    print("-" * 80)
    if len(impact_links) > 0:
        print(f"Total impact links: {len(impact_links)}")
        if 'pillar' in impact_links.columns:
            print("\nImpact links by pillar:")
            print(impact_links['pillar'].value_counts())
        if 'impact_direction' in impact_links.columns:
            print("\nImpact direction:")
            print(impact_links['impact_direction'].value_counts())
    
    print("\n10. REFERENCE CODES")
    print("-" * 80)
    if ref_codes is not None and len(ref_codes) > 0:
        print(f"Total reference code entries: {len(ref_codes)}")
        print("\nReference code structure:")
        print(ref_codes.head(10).to_string())


def analyze_data_quality(df, impact_links):
    """Analyze data quality and completeness"""
    print("\n" + "=" * 80)
    print("DATA QUALITY ANALYSIS")
    print("=" * 80)
    
    print("\n1. MISSING VALUES")
    print("-" * 80)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    print(missing_df.to_string())
    
    print("\n2. DUPLICATE RECORDS")
    print("-" * 80)
    if 'record_id' in df.columns:
        duplicates = df[df.duplicated(subset=['record_id'], keep=False)]
        print(f"Duplicate record_ids: {len(duplicates)}")
        if len(duplicates) > 0:
            print(duplicates[['record_id', 'record_type']].to_string())


def identify_enrichment_opportunities(df, impact_links, ref_codes):
    """Identify opportunities for data enrichment"""
    print("\n" + "=" * 80)
    print("ENRICHMENT OPPORTUNITIES")
    print("=" * 80)
    
    print("\n1. TEMPORAL GAPS")
    print("-" * 80)
    obs_df = df[df['record_type'] == 'observation']
    if 'observation_date' in obs_df.columns:
        obs_df['year'] = pd.to_datetime(obs_df['observation_date'], errors='coerce').dt.year
        years = sorted(obs_df['year'].dropna().unique())
        print(f"Years with observations: {years}")
        if len(years) > 1:
            gaps = []
            for i in range(len(years) - 1):
                if years[i+1] - years[i] > 1:
                    gaps.append(f"{int(years[i])} - {int(years[i+1])}")
            if gaps:
                print(f"Temporal gaps: {', '.join(gaps)}")
    
    print("\n2. MISSING INDICATORS")
    print("-" * 80)
    print("Consider adding observations for:")
    print("  - Disaggregated data (gender, region, urban/rural)")
    print("  - Infrastructure metrics (agent density, POS terminals, ATM density)")
    print("  - Transaction volumes and values")
    print("  - Active vs. registered accounts")
    
    print("\n3. MISSING EVENTS")
    print("-" * 80)
    print("Consider adding events for:")
    print("  - Regulatory changes (KYC requirements, interoperability rules)")
    print("  - Infrastructure investments (network expansion, agent network growth)")
    print("  - Economic events (inflation, currency changes)")
    print("  - Partnership announcements")
    
    print("\n4. MISSING IMPACT LINKS")
    print("-" * 80)
    events = df[df['record_type'] == 'event']
    event_ids = set(events['record_id'].unique()) if 'record_id' in events.columns else set()
    linked_events = set(impact_links['parent_id'].unique()) if 'parent_id' in impact_links.columns else set()
    unlinked_events = event_ids - linked_events
    if unlinked_events:
        print(f"Events without impact links: {len(unlinked_events)}")
        unlinked = events[events['record_id'].isin(unlinked_events)]
        print(unlinked[['record_id', 'indicator', 'category']].to_string())


if __name__ == "__main__":
    print("Loading data...")
    main_data, impact_links = load_unified_data()
    ref_codes = load_reference_codes()
    
    print("\n" + "=" * 80)
    print("ETHIOPIA FINANCIAL INCLUSION DATA EXPLORATION")
    print("=" * 80)
    
    # Explore schema
    explore_schema(main_data, impact_links, ref_codes)
    
    # Analyze data quality
    analyze_data_quality(main_data, impact_links)
    
    # Identify enrichment opportunities
    identify_enrichment_opportunities(main_data, impact_links, ref_codes)
    
    print("\n" + "=" * 80)
    print("EXPLORATION COMPLETE")
    print("=" * 80)
