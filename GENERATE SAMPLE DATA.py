#!/usr/bin/env python3
"""
Generate sample network traffic data for training and testing
"""

import pandas as pd
import numpy as np
import random
import argparse
from pathlib import Path

def generate_ip():
    """Generate random IP address"""
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def generate_normal_traffic(n=1000):
    """Generate normal network traffic"""
    data = []
    protocols = ['TCP', 'UDP', 'ICMP']
    common_ports = [80, 443, 53, 22, 21, 25, 110, 143, 3306, 5432]
    
    for _ in range(n):
        data.append({
            'src_ip': generate_ip(),
            'dst_ip': generate_ip(),
            'src_port': random.randint(1024, 65535),
            'dst_port': random.choice(common_ports),
            'protocol': random.choice(protocols),
            'packet_size': random.randint(64, 1500),
            'duration': round(random.uniform(0.001, 10.0), 3),
            'packets_sent': random.randint(1, 200),
            'packets_received': random.randint(1, 200),
            'bytes_sent': random.randint(100, 50000),
            'bytes_received': random.randint(100, 50000),
            'syn_flag': random.choice([0, 1]),
            'ack_flag': random.choice([0, 1]),
            'fin_flag': random.choice([0, 1]),
            'rst_flag': 0,
            'psh_flag': random.choice([0, 1]),
            'urg_flag': 0,
            'label': 'normal'
        })
    return data

def generate_port_scan(n=200):
    """Generate port scanning attack traffic"""
    data = []
    attacker_ips = [generate_ip() for _ in range(random.randint(1, 5))]
    target_ip = generate_ip()
    
    for _ in range(n):
        attacker = random.choice(attacker_ips)
        data.append({
            'src_ip': attacker,
            'dst_ip': target_ip,
            'src_port': random.randint(40000, 50000),
            'dst_port': random.randint(1, 65535),
            'protocol': 'TCP',
            'packet_size': 60,
            'duration': round(random.uniform(0.001, 0.01), 3),
            'packets_sent': 1,
            'packets_received': random.choice([0, 1]),
            'bytes_sent': 60,
            'bytes_received': random.choice([0, 40]),
            'syn_flag': 1,
            'ack_flag': 0,
            'fin_flag': 0,
            'rst_flag': random.choice([0, 1]),
            'psh_flag': 0,
            'urg_flag': 0,
            'label': 'port_scan'
        })
    return data

def generate_ddos(n=300):
    """Generate DDoS attack traffic"""
    data = []
    target_ip = generate_ip()
    target_port = random.choice([80, 443, 8080])
    
    for _ in range(n):
        data.append({
            'src_ip': generate_ip(),  # Different source IPs
            'dst_ip': target_ip,
            'src_port': random.randint(1024, 65535),
            'dst_port': target_port,
            'protocol': random.choice(['TCP', 'UDP', 'ICMP']),
            'packet_size': random.randint(500, 1500),
            'duration': round(random.uniform(0.001, 0.1), 3),
            'packets_sent': random.randint(100, 2000),
            'packets_received': random.choice([0, 1, 2]),
            'bytes_sent': random.randint(50000, 1000000),
            'bytes_received': random.choice([0, 100]),
            'syn_flag': random.choice([0, 1]),
            'ack_flag': 0,
            'fin_flag': 0,
            'rst_flag': 0,
            'psh_flag': random.choice([0, 1]),
            'urg_flag': 0,
            'label': 'ddos'
        })
    return data

def generate_sql_injection(n=100):
    """Generate SQL injection attempt traffic"""
    data = []
    attacker = generate_ip()
    target = generate_ip()
    
    for _ in range(n):
        data.append({
            'src_ip': attacker,
            'dst_ip': target,
            'src_port': random.randint(40000, 60000),
            'dst_port': random.choice([80, 443, 8080]),
            'protocol': 'TCP',
            'packet_size': random.randint(200, 1000),
            'duration': round(random.uniform(0.1, 2.0), 3),
            'packets_sent': random.randint(5, 20),
            'packets_received': random.randint(1, 10),
            'bytes_sent': random.randint(500, 5000),
            'bytes_received': random.randint(100, 2000),
            'syn_flag': 0,
            'ack_flag': 1,
            'fin_flag': 0,
            'rst_flag': 0,
            'psh_flag': 1,
            'urg_flag': 0,
            'label': 'sql_injection'
        })
    return data

def generate_brute_force(n=150):
    """Generate brute force login attack traffic"""
    data = []
    attacker = generate_ip()
    target = generate_ip()
    
    for _ in range(n):
        data.append({
            'src_ip': attacker,
            'dst_ip': target,
            'src_port': random.randint(40000, 60000),
            'dst_port': random.choice([22, 23, 21, 3389]),
            'protocol': 'TCP',
            'packet_size': random.randint(100, 300),
            'duration': round(random.uniform(0.1, 1.0), 3),
            'packets_sent': random.randint(5, 15),
            'packets_received': random.randint(3, 10),
            'bytes_sent': random.randint(200, 1500),
            'bytes_received': random.randint(100, 1000),
            'syn_flag': 0,
            'ack_flag': 1,
            'fin_flag': 0,
            'rst_flag': random.choice([0, 1]),
            'psh_flag': 1,
            'urg_flag': 0,
            'label': 'brute_force'
        })
    return data

def main():
    parser = argparse.ArgumentParser(description='Generate sample network traffic data')
    parser.add_argument('--output', '-o', default='network_traffic_sample.csv',
                       help='Output filename')
    parser.add_argument('--normal', type=int, default=5000,
                       help='Number of normal traffic records')
    parser.add_argument('--port-scan', type=int, default=800,
                       help='Number of port scan records')
    parser.add_argument('--ddos', type=int, default=1000,
                       help='Number of DDoS records')
    parser.add_argument('--sql-injection', type=int, default=500,
                       help='Number of SQL injection records')
    parser.add_argument('--brute-force', type=int, default=700,
                       help='Number of brute force records')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv',
                       help='Output format')
    
    args = parser.parse_args()
    
    print("Generating sample network traffic data...")
    print(f"  Normal traffic: {args.normal}")
    print(f"  Port scans: {args.port_scan}")
    print(f"  DDoS attacks: {args.ddos}")
    print(f"  SQL injections: {args.sql_injection}")
    print(f"  Brute force: {args.brute_force}")
    
    # Generate data
    all_data = []
    all_data.extend(generate_normal_traffic(args.normal))
    all_data.extend(generate_port_scan(args.port_scan))
    all_data.extend(generate_ddos(args.ddos))
    all_data.extend(generate_sql_injection(args.sql_injection))
    all_data.extend(generate_brute_force(args.brute_force))
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save
    if args.format == 'csv':
        df.to_csv(args.output, index=False)
    else:
        df.to_json(args.output, orient='records', indent=2)
    
    print(f"\n✓ Generated {len(df)} records")
    print(f"✓ Saved to: {args.output}")
    
    # Statistics
    print("\nLabel Distribution:")
    print(df['label'].value_counts())
    
    print("\nSample statistics:")
    print(df.describe())
    
    # Create test file (10% of data)
    test_size = int(len(df) * 0.1)
    test_df = df.sample(n=test_size, random_state=42)
    test_output = Path(args.output).stem + '_test.' + args.format
    
    if args.format == 'csv':
        test_df.to_csv(test_output, index=False)
    else:
        test_df.to_json(test_output, orient='records', indent=2)
    
    print(f"\n✓ Test file created: {test_output} ({test_size} records)")

if __name__ == "__main__":
    main()