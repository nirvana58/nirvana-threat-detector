"""
PCAP to CSV Converter for Network Threat Detection
Converts PCAP files to CSV format for analysis
"""

import pandas as pd
from pathlib import Path

try:
    from scapy.all import rdpcap, IP, TCP, UDP, ICMP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

def convert_pcap_to_csv(pcap_file: str, output_file: str = None) -> str:
    """
    Convert PCAP file to CSV format for threat analysis
    
    Args:
        pcap_file: Path to PCAP file
        output_file: Path to output CSV file (optional)
    
    Returns:
        Path to generated CSV file
    """
    if not SCAPY_AVAILABLE:
        raise ImportError("Scapy is required for PCAP analysis. Install with: pip install scapy")
    
    print(f"Reading PCAP file: {pcap_file}")
    
    # Read PCAP file
    packets = rdpcap(pcap_file)
    print(f"Loaded {len(packets)} packets")
    
    # Extract features from packets
    data = []
    
    for i, packet in enumerate(packets):
        if IP in packet:
            ip_layer = packet[IP]
            
            # Basic packet info
            record = {
                'timestamp': float(packet.time),
                'src_ip': ip_layer.src,
                'dst_ip': ip_layer.dst,
                'protocol': ip_layer.proto,
                'packet_size': len(packet),
                'ttl': ip_layer.ttl if hasattr(ip_layer, 'ttl') else 0
            }
            
            # TCP specific
            if TCP in packet:
                tcp_layer = packet[TCP]
                record.update({
                    'src_port': tcp_layer.sport,
                    'dst_port': tcp_layer.dport,
                    'protocol': 'TCP',
                    'tcp_flags': tcp_layer.flags,
                    'has_syn': 1 if tcp_layer.flags & 0x02 else 0,
                    'has_ack': 1 if tcp_layer.flags & 0x10 else 0,
                    'has_fin': 1 if tcp_layer.flags & 0x01 else 0,
                    'has_rst': 1 if tcp_layer.flags & 0x04 else 0,
                    'has_psh': 1 if tcp_layer.flags & 0x08 else 0,
                    'window_size': tcp_layer.window,
                    'seq_num': tcp_layer.seq,
                    'ack_num': tcp_layer.ack
                })
            
            # UDP specific
            elif UDP in packet:
                udp_layer = packet[UDP]
                record.update({
                    'src_port': udp_layer.sport,
                    'dst_port': udp_layer.dport,
                    'protocol': 'UDP',
                    'tcp_flags': 0,
                    'has_syn': 0,
                    'has_ack': 0,
                    'has_fin': 0,
                    'has_rst': 0,
                    'has_psh': 0,
                    'window_size': 0,
                    'seq_num': 0,
                    'ack_num': 0
                })
            
            # ICMP specific
            elif ICMP in packet:
                record.update({
                    'src_port': 0,
                    'dst_port': 0,
                    'protocol': 'ICMP',
                    'tcp_flags': 0,
                    'has_syn': 0,
                    'has_ack': 0,
                    'has_fin': 0,
                    'has_rst': 0,
                    'has_psh': 0,
                    'window_size': 0,
                    'seq_num': 0,
                    'ack_num': 0
                })
            
            # Other protocols
            else:
                record.update({
                    'src_port': 0,
                    'dst_port': 0,
                    'tcp_flags': 0,
                    'has_syn': 0,
                    'has_ack': 0,
                    'has_fin': 0,
                    'has_rst': 0,
                    'has_psh': 0,
                    'window_size': 0,
                    'seq_num': 0,
                    'ack_num': 0
                })
            
            # Calculate payload size
            record['payload_size'] = len(bytes(packet)) - len(packet[IP])
            
            data.append(record)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add derived features
    print("Adding derived features...")
    
    # Calculate duration and bytes per connection
    if len(df) > 0:
        # Group by connection (src_ip, dst_ip, src_port, dst_port)
        df['connection_id'] = (df['src_ip'] + ':' + df['src_port'].astype(str) + '-' + 
                               df['dst_ip'] + ':' + df['dst_port'].astype(str))
        
        # Calculate statistics per connection
        conn_stats = df.groupby('connection_id').agg({
            'timestamp': ['min', 'max', 'count'],
            'packet_size': ['sum', 'mean'],
            'payload_size': ['sum', 'mean']
        }).reset_index()
        
        conn_stats.columns = ['connection_id', 'start_time', 'end_time', 'packet_count',
                             'total_bytes', 'avg_packet_size', 'total_payload', 'avg_payload']
        
        conn_stats['duration'] = conn_stats['end_time'] - conn_stats['start_time']
        conn_stats['packets_per_second'] = conn_stats['packet_count'] / (conn_stats['duration'] + 0.001)
        conn_stats['bytes_per_second'] = conn_stats['total_bytes'] / (conn_stats['duration'] + 0.001)
        
        # Merge back to main dataframe
        df = df.merge(conn_stats[['connection_id', 'duration', 'packet_count', 
                                   'packets_per_second', 'bytes_per_second']], 
                      on='connection_id', how='left')
    
    # Add port category
    def categorize_port(port):
        if port == 0:
            return 'unknown'
        elif port < 1024:
            return 'well_known'
        elif port < 49152:
            return 'registered'
        else:
            return 'dynamic'
    
    df['port_category'] = df['dst_port'].apply(categorize_port)
    
    # Select relevant columns for ML
    ml_columns = [
        'src_port', 'dst_port', 'protocol', 'packet_size', 'payload_size',
        'ttl', 'has_syn', 'has_ack', 'has_fin', 'has_rst', 'has_psh',
        'window_size', 'duration', 'packet_count', 'packets_per_second',
        'bytes_per_second', 'port_category'
    ]
    
    # Keep only existing columns
    ml_columns = [col for col in ml_columns if col in df.columns]
    df_ml = df[ml_columns].copy()
    
    # Fill any remaining NaN values
    df_ml = df_ml.fillna(0)
    
    # Determine output file
    if output_file is None:
        pcap_path = Path(pcap_file)
        output_file = str(pcap_path.parent / f"{pcap_path.stem}_converted.csv")
    
    # Save to CSV
    df_ml.to_csv(output_file, index=False)
    
    print(f"✓ Converted {len(df_ml)} packets to CSV")
    print(f"✓ Saved to: {output_file}")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total packets: {len(df_ml)}")
    print(f"  Unique connections: {df['connection_id'].nunique() if 'connection_id' in df.columns else 'N/A'}")
    print(f"  Protocol distribution:")
    for proto, count in df['protocol'].value_counts().items():
        print(f"    {proto}: {count}")
    
    return output_file


def is_pcap_file(filename: str) -> bool:
    """Check if file is a PCAP file"""
    return filename.lower().endswith(('.pcap', '.pcapng', '.cap'))
