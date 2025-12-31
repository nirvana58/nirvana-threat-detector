# 📊 Data Format Guide

Complete guide for preparing network traffic data for analysis.

---

## 🎯 Supported Formats

The Network Threat Detector accepts two formats:

1. **CSV** (Comma-Separated Values) - Recommended
2. **JSON** (JavaScript Object Notation)

---

## 📝 CSV Format

### Basic Structure

```csv
src_ip,dst_ip,src_port,dst_port,protocol,packet_size,duration,packets_sent,packets_received,bytes_sent,bytes_received,syn_flag,ack_flag,fin_flag,rst_flag
192.168.1.100,10.0.0.50,45123,80,TCP,1200,2.5,50,48,60000,57600,0,1,0,0
10.10.10.5,192.168.1.1,50000,22,TCP,60,0.001,1,0,60,0,1,0,0,1
```

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `src_ip` | String | Source IP address | `192.168.1.100` |
| `dst_ip` | String | Destination IP address | `10.0.0.50` |
| `src_port` | Integer | Source port number | `45123` |
| `dst_port` | Integer | Destination port number | `80` |
| `protocol` | String | Network protocol | `TCP`, `UDP`, `ICMP` |

### Recommended Fields (for better accuracy)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `packet_size` | Integer | Packet size in bytes | `1200` |
| `duration` | Float | Connection duration in seconds | `2.5` |
| `packets_sent` | Integer | Number of packets sent | `50` |
| `packets_received` | Integer | Number of packets received | `48` |
| `bytes_sent` | Integer | Total bytes sent | `60000` |
| `bytes_received` | Integer | Total bytes received | `57600` |
| `syn_flag` | Integer | TCP SYN flag (0 or 1) | `1` |
| `ack_flag` | Integer | TCP ACK flag (0 or 1) | `1` |
| `fin_flag` | Integer | TCP FIN flag (0 or 1) | `0` |
| `rst_flag` | Integer | TCP RST flag (0 or 1) | `0` |
| `psh_flag` | Integer | TCP PSH flag (0 or 1) | `0` |
| `urg_flag` | Integer | TCP URG flag (0 or 1) | `0` |

### Complete Example

```csv
src_ip,dst_ip,src_port,dst_port,protocol,packet_size,duration,packets_sent,packets_received,bytes_sent,bytes_received,syn_flag,ack_flag,fin_flag,rst_flag,psh_flag,urg_flag
192.168.1.100,10.0.0.50,45123,80,TCP,1200,2.5,50,48,60000,57600,0,1,0,0,1,0
192.168.1.101,10.0.0.50,45124,443,TCP,800,1.8,30,28,24000,22400,0,1,0,0,1,0
10.10.10.5,192.168.1.1,50000,22,TCP,60,0.001,1,0,60,0,1,0,0,1,0,0
200.200.1.1,192.168.1.50,55000,80,TCP,1500,0.01,500,0,750000,0,1,0,0,0,1,0
```

---

## 🔗 JSON Format

### Basic Structure

```json
[
  {
    "src_ip": "192.168.1.100",
    "dst_ip": "10.0.0.50",
    "src_port": 45123,
    "dst_port": 80,
    "protocol": "TCP",
    "packet_size": 1200,
    "duration": 2.5,
    "packets_sent": 50,
    "packets_received": 48,
    "bytes_sent": 60000,
    "bytes_received": 57600,
    "syn_flag": 0,
    "ack_flag": 1,
    "fin_flag": 0,
    "rst_flag": 0
  }
]
```

### Complete Example

```json
[
  {
    "src_ip": "192.168.1.100",
    "dst_ip": "10.0.0.50",
    "src_port": 45123,
    "dst_port": 80,
    "protocol": "TCP",
    "packet_size": 1200,
    "duration": 2.5,
    "packets_sent": 50,
    "packets_received": 48,
    "bytes_sent": 60000,
    "bytes_received": 57600,
    "syn_flag": 0,
    "ack_flag": 1,
    "fin_flag": 0,
    "rst_flag": 0,
    "psh_flag": 1,
    "urg_flag": 0
  },
  {
    "src_ip": "10.10.10.5",
    "dst_ip": "192.168.1.1",
    "src_port": 50000,
    "dst_port": 22,
    "protocol": "TCP",
    "packet_size": 60,
    "duration": 0.001,
    "packets_sent": 1,
    "packets_received": 0,
    "bytes_sent": 60,
    "bytes_received": 0,
    "syn_flag": 1,
    "ack_flag": 0,
    "fin_flag": 0,
    "rst_flag": 1,
    "psh_flag": 0,
    "urg_flag": 0
  }
]
```

