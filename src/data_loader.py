"""
Data loading utilities for Ethiopia Financial Inclusion Forecasting
"""

import pandas as pd
import os
from pathlib import Path


def get_data_path(filename):
    """Get the path to a data file in the raw data directory"""
    project_root = Path(__file__).parent.parent
    return project_root / "data" / "raw" / filename


def load_unified_data():
    """
    Load the unified financial inclusion dataset.
    
    Returns:
        tuple: (main_data DataFrame, impact_links DataFrame)
    """
    filepath = get_data_path("ethiopia_fi_unified_data.xlsx")
    
    # Load the main data sheet
    main_data = pd.read_excel(filepath, sheet_name=0)
    
    # Load the impact_links sheet if it exists
    try:
        impact_links = pd.read_excel(filepath, sheet_name=1)
    except:
        # If only one sheet, impact_links might be in the main data
        impact_links = main_data[main_data['record_type'] == 'impact_link'].copy()
        main_data = main_data[main_data['record_type'] != 'impact_link'].copy()
    
    return main_data, impact_links


def load_reference_codes():
    """Load the reference codes for valid field values"""
    filepath = get_data_path("reference_codes.xlsx")
    return pd.read_excel(filepath)


def load_additional_data_guide():
    """Load the additional data points guide"""
    filepath = get_data_path("Additional Data Points Guide.xlsx")
    return pd.read_excel(filepath, sheet_name=None)  # Load all sheets


if __name__ == "__main__":
    # Test loading
    print("Loading unified data...")
    main_data, impact_links = load_unified_data()
    print(f"Main data shape: {main_data.shape}")
    print(f"Impact links shape: {impact_links.shape}")
    
    print("\nLoading reference codes...")
    ref_codes = load_reference_codes()
    print(f"Reference codes shape: {ref_codes.shape}")
    
    print("\nMain data columns:", main_data.columns.tolist())
    print("\nMain data record types:", main_data['record_type'].value_counts())
