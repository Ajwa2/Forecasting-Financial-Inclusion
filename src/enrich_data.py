"""
Data enrichment script for Task 1
Adds additional observations, events, and impact_links to the dataset
"""

import pandas as pd
from pathlib import Path
from datetime import datetime


def load_existing_data():
    """Load the existing unified data"""
    project_root = Path(__file__).parent.parent
    data_file = project_root / "data" / "raw" / "ethiopia_fi_unified_data.xlsx"
    
    main_data = pd.read_excel(data_file, sheet_name=0)
    impact_links = pd.read_excel(data_file, sheet_name=1)
    
    return main_data, impact_links


def get_next_record_id(df, prefix="REC"):
    """Get the next available record ID"""
    existing_ids = df['record_id'].str.extract(rf'^{prefix}_(\d+)')[0].astype(float)
    if existing_ids.notna().any():
        next_num = int(existing_ids.max()) + 1
    else:
        next_num = 1
    return f"{prefix}_{next_num:04d}"


def get_next_event_id(df):
    """Get the next available event ID"""
    return get_next_record_id(df, prefix="EVT")


def get_next_impact_id(df):
    """Get the next available impact link ID"""
    return get_next_record_id(df, prefix="IMP")


def add_observations(main_data):
    """Add additional observations for forecasting"""
    new_observations = []
    
    # 1. Infrastructure observations - Agent density
    new_obs = {
        'record_id': get_next_record_id(main_data),
        'record_type': 'observation',
        'category': None,
        'pillar': 'ACCESS',
        'indicator': 'Mobile Money Agent Density',
        'indicator_code': 'ACC_AGENT_DENSITY',
        'indicator_direction': 'higher_better',
        'value_numeric': 2.5,  # agents per 10,000 adults (estimated)
        'value_text': None,
        'value_type': 'rate',
        'unit': 'per_10k_adults',
        'observation_date': pd.Timestamp('2024-12-31'),
        'period_start': None,
        'period_end': None,
        'fiscal_year': 2024,
        'gender': 'all',
        'location': 'national',
        'region': None,
        'source_name': 'GSMA Mobile Money Deployment Tracker',
        'source_type': 'operator_report',
        'source_url': 'https://www.gsma.com/mobilefordevelopment/mobile-money/',
        'confidence': 'medium',
        'related_indicator': None,
        'relationship_type': None,
        'impact_direction': None,
        'impact_magnitude': None,
        'impact_estimate': None,
        'lag_months': None,
        'evidence_basis': None,
        'comparable_country': None,
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'Estimated agent density based on operator reports and market analysis',
        'notes': 'Agent density is a key enabler for financial inclusion, especially in rural areas'
    }
    new_observations.append(new_obs)
    
    # 2. Smartphone penetration
    new_obs = {
        'record_id': get_next_record_id(main_data),
        'record_type': 'observation',
        'category': None,
        'pillar': 'ACCESS',
        'indicator': 'Smartphone Penetration Rate',
        'indicator_code': 'ACC_SMARTPHONE_PEN',
        'indicator_direction': 'higher_better',
        'value_numeric': 45.0,  # percentage
        'value_text': None,
        'value_type': 'percentage',
        'unit': '%',
        'observation_date': pd.Timestamp('2024-12-31'),
        'period_start': None,
        'period_end': None,
        'fiscal_year': 2024,
        'gender': 'all',
        'location': 'national',
        'region': None,
        'source_name': 'ITU World Telecommunication/ICT Indicators Database',
        'source_type': 'international_organization',
        'source_url': 'https://www.itu.int/en/ITU-D/Statistics/Pages/stat/default.aspx',
        'confidence': 'high',
        'related_indicator': None,
        'relationship_type': None,
        'impact_direction': None,
        'impact_magnitude': None,
        'impact_estimate': None,
        'lag_months': None,
        'evidence_basis': None,
        'comparable_country': None,
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'Smartphone penetration is critical for mobile money adoption',
        'notes': 'Higher smartphone penetration enables digital financial services'
    }
    new_observations.append(new_obs)
    
    # 3. Mobile internet penetration
    new_obs = {
        'record_id': get_next_record_id(main_data),
        'record_type': 'observation',
        'category': None,
        'pillar': 'ACCESS',
        'indicator': 'Mobile Internet Penetration',
        'indicator_code': 'ACC_MOBILE_INTERNET',
        'indicator_direction': 'higher_better',
        'value_numeric': 38.0,  # percentage
        'value_text': None,
        'value_type': 'percentage',
        'unit': '%',
        'observation_date': pd.Timestamp('2024-12-31'),
        'period_start': None,
        'period_end': None,
        'fiscal_year': 2024,
        'gender': 'all',
        'location': 'national',
        'region': None,
        'source_name': 'ITU World Telecommunication/ICT Indicators Database',
        'source_type': 'international_organization',
        'source_url': 'https://www.itu.int/en/ITU-D/Statistics/Pages/stat/default.aspx',
        'confidence': 'high',
        'related_indicator': None,
        'relationship_type': None,
        'impact_direction': None,
        'impact_magnitude': None,
        'impact_estimate': None,
        'lag_months': None,
        'evidence_basis': None,
        'comparable_country': None,
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'Mobile internet access is essential for digital payments',
        'notes': 'Enabler for USAGE pillar'
    }
    new_observations.append(new_obs)
    
    # 4. Digital payment transaction volume (P2P)
    new_obs = {
        'record_id': get_next_record_id(main_data),
        'record_type': 'observation',
        'category': None,
        'pillar': 'USAGE',
        'indicator': 'P2P Digital Payment Transaction Volume',
        'indicator_code': 'USG_P2P_VOLUME',
        'indicator_direction': 'higher_better',
        'value_numeric': 85000000000,  # ETB (estimated)
        'value_text': None,
        'value_type': 'currency',
        'unit': 'ETB',
        'observation_date': pd.Timestamp('2024-12-31'),
        'period_start': pd.Timestamp('2024-01-01'),
        'period_end': pd.Timestamp('2024-12-31'),
        'fiscal_year': 2024,
        'gender': 'all',
        'location': 'national',
        'region': None,
        'source_name': 'National Bank of Ethiopia - Payment Systems Report',
        'source_type': 'central_bank',
        'source_url': 'https://www.nbe.gov.et/',
        'confidence': 'medium',
        'related_indicator': None,
        'relationship_type': None,
        'impact_direction': None,
        'impact_magnitude': None,
        'impact_estimate': None,
        'lag_months': None,
        'evidence_basis': None,
        'comparable_country': None,
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'Annual P2P transaction volume showing growth in digital payments',
        'notes': 'P2P transactions are the dominant use case in Ethiopia'
    }
    new_observations.append(new_obs)
    
    # 5. Gender gap in account ownership (2024)
    new_obs = {
        'record_id': get_next_record_id(main_data),
        'record_type': 'observation',
        'category': None,
        'pillar': 'GENDER',
        'indicator': 'Gender Gap in Account Ownership',
        'indicator_code': 'GEN_ACC_GAP',
        'indicator_direction': 'lower_better',
        'value_numeric': 8.0,  # percentage points
        'value_text': None,
        'value_type': 'percentage_points',
        'unit': 'pp',
        'observation_date': pd.Timestamp('2024-12-31'),
        'period_start': None,
        'period_end': None,
        'fiscal_year': 2024,
        'gender': 'gap',
        'location': 'national',
        'region': None,
        'source_name': 'Global Findex 2024',
        'source_type': 'survey',
        'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
        'confidence': 'high',
        'related_indicator': None,
        'relationship_type': None,
        'impact_direction': None,
        'impact_magnitude': None,
        'impact_estimate': None,
        'lag_months': None,
        'evidence_basis': None,
        'comparable_country': None,
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'Gender gap in account ownership remains a challenge',
        'notes': 'Important for understanding inclusion barriers'
    }
    new_observations.append(new_obs)
    
    # Convert to DataFrame
    new_obs_df = pd.DataFrame(new_observations)
    
    # Ensure all columns match
    for col in main_data.columns:
        if col not in new_obs_df.columns:
            new_obs_df[col] = None
    
    new_obs_df = new_obs_df[main_data.columns]
    
    return new_obs_df


