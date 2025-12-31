# 🛡️ Network Threat Detector - Client Tool

**Analyze network traffic for security threats using AI-powered cloud analysis**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Detect DDoS attacks, port scans, SQL injections, brute force attempts, and more with one simple command.

---

## ✨ Features

- 🤖 **AI-Powered Analysis** - Machine Learning + Large Language Models
- 🚀 **Easy to Use** - Interactive menu or simple commands
- ⚡ **Fast Results** - Get threat analysis in seconds
- 📊 **Detailed Reports** - ML predictions + LLM explanations
- 🔐 **Secure** - API key authentication
- 💻 **Cross-Platform** - Works on Linux, macOS, Windows

---

## 🚀 Quick Start

### One-Command Installation

```bash
curl -sSL https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main/install.sh | bash
```

### Manual Installation

```bash
# Download the client
curl -o ntd-client.py https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main/ntd-client.py
chmod +x ntd-client.py

# Install dependencies
pip3 install requests pandas

# Configure (get API key from your admin)
python3 ntd-client.py --configure

# Start analyzing!
python3 ntd-client.py
```

---

## 📖 Usage

### Interactive Mode (Recommended)

```bash
python3 ntd-client.py
```

**Menu:**
```
  ███████████████
AI THREAT DETECTOR

Client Menu:
  [1] Check Connection
  [2] List Available Models
  [3] Analyze Network Traffic
  [4] Quick Analysis (No LLM)
  [5] View Configuration
  [6] Exit

Select option:
```

### Command Line Mode

```bash
# Test connection
python3 ntd-client.py check

# List available LLM models
python3 ntd-client.py models

# Analyze with full LLM analysis
python3 ntd-client.py analyze network_traffic.csv

# Quick analysis (ML only, faster)
python3 ntd-client.py analyze network_traffic.csv --no-llm

# Use different LLM model
python3 ntd-client.py analyze traffic.csv --llm-model phi3:mini

# Adjust confidence threshold
python3 ntd-client.py analyze traffic.csv --threshold 0.9
```

---

## 📊 Example Output

```
======================================================================
ANALYSIS RESULTS
======================================================================

Total Records:    800
Threats Detected: 302
Avg Confidence:   99.87%

Threat Distribution:
  normal            498 (62.3%)
  ddos               91 (11.4%)
  brute_force        82 (10.2%)
  port_scan          77 (9.6%)
  sql_injection      52 (6.5%)

Top 10 Threats (by confidence):
Record     Threat Type          Confidence
=============================================
342        ddos                     100.00%
156        port_scan                 99.98%
789        brute_force               99.95%

======================================================================
DETAILED LLM ANALYSIS
======================================================================

Record #342 - ddos (100.00%)
────────────────────────────────────────────────────────────────────
THREAT ASSESSMENT: Yes
THREAT TYPE: Distributed Denial of Service (DDoS) Attack
EXPLANATION: Extremely high volume of packets from single source
targeting specific port. Classic flooding behavior detected.
RECOMMENDED ACTION: Block source IP immediately, enable rate 
limiting, deploy DDoS mitigation
RISK LEVEL: Critical

✓ Results saved to: network_traffic_results.json
```

---

## 📁 Data Format

Your network traffic data should be in CSV or JSON format:

### CSV Format

```csv
src_ip,dst_ip,src_port,dst_port,protocol,packet_size,duration,packets_sent,packets_received,bytes_sent,bytes_received,syn_flag,ack_flag,fin_flag,rst_flag
192.168.1.100,10.0.0.50,45123,80,TCP,1200,2.5,50,48,60000,57600,0,1,0,0
10.10.10.5,192.168.1.1,50000,22,TCP,60,0.001,1,0,60,0,1,0,0,1
```

### JSON Format

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

**Minimum Required Fields:**
- Source/Destination IPs
- Ports
- Protocol
- Packet information
- TCP flags

---

## ⚙️ Configuration

### Initial Setup

```bash
python3 ntd-client.py --configure
```

**You'll need:**
1. **API URL** - The server address (e.g., `https://ai-threat-detector.up.railway.app`)
2. **API Key** - Provided by your admin (format: `ntd_xxxxx...`)

### Configuration File

Config is stored in `~/.ntd-client/config.json`:

```json
{
  "api_url": "https://ai-threat-detector.up.railway.app",
  "api_key": "ntd_your_api_key_here"
}
```

### Environment Variables

Alternative to config file:

```bash
export NTD_API_URL="https://ai-threat-detector.up.railway.app"
export NTD_API_KEY="ntd_your_api_key_here"

python3 ntd-client.py analyze traffic.csv
```

---

## 🎯 Use Cases

### Security Operations Center (SOC)

```bash
# Daily traffic analysis
python3 ntd-client.py analyze daily_traffic.csv

# Monitor results
cat daily_traffic_results.json | grep -i "critical"
```