---

## 🎨 Field Details

### IP Addresses

**Format**: IPv4 dotted decimal notation

**Valid Examples**:
- `192.168.1.100`
- `10.0.0.1`
- `172.16.0.5`
- `8.8.8.8`

**Invalid Examples**:
- `192.168.1` (incomplete)
- `256.1.1.1` (out of range)
- `example.com` (hostname, not IP)

### Ports

**Range**: 0-65535

**Common Ports**:
- `80` - HTTP
- `443` - HTTPS
- `22` - SSH
- `21` - FTP
- `25` - SMTP
- `53` - DNS
- `3306` - MySQL
- `5432` - PostgreSQL

### Protocol

**Supported Values**:
- `TCP` - Transmission Control Protocol
- `UDP` - User Datagram Protocol
- `ICMP` - Internet Control Message Protocol

**Note**: Case-insensitive (`tcp`, `TCP`, `Tcp` all work)

### TCP Flags

**Values**: `0` (not set) or `1` (set)

**Flags**:
- `syn_flag` - Synchronize (start connection)
- `ack_flag` - Acknowledgment
- `fin_flag` - Finish (close connection)
- `rst_flag` - Reset (abort connection)
- `psh_flag` - Push (send data immediately)
- `urg_flag` - Urgent

**Common Combinations**:
- SYN=1, ACK=0: Connection initiation
- SYN=1, ACK=1: Connection accepted
- FIN=1: Connection closing
- RST=1: Connection aborted
- ACK=1, PSH=1: Data transmission

---

## 📋 Data Collection Methods

### From PCAP Files

```bash
# Using tshark
tshark -r capture.pcap -T fields \
  -e ip.src -e ip.dst \
  -e tcp.srcport -e tcp.dstport \
  -e _ws.col.Protocol \
  -e frame.len \
  -e frame.time_relative \
  -E header=y -E separator=, > traffic.csv

# Using tcpdump and Python
tcpdump -w capture.pcap -i eth0
python3 pcap_to_csv.py capture.pcap traffic.csv
```

### From Network Flow Data

```bash
# From NetFlow/IPFIX
nfdump -r flows.nfcap -o csv > traffic.csv

# From sFlow
sflowtool -l > sflow.txt
python3 sflow_to_csv.py sflow.txt traffic.csv
```

### From Firewall Logs

```bash
# Parse firewall logs
cat firewall.log | awk '{print $fields}' > traffic.csv

# Using custom parser
python3 firewall_parser.py firewall.log traffic.csv
```

---

## ✅ Data Quality Guidelines

### Minimum Requirements

- **At least 100 records** for meaningful analysis
- **All required fields** must be present
- **Valid IP addresses** (IPv4 format)
- **Valid port numbers** (0-65535)
- **Consistent protocols** (TCP/UDP/ICMP)

### Best Practices

1. **Include Multiple Traffic Types**
   - Normal traffic (majority)
   - Various attack types
   - Mix of protocols

2. **Recent Data**
   - Ideally within last 30 days
   - Reflects current network patterns

3. **Complete Information**
   - All recommended fields filled
   - Accurate timestamps
   - Proper TCP flags

4. **Clean Data**
   - No missing values in required fields
   - Consistent formatting
   - Valid ranges for all fields

---

## 🚫 Common Issues

### Issue: "Missing Required Fields"

**Problem**: CSV missing required columns

**Solution**: Ensure all required fields are present
```csv
# Bad - missing protocol
src_ip,dst_ip,src_port,dst_port
192.168.1.1,10.0.0.1,1234,80

# Good - all required fields
src_ip,dst_ip,src_port,dst_port,protocol
192.168.1.1,10.0.0.1,1234,80,TCP
```

### Issue: "Invalid IP Address"

**Problem**: Malformed IP addresses

**Solution**: Use proper IPv4 format
```csv
# Bad
src_ip,dst_ip
192.168.1,10.0
example.com,server.local

# Good
src_ip,dst_ip
192.168.1.100,10.0.0.50
```

### Issue: "Port Out of Range"

**Problem**: Port numbers > 65535