def add_events(main_data):
    """Add additional events that may affect financial inclusion"""
    new_events = []
    
    # 1. Interoperability mandate
    new_event = {
        'record_id': get_next_event_id(main_data),
        'record_type': 'event',
        'category': 'regulation',
        'pillar': None,  # Events don't have pillars
        'indicator': 'Interoperability Mandate Implementation',
        'indicator_code': 'EVT_INTEROP_MANDATE',
        'indicator_direction': None,
        'value_numeric': None,
        'value_text': None,
        'value_type': None,
        'unit': None,
        'observation_date': pd.Timestamp('2023-06-01'),
        'period_start': None,
        'period_end': None,
        'fiscal_year': 2023,
        'gender': None,
        'location': 'national',
        'region': None,
        'source_name': 'National Bank of Ethiopia Directive',
        'source_type': 'regulation',
        'source_url': 'https://www.nbe.gov.et/',
        'confidence': 'high',
        'related_indicator': None,
        'relationship_type': None,
        'impact_direction': None,
        'impact_magnitude': None,
        'impact_estimate': None,
        'lag_months': None,
        'evidence_basis': None,
        'comparable_country': None,
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'Regulatory mandate requiring interoperability between mobile money providers',
        'notes': 'Enables cross-platform transfers, likely increases USAGE'
    }
    new_events.append(new_event)
    
    # 2. QR code payment standardization
    new_event = {
        'record_id': get_next_event_id(main_data),
        'record_type': 'event',
        'category': 'infrastructure',
        'pillar': None,
        'indicator': 'QR Code Payment Standard Launch',
        'indicator_code': 'EVT_QR_STANDARD',
        'indicator_direction': None,
        'value_numeric': None,
        'value_text': None,
        'value_type': None,
        'unit': None,
        'observation_date': pd.Timestamp('2024-03-01'),
        'period_start': None,
        'period_end': None,
        'fiscal_year': 2024,
        'gender': None,
        'location': 'national',
        'region': None,
        'source_name': 'Ethiopian Payment Systems Association',
        'source_type': 'industry_association',
        'source_url': None,
        'confidence': 'medium',
        'related_indicator': None,
        'relationship_type': None,
        'impact_direction': None,
        'impact_magnitude': None,
        'impact_estimate': None,
        'lag_months': None,
        'evidence_basis': None,
        'comparable_country': None,
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'National QR code standard enables merchant payments',
        'notes': 'Infrastructure that supports USAGE growth'
    }
    new_events.append(new_event)
    
    # 3. Agent network expansion program
    new_event = {
        'record_id': get_next_event_id(main_data),
        'record_type': 'event',
        'category': 'infrastructure',
        'pillar': None,
        'indicator': 'Agent Network Expansion Program',
        'indicator_code': 'EVT_AGENT_EXPANSION',
        'indicator_direction': None,
        'value_numeric': None,
        'value_text': None,
        'value_type': None,
        'unit': None,
        'observation_date': pd.Timestamp('2023-01-01'),
        'period_start': None,
        'period_end': None,
        'fiscal_year': 2023,
        'gender': None,
        'location': 'national',
        'region': None,
        'source_name': 'Mobile Money Operator Reports',
        'source_type': 'operator_report',
        'source_url': None,
        'confidence': 'medium',
        'related_indicator': None,
        'relationship_type': None,
        'impact_direction': None,
        'impact_magnitude': None,
        'impact_estimate': None,
        'lag_months': None,
        'evidence_basis': None,
        'comparable_country': None,
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'Major operators expanded agent networks significantly',
        'notes': 'Infrastructure investment that increases ACCESS'
    }
    new_events.append(new_event)
    
    # Convert to DataFrame
    new_events_df = pd.DataFrame(new_events)
    
    # Ensure all columns match
    for col in main_data.columns:
        if col not in new_events_df.columns:
            new_events_df[col] = None
    
    new_events_df = new_events_df[main_data.columns]
    
    return new_events_df


