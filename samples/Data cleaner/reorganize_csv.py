"""
CSV Data Reorganizer for Network Threat Detection
Rearranges pipe-delimited network traffic data into proper CSV format
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

def rearrange_threat_data(input_file, output_file=None):
    """
    Rearrange pipe-delimited network traffic data into clean CSV format
    
    Args:
        input_file: Path to input CSV file (pipe-delimited)
        output_file: Path to output CSV file (optional)
    """
    
    print(f"Reading file: {input_file}")
    
    # Read the pipe-delimited file
    try:
        df = pd.read_csv(input_file, delimiter='|', low_memory=False)
        print(f"✓ Loaded {len(df)} rows with {len(df.columns)} columns")
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return None
    
    # Display original columns
    print("\nOriginal columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    # Clean column names (remove spaces, standardize)
    df.columns = df.columns.str.strip()
    
    # Rename columns to more standard names
    column_mapping = {
        'ts': 'timestamp',
        'uid': 'connection_id',
        'id.orig_h': 'src_ip',
        'id.orig_p': 'src_port',
        'id.resp_h': 'dst_ip',
        'id.resp_p': 'dst_port',
        'proto': 'protocol',
        'service': 'service',
        'duration': 'duration',
        'orig_bytes': 'bytes_sent',
        'resp_bytes': 'bytes_received',
        'conn_state': 'connection_state',
        'local_orig': 'local_origin',
        'local_resp': 'local_response',
        'missed_bytes': 'missed_bytes',
        'history': 'history',
        'orig_pkts': 'packets_sent',
        'orig_ip_bytes': 'ip_bytes_sent',
        'resp_pkts': 'packets_received',
        'resp_ip_bytes': 'ip_bytes_received',
        'tunnel_parents': 'tunnel_parents',
        'label': 'label',
        'detailed-label': 'detailed_label'
    }
    
    # Rename columns that exist
    df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns}, inplace=True)
    
    print("\nRenamed columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    # Handle missing values
    print("\nHandling missing values...")
    
    # Numeric columns - fill with 0
    numeric_cols = ['src_port', 'dst_port', 'duration', 'bytes_sent', 'bytes_received',
                    'missed_bytes', 'packets_sent', 'ip_bytes_sent', 'packets_received', 
                    'ip_bytes_received']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Categorical columns - fill with 'unknown'
    categorical_cols = ['protocol', 'service', 'connection_state', 'history']
    
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna('unknown')
    
    # Boolean columns - fill with False
    boolean_cols = ['local_origin', 'local_response']
    
    for col in boolean_cols:
        if col in df.columns:
            df[col] = df[col].fillna(False)
    
    # Label - fill with 'normal' if missing
    if 'label' in df.columns:
        df['label'] = df['label'].fillna('normal')
    
    if 'detailed_label' in df.columns:
        df['detailed_label'] = df['detailed_label'].fillna('Benign')
    
    # Add derived features for ML
    print("\nAdding derived features...")
    
    # Total bytes
    if 'bytes_sent' in df.columns and 'bytes_received' in df.columns:
        df['total_bytes'] = df['bytes_sent'] + df['bytes_received']
    
    # Total packets
    if 'packets_sent' in df.columns and 'packets_received' in df.columns:
        df['total_packets'] = df['packets_sent'] + df['packets_received']
    
    # Bytes per packet ratio
    if 'total_bytes' in df.columns and 'total_packets' in df.columns:
        df['bytes_per_packet'] = np.where(
            df['total_packets'] > 0,
            df['total_bytes'] / df['total_packets'],
            0
        )
    
    # Connection duration category
    if 'duration' in df.columns:
        df['duration_category'] = pd.cut(
            df['duration'],
            bins=[-np.inf, 0.1, 1, 10, np.inf],
            labels=['very_short', 'short', 'medium', 'long']
        )
    
    # Port category
    if 'dst_port' in df.columns:
        df['port_category'] = df['dst_port'].apply(categorize_port)
    
    # Extract TCP flags from history if available
    if 'history' in df.columns:
        df['has_syn'] = df['history'].str.contains('S', na=False).astype(int)
        df['has_ack'] = df['history'].str.contains('A', na=False).astype(int)
        df['has_fin'] = df['history'].str.contains('F', na=False).astype(int)
        df['has_rst'] = df['history'].str.contains('R', na=False).astype(int)
    
    # Data statistics
    print("\n" + "="*70)
    print("DATA STATISTICS")
    print("="*70)
    print(f"\nTotal records: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")
    
    if 'label' in df.columns:
        print("\nLabel distribution:")
        label_counts = df['label'].value_counts()
        for label, count in label_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {label}: {count:,} ({percentage:.2f}%)")
    
    if 'detailed_label' in df.columns:
        print("\nDetailed label distribution (top 10):")
        detailed_counts = df['detailed_label'].value_counts().head(10)
        for label, count in detailed_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {label}: {count:,} ({percentage:.2f}%)")
    
    if 'protocol' in df.columns:
        print("\nProtocol distribution:")
        proto_counts = df['protocol'].value_counts()
        for proto, count in proto_counts.items():
            print(f"  {proto}: {count:,}")
    
    # Data quality checks
    print("\n" + "="*70)
    print("DATA QUALITY")
    print("="*70)
    
    missing_summary = df.isnull().sum()
    if missing_summary.sum() > 0:
        print("\nColumns with missing values:")
        for col, count in missing_summary[missing_summary > 0].items():
            percentage = (count / len(df)) * 100
            print(f"  {col}: {count:,} ({percentage:.2f}%)")
    else:
        print("\n✓ No missing values!")
    
    # Duplicate check
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"\n⚠ Found {duplicates:,} duplicate rows")
    else:
        print("\n✓ No duplicate rows")
    
    # Select important columns for ML training
    ml_columns = [
        'src_port', 'dst_port', 'protocol', 'duration',
        'bytes_sent', 'bytes_received', 'total_bytes',
        'packets_sent', 'packets_received', 'total_packets',
        'bytes_per_packet', 'connection_state',
        'has_syn', 'has_ack', 'has_fin', 'has_rst',
        'port_category', 'label'
    ]
    
    # Keep only columns that exist
    ml_columns = [col for col in ml_columns if col in df.columns]
    df_ml = df[ml_columns].copy()
    
    # Determine output filename
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_cleaned.csv"
        output_ml_file = input_path.parent / f"{input_path.stem}_ml_ready.csv"
    else:
        output_path = Path(output_file)
        output_ml_file = output_path.parent / f"{output_path.stem}_ml_ready.csv"
    
    # Save files
    print("\n" + "="*70)
    print("SAVING FILES")
    print("="*70)
    
    try:
        # Save full cleaned dataset
        df.to_csv(output_file, index=False)
        print(f"\n✓ Full dataset saved to: {output_file}")
        print(f"  Rows: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")
        
        # Save ML-ready dataset
        df_ml.to_csv(output_ml_file, index=False)
        print(f"\n✓ ML-ready dataset saved to: {output_ml_file}")
        print(f"  Rows: {len(df_ml):,}")
        print(f"  Columns: {len(df_ml.columns)}")
        
        # Display sample
        print("\n" + "="*70)
        print("SAMPLE DATA (first 5 rows)")
        print("="*70)
        print(df_ml.head().to_string())
        
        print("\n✓ Data reorganization complete!")
        
        return df, df_ml
        
    except Exception as e:
        print(f"\n✗ Error saving files: {e}")
        return None, None


def categorize_port(port):
    """Categorize port numbers"""
    if pd.isna(port) or port == 0:
        return 'unknown'
    elif port < 1024:
        return 'well_known'
    elif port < 49152:
        return 'registered'
    else:
        return 'dynamic'


def create_sample_datasets(df, output_dir='.'):
    """Create sample datasets for testing"""
    output_dir = Path(output_dir)
    
    print("\n" + "="*70)
    print("CREATING SAMPLE DATASETS")
    print("="*70)
    
    # Small sample (100 rows)
    sample_small = df.sample(n=min(100, len(df)), random_state=42)
    sample_small_file = output_dir / "sample_small_100.csv"
    sample_small.to_csv(sample_small_file, index=False)
    print(f"\n✓ Small sample (100 rows): {sample_small_file}")
    
    # Medium sample (1000 rows)
    sample_medium = df.sample(n=min(1000, len(df)), random_state=42)
    sample_medium_file = output_dir / "sample_medium_1000.csv"
    sample_medium.to_csv(sample_medium_file, index=False)
    print(f"✓ Medium sample (1000 rows): {sample_medium_file}")
    
    # Balanced sample (equal number of each label)
    if 'label' in df.columns:
        min_count = df['label'].value_counts().min()
        sample_balanced = df.groupby('label').apply(
            lambda x: x.sample(n=min(min_count, 500), random_state=42)
        ).reset_index(drop=True)
        sample_balanced_file = output_dir / "sample_balanced.csv"
        sample_balanced.to_csv(sample_balanced_file, index=False)
        print(f"✓ Balanced sample ({len(sample_balanced)} rows): {sample_balanced_file}")


# Main execution
if __name__ == "__main__":
    print("="*70)
    print("  NETWORK THREAT DATA CSV REORGANIZER")
    print("="*70)
    print()
    
    # Get input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = input("Enter input CSV file path: ").strip()
    
    # Check if file exists
    if not Path(input_file).exists():
        print(f"✗ Error: File not found: {input_file}")
        sys.exit(1)
    
    # Get output file (optional)
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = None
    
    # Process the file
    df_full, df_ml = rearrange_threat_data(input_file, output_file)
    
    if df_full is not None and df_ml is not None:
        # Ask if user wants sample datasets
        create_samples = input("\nCreate sample datasets for testing? (y/n): ").strip().lower()
        
        if create_samples == 'y':
            output_dir = Path(input_file).parent
            create_sample_datasets(df_ml, output_dir)
        
        print("\n" + "="*70)
        print("  ALL DONE!")
        print("="*70)
        print("\nYou can now use the cleaned CSV files for:")
        print("  1. Training ML models")
        print("  2. Uploading to Railway backend")
        print("  3. Testing with CLI tools")
        print()
    else:
        print("\n✗ Data reorganization failed")
        sys.exit(1)