**Solution**: Use valid port range (0-65535)
```csv
# Bad
src_port,dst_port
100000,70000

# Good
src_port,dst_port
45123,80
```

### Issue: "Invalid Protocol"

**Problem**: Unsupported protocol

**Solution**: Use TCP, UDP, or ICMP
```csv
# Bad
protocol
HTTP
HTTPS

# Good
protocol
TCP
UDP
```

---

## 📊 Sample Datasets

### Normal Traffic

```csv
src_ip,dst_ip,src_port,dst_port,protocol,packet_size,duration,packets_sent,packets_received,bytes_sent,bytes_received,syn_flag,ack_flag,fin_flag,rst_flag
192.168.1.100,8.8.8.8,45000,53,UDP,512,0.1,2,2,1024,1024,0,0,0,0
192.168.1.100,10.0.0.50,45001,80,TCP,1200,2.5,50,48,60000,57600,0,1,0,0
192.168.1.101,10.0.0.50,45002,443,TCP,800,3.2,40,38,32000,30400,0,1,1,0
```

### DDoS Attack

```csv
src_ip,dst_ip,src_port,dst_port,protocol,packet_size,duration,packets_sent,packets_received,bytes_sent,bytes_received,syn_flag,ack_flag,fin_flag,rst_flag
200.1.1.1,192.168.1.50,55000,80,TCP,1500,0.01,1000,0,1500000,0,1,0,0,0
200.1.1.2,192.168.1.50,55001,80,TCP,1500,0.01,1000,0,1500000,0,1,0,0,0
200.1.1.3,192.168.1.50,55002,80,TCP,1500,0.01,1000,0,1500000,0,1,0,0,0
```

### Port Scan

```csv
src_ip,dst_ip,src_port,dst_port,protocol,packet_size,duration,packets_sent,packets_received,bytes_sent,bytes_received,syn_flag,ack_flag,fin_flag,rst_flag
10.10.10.5,192.168.1.1,50000,22,TCP,60,0.001,1,0,60,0,1,0,0,1
10.10.10.5,192.168.1.1,50001,23,TCP,60,0.001,1,0,60,0,1,0,0,1
10.10.10.5,192.168.1.1,50002,80,TCP,60,0.001,1,0,60,0,1,0,0,1
```

---

## 🔄 Converting Common Formats

### From Wireshark CSV

```python
import pandas as pd

# Read Wireshark CSV
df = pd.read_csv('wireshark_export.csv')

# Map to required format
output = pd.DataFrame({
    'src_ip': df['Source'],
    'dst_ip': df['Destination'],
    'src_port': df['Source Port'],
    'dst_port': df['Destination Port'],
    'protocol': df['Protocol'],
    'packet_size': df['Length'],
    'duration': df['Time']
})

output.to_csv('traffic.csv', index=False)
```

### From Zeek/Bro Logs

```python
import pandas as pd

# Read Zeek conn.log
df = pd.read_csv('conn.log', sep='\t', comment='#', names=[
    'ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p',
    'proto', 'service', 'duration', 'orig_bytes', 'resp_bytes'
])

# Convert to required format
output = pd.DataFrame({
    'src_ip': df['id.orig_h'],
    'dst_ip': df['id.resp_h'],
    'src_port': df['id.orig_p'],
    'dst_port': df['id.resp_p'],
    'protocol': df['proto'],
    'duration': df['duration'],
    'bytes_sent': df['orig_bytes'],
    'bytes_received': df['resp_bytes']
})

output.to_csv('traffic.csv', index=False)
```

---

## 📚 Additional Resources

- **Sample Data**: See `/samples/sample_traffic.csv` in repository
- **Conversion Scripts**: Available in `/tools/` directory
- **PCAP Examples**: Check `/examples/` for sample PCAP files

---

## 💡 Tips

1. **Start Small**: Test with 100-500 records first
2. **Include Context**: Mix of normal and suspicious traffic
3. **Recent Data**: More recent = more relevant
4. **Complete Fields**: More fields = better accuracy
5. **Clean Data**: Remove duplicates and invalid entries

---

## 🆘 Need Help?

- **Issues**: https://github.com/YOUR-USERNAME/ntd-client/issues
- **Discussions**: https://github.com/YOUR-USERNAME/ntd-client/discussions
- **Examples**: Check `/samples/` directory

---

**Ready to analyze? Run:**
```bash
ntd-client analyze your_traffic.csv
```