### Incident Response

```bash
# Quick scan for threats
python3 ntd-client.py analyze suspicious_traffic.csv --no-llm

# Deep analysis of confirmed threats
python3 ntd-client.py analyze confirmed_threats.csv --threshold 0.95
```

### Automated Monitoring

```bash
#!/bin/bash
# cron job: 0 */6 * * *

# Export network logs
tcpdump -i eth0 -w /tmp/traffic.pcap

# Convert and analyze
python3 convert_pcap.py /tmp/traffic.pcap traffic.csv
python3 ntd-client.py analyze traffic.csv --no-llm

# Alert on threats
THREATS=$(cat traffic_results.json | jq '.threats_detected')
if [ "$THREATS" -gt 0 ]; then
    echo "⚠️ $THREATS threats detected!" | mail -s "Threat Alert" admin@company.com
fi
```

---

## 🔧 Advanced Options

### Analysis Options

```bash
# Full analysis with LLM
python3 ntd-client.py analyze data.csv

# ML only (fast, good for large datasets)
python3 ntd-client.py analyze data.csv --no-llm

# Use specific LLM model
python3 ntd-client.py analyze data.csv --llm-model phi3:mini
python3 ntd-client.py analyze data.csv --llm-model gemma:2b

# Adjust confidence threshold (0.0-1.0)
python3 ntd-client.py analyze data.csv --threshold 0.8

# Don't save results file
python3 ntd-client.py analyze data.csv --no-save
```

### Available LLM Models

- **llama3.2:1b** (default) - Fast, good accuracy
- **phi3:mini** - Balanced speed and quality
- **gemma:2b** - Highest accuracy, slower

---

## 🐛 Troubleshooting

### "Cannot connect to API"

```bash
# Test connection
python3 ntd-client.py check

# Verify URL
cat ~/.ntd-client/config.json

# Test manually
curl https://your-api-url/health
```

### "Invalid API key"

```bash
# Get new key from admin
# Then reconfigure
python3 ntd-client.py --configure
```

### "ML model not available"

The admin needs to train the model first. Contact your admin.

### "Module not found"

```bash
# Install dependencies
pip3 install requests pandas
```

---

## 📚 Documentation

- **Interactive Mode Guide** - [INTERACTIVE_GUIDE.md](INTERACTIVE_GUIDE.md)
- **Data Format Guide** - [DATA_FORMAT.md](DATA_FORMAT.md)
- **Troubleshooting** - [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **FAQ** - [FAQ.md](FAQ.md)

---

## 🔐 Security & Privacy

- All communication is encrypted (HTTPS)
- API key required for all requests
- Your data is processed and not stored on the server
- Results are saved locally only

---

## 💡 Tips & Best Practices

### For Better Accuracy

- Provide complete network traffic data (all fields)
- Use recent data (within last 30 days)
- Include both normal and suspicious traffic
- Minimum 100 records for meaningful analysis

### For Better Performance

- Use `--no-llm` for large datasets (1000+ records)
- Use full LLM analysis for detailed investigation
- Set higher confidence threshold (0.8+) to focus on certain threats
- Save results and review offline

### For Automation

- Use environment variables instead of config file
- Parse JSON results programmatically
- Set up cron jobs for regular scanning
- Integrate with your SIEM/alerting system

---

## 📞 Support

- 📖 [Documentation](https://github.com/YOUR-USERNAME/ntd-client/wiki)
- 🐛 [Report Issues](https://github.com/YOUR-USERNAME/ntd-client/issues)
- 💬 [Discussions](https://github.com/YOUR-USERNAME/ntd-client/discussions)

---

## 🤝 Contributing

Found a bug? Want a feature? Contributions welcome!

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

Powered by:
- Machine Learning (Scikit-learn)
- Large Language Models (Ollama)
- FastAPI backend

---

## 📊 System Requirements

- **Python**: 3.9 or higher
- **RAM**: 100MB minimum
- **Disk**: 50MB
- **Network**: Internet connection required
- **OS**: Linux, macOS, Windows (WSL)

---

## 🎓 Getting Started Tutorial

### Step 1: Get API Access

Contact your admin to get:
- API URL
- API Key

### Step 2: Install

```bash
curl -o ntd-client.py https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main/ntd-client.py
pip3 install requests pandas
```

### Step 3: Configure

```bash
python3 ntd-client.py --configure
# Enter API URL
# Enter API Key
```

### Step 4: Test

```bash
python3 ntd-client.py check
# Should show: ✓ Connected to API
```

### Step 5: Analyze

```bash
# Download sample data
curl -o sample.csv https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main/samples/sample_traffic.csv

# Analyze
python3 ntd-client.py analyze sample.csv
```

---

<div align="center">

**🛡️ Stay secure with AI-powered threat detection**

[⬆ Back to Top](#️-network-threat-detector---client-tool)

</div>