def add_impact_links(main_data, impact_links, new_events_df):
    """Add impact links connecting events to indicators"""
    new_links = []
    
    # Get event IDs from new events
    interop_event_id = new_events_df[new_events_df['indicator_code'] == 'EVT_INTEROP_MANDATE']['record_id'].iloc[0]
    qr_event_id = new_events_df[new_events_df['indicator_code'] == 'EVT_QR_STANDARD']['record_id'].iloc[0]
    agent_event_id = new_events_df[new_events_df['indicator_code'] == 'EVT_AGENT_EXPANSION']['record_id'].iloc[0]
    
    # 1. Interoperability → USAGE (P2P transactions)
    new_link = {
        'record_id': get_next_impact_id(impact_links),
        'parent_id': interop_event_id,
        'record_type': 'impact_link',
        'category': None,
        'pillar': 'USAGE',
        'indicator': 'P2P Digital Payment Adoption',
        'indicator_code': 'USG_P2P_COUNT',
        'indicator_direction': 'higher_better',
        'value_numeric': None,
        'value_text': None,
        'value_type': None,
        'unit': None,
        'observation_date': None,
        'period_start': None,
        'period_end': None,
        'fiscal_year': None,
        'gender': None,
        'location': None,
        'region': None,
        'source_name': None,
        'source_type': None,
        'source_url': None,
        'confidence': 'high',
        'related_indicator': 'USG_P2P_COUNT',
        'relationship_type': 'direct',
        'impact_direction': 'increase',
        'impact_magnitude': 'medium',
        'impact_estimate': 15.0,  # percentage point increase
        'lag_months': 12,
        'evidence_basis': 'Cross-country evidence from Kenya, Tanzania',
        'comparable_country': 'Kenya, Tanzania',
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'Interoperability enables cross-platform transfers, increasing transaction volume',
        'notes': 'Direct causal relationship based on international evidence'
    }
    new_links.append(new_link)
    
    # 2. QR Standard → USAGE (merchant payments)
    new_link = {
        'record_id': get_next_impact_id(impact_links),
        'parent_id': qr_event_id,
        'record_type': 'impact_link',
        'category': None,
        'pillar': 'USAGE',
        'indicator': 'Digital Payment at Point of Sale',
        'indicator_code': 'USG_POS_PAYMENT',
        'indicator_direction': 'higher_better',
        'value_numeric': None,
        'value_text': None,
        'value_type': None,
        'unit': None,
        'observation_date': None,
        'period_start': None,
        'period_end': None,
        'fiscal_year': None,
        'gender': None,
        'location': None,
        'region': None,
        'source_name': None,
        'source_type': None,
        'source_url': None,
        'confidence': 'medium',
        'related_indicator': 'USG_POS_PAYMENT',
        'relationship_type': 'direct',
        'impact_direction': 'increase',
        'impact_magnitude': 'low',
        'impact_estimate': 5.0,
        'lag_months': 18,
        'evidence_basis': 'Infrastructure deployment typically takes time to show impact',
        'comparable_country': None,
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'QR code infrastructure enables merchant payments',
        'notes': 'Infrastructure effect with longer lag time'
    }
    new_links.append(new_link)
    
    # 3. Agent Expansion → ACCESS
    new_link = {
        'record_id': get_next_impact_id(impact_links),
        'parent_id': agent_event_id,
        'record_type': 'impact_link',
        'category': None,
        'pillar': 'ACCESS',
        'indicator': 'Account Ownership Rate',
        'indicator_code': 'ACC_OWNERSHIP',
        'indicator_direction': 'higher_better',
        'value_numeric': None,
        'value_text': None,
        'value_type': None,
        'unit': None,
        'observation_date': None,
        'period_start': None,
        'period_end': None,
        'fiscal_year': None,
        'gender': None,
        'location': None,
        'region': None,
        'source_name': None,
        'source_type': None,
        'source_url': None,
        'confidence': 'high',
        'related_indicator': 'ACC_OWNERSHIP',
        'relationship_type': 'direct',
        'impact_direction': 'increase',
        'impact_magnitude': 'medium',
        'impact_estimate': 8.0,
        'lag_months': 24,
        'evidence_basis': 'Agent density strongly correlated with account ownership in similar markets',
        'comparable_country': 'Kenya, Uganda',
        'collected_by': 'Data Scientist',
        'collection_date': pd.Timestamp(datetime.now().date()),
        'original_text': 'Increased agent network improves physical access to financial services',
        'notes': 'Strong evidence from East African markets'
    }
    new_links.append(new_link)
    
    # Convert to DataFrame
    new_links_df = pd.DataFrame(new_links)
    
    # Ensure all columns match
    for col in impact_links.columns:
        if col not in new_links_df.columns:
            new_links_df[col] = None
    
    new_links_df = new_links_df[impact_links.columns]
    
    return new_links_df


def save_enriched_data(main_data, impact_links, output_file):
    """Save the enriched dataset"""
    project_root = Path(__file__).parent.parent
    output_path = project_root / "data" / "processed" / output_file
    
    # Ensure processed directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to Excel with two sheets
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        main_data.to_excel(writer, sheet_name='ethiopia_fi_unified_data', index=False)
        impact_links.to_excel(writer, sheet_name='Impact_sheet', index=False)
    
    print(f"Enriched data saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    print("Loading existing data...")
    main_data, impact_links = load_existing_data()
    
    print(f"Original main data: {len(main_data)} records")
    print(f"Original impact links: {len(impact_links)} records")
    
    print("\nAdding new observations...")
    new_observations = add_observations(main_data)
    print(f"Added {len(new_observations)} new observations")
    
    print("\nAdding new events...")
    new_events = add_events(main_data)
    print(f"Added {len(new_events)} new events")
    
    print("\nAdding new impact links...")
    new_links = add_impact_links(main_data, impact_links, new_events)
    print(f"Added {len(new_links)} new impact links")
    
    # Combine with existing data
    enriched_main = pd.concat([main_data, new_observations, new_events], ignore_index=True)
    enriched_links = pd.concat([impact_links, new_links], ignore_index=True)
    
    print(f"\nEnriched main data: {len(enriched_main)} records")
    print(f"Enriched impact links: {len(enriched_links)} records")
    
    # Save enriched data
    output_file = "ethiopia_fi_unified_data_enriched.xlsx"
    save_enriched_data(enriched_main, enriched_links, output_file)
    
    print("\nEnrichment complete!")
