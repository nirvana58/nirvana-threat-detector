# ❓ Frequently Asked Questions (FAQ)

Common questions about Network Threat Detector Client.

---

## 🎯 General Questions

### What is the Network Threat Detector?

A command-line tool that analyzes network traffic for security threats using AI (Machine Learning + Large Language Models). It connects to a cloud-based backend for analysis.

### Do I need to install a server?

No! The server is already running. You only install the client tool on your computer.

### Is this tool free?

The client tool is open source and free. Server access requires an API key from your administrator (costs depend on your organization's setup).

### What types of threats can it detect?

- **DDoS attacks** - Distributed Denial of Service
- **Port scans** - Network reconnaissance
- **Brute force attacks** - Password guessing attempts
- **SQL injection** - Database attack attempts
- **Abnormal traffic patterns**

### How accurate is the detection?

The ML model achieves 97%+ accuracy on test data. Actual accuracy depends on your data quality and threat types.

---

## 🚀 Getting Started

### How do I get an API key?

Contact your system administrator. They will:
1. Give you the generated API key (starts with `ntd_`)


### Can I try it without an API key?

No. The client requires a valid API key to connect to the analysis server.

### How long does installation take?

About 1-2 minutes using the one-click installer.

---

## 📊 Data & Analysis

### What data format do I need?

CSV or JSON files with network traffic information. See [DATA_FORMAT.md](DATA_FORMAT.md) for details.

**Required fields:**
- Source/destination IPs
- Source/destination ports
- Protocol
- Traffic statistics

### Where do I get network traffic data?

Common sources:
- Firewall logs
- Network flow data (NetFlow, sFlow)
- PCAP files from tcpdump/Wireshark
- IDS/IPS systems (Snort, Suricata)
- SIEM platforms

### How much data should I analyze?

- **Minimum**: 100 records for meaningful results
- **Recommended**: 500-1000 records
- **Maximum**: Unlimited, but use `--no-llm` for 10,000+ records

### How long does analysis take?

- **ML only**: Seconds (100-1000 records/second)
- **With LLM**: 2-5 seconds per threat analyzed
- **Large datasets**: Minutes (use `--no-llm` for faster results)

### Can I analyze real-time traffic?

Not directly, but you can:
1. Capture traffic periodically (every 5-15 minutes)
2. Export to CSV
3. Analyze with the client
4. Automate with cron/scheduled tasks

---

## 🔧 Usage Questions

### What's the difference between ML and LLM analysis?

| Feature | ML Only (`--no-llm`) | ML + LLM |
|---------|---------------------|----------|
| Speed | Fast (seconds) | Slower (minutes) |
| Output | Threat labels + confidence | Labels + detailed explanations |
| Use case | Large datasets, quick scans | Detailed investigation |
| Cost | Lower API usage | Higher API usage |

### Which LLM model should I use?

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| `llama3.2:1b` | Fast | Good | Default, general use |
| `phi3:mini` | Medium | Better | Detailed analysis |
| `gemma:2b` | Slower | Best | Critical threats |

### Can I analyze the same data twice?

Yes! Each analysis is independent. You can:
- Reanalyze with different settings
- Use different LLM models
- Adjust confidence thresholds

### Do I need to install anything else?

Only Python 3.9+ and two packages:
```bash
pip3 install requests pandas
```

---

## 🔐 Security & Privacy

### Is my data stored on the server?

No. Your data is:
1. Sent to server for analysis
2. Processed immediately
3. Results returned to you
4. Not stored on server

### Can others see my analysis results?

No. Results are:
- Sent only to you
- Saved locally on your computer
- Not shared with other users

### Is the connection secure?

Yes. All communication uses:
- HTTPS encryption
- API key authentication
- Secure Railway.app infrastructure

### What happens to my API key?

Your API key:
- Is stored locally in `~/.ntd-client/config.json`
- Is never logged or exposed
- Can be revoked by admin at any time
- Should be kept secret (like a password)

### Can my admin see what I analyze?

Admins can see:
- API key usage count (how many times you've used it)
- Whether your key is active

Admins **cannot** see:
- What data you analyzed
- Your analysis results
- File contents

---

## 💻 Technical Questions

### What operating systems are supported?

- **Linux** ✅ (Ubuntu, Debian, CentOS, etc.)
- **macOS** ✅
- **Windows** ✅ (via WSL or native Python)

### What Python version do I need?

Python 3.9 or higher. Check with:
```bash
python3 --version
```

### Can I use it in a Docker container?

Yes! Example Dockerfile:
```dockerfile
FROM python:3.11-slim
RUN pip install requests pandas
COPY ntd-client.py /usr/local/bin/ntd-client
RUN chmod +x /usr/local/bin/ntd-client
CMD ["ntd-client"]
```

### Can I integrate it with my scripts?

Yes! Parse the JSON output:
```bash
ntd-client analyze data.csv

# Parse results
threats=$(cat data_results.json | jq '.threats_detected')
if [ "$threats" -gt 0 ]; then
    echo "Threats found!"
fi
```

### Does it work offline?

No. It requires internet connection to:
- Connect to the API server
- Send data for analysis
- Receive results

### Can I run it on a schedule?

Yes! Use cron (Linux/Mac):
```bash
# Edit crontab
crontab -e

# Add line (run every 6 hours)
0 */6 * * * ntd-client analyze /path/to/traffic.csv
```

Or Task Scheduler (Windows).

---

## 🛠️ Customization

### Can I change the API URL?

Yes:
```bash
ntd-client --configure
# Enter new API URL
```

### Can I use environment variables instead of config file?

Yes:
```bash
export NTD_API_URL="https://your-api.railway.app"
export NTD_API_KEY="ntd_your_key_here"
ntd-client analyze data.csv
```

### Can I change confidence threshold?

Yes:
```bash
# Only show threats with 90%+ confidence
ntd-client analyze data.csv --threshold 0.9
```

### Can I disable saving results?

Yes:
```bash
ntd-client analyze data.csv --no-save
```

---

## 🐛 Troubleshooting

### Why can't I connect?

Common causes:
1. Wrong API URL
2. Invalid API key
3. Network/firewall issues
4. Server is down

**Solution**: Run `ntd-client check` and see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Why is it slow?

Possible reasons:
1. Using LLM analysis (2-5 seconds per threat)
2. Large dataset
3. Slow network connection

**Solution**: Use `--no-llm` for faster analysis

### Why do I get "ML model not available"?

The admin hasn't trained the model yet. Contact them to run:
```bash
ntd-admin train training_data.csv
```

### Where are results saved?

Same directory as input file:
- Input: `traffic.csv`
- Output: `traffic_results.json`

### Can I export results to CSV?

Results are JSON by default. Convert with:
```bash
# Using jq
cat results.json | jq -r '.predictions[] | [.record_id, .prediction, .confidence] | @csv' > results.csv

# Using Python
python3 << EOF
import json, csv
data = json.load(open('results.json'))
with open('results.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['record_id', 'prediction', 'confidence'])
    for p in data['predictions']:
        writer.writerow([p['record_id'], p['prediction'], p['confidence']])
EOF
```

---

## 📈 Performance

### How many records can I analyze at once?

- **With LLM**: 500-1000 records (practical limit)
- **Without LLM**: 100,000+ records (limited by file size and memory)

### How do I analyze very large files?

```bash
# Option 1: Disable LLM
ntd-client analyze large_file.csv --no-llm

# Option 2: Split file
split -l 1000 large_file.csv chunk_
for file in chunk_*; do
    ntd-client analyze "$file"
done

# Option 3: Sample data
head -1000 large_file.csv > sample.csv
ntd-client analyze sample.csv
```

### Does it use a lot of bandwidth?

Bandwidth usage depends on:
- File size (your data is uploaded)
- Number of analyses
- LLM usage (more bandwidth)

Typical: 1-10 MB per analysis

---

## 💰 Cost & Limits

### Is there a usage limit?

Limits depend on your API key:
- Default: 1000 requests per hour
- Your admin can adjust this

### What happens if I exceed limits?

You'll receive an error. Contact your admin to:
- Increase your limit
- Get additional API key

### Can I share my API key?

**No!** Each user should have their own key:
- Easier to track usage
- Can be revoked independently
- Better security

---

## 🔄 Updates

### How do I update the client?

```bash
# Reinstall to get latest version
curl -sSL https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main/install.sh | bash
```

### How do I know if there's a new version?

Check the GitHub repository:
- https://github.com/YOUR-USERNAME/ntd-client/releases

### Will updates break my config?

No. Your configuration (`~/.ntd-client/config.json`) is preserved during updates.

---

## 🤝 Contributing

### Can I contribute to the project?

Yes! Contributions welcome:
1. Fork the repository
2. Make improvements
3. Submit pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md)

### I found a bug. What should I do?

1. Check [existing issues](https://github.com/YOUR-USERNAME/ntd-client/issues)
2. Create new issue with details
3. Include steps to reproduce

### Can I request features?

Yes! Create a feature request:
- https://github.com/YOUR-USERNAME/ntd-client/issues/new
- Label it as "enhancement"

---

## 📚 Learning More

### Where can I learn about network threats?

Resources:
- OWASP Top 10
- MITRE ATT&CK Framework
- SANS Reading Room
- Network security courses (Coursera, Udemy)

### How does the ML model work?

- **Algorithm**: Random Forest Classifier
- **Training**: Supervised learning on labeled network data
- **Features**: IP addresses, ports, protocols, traffic patterns
- **Output**: Threat classification + confidence score

### What LLM models are used?

- **llama3.2** - Meta's Llama model (1B parameters)
- **phi3** - Microsoft's Phi model
- **gemma** - Google's Gemma model

All running via Ollama on the server.

---

## 🎓 Best Practices

### How often should I analyze traffic?

Depends on your needs:
- **High security**: Every 15-30 minutes
- **Normal**: Daily
- **Low risk**: Weekly

### Should I always use LLM analysis?

Use LLM when:
- Investigating specific incidents
- Need detailed explanations
- Analyzing small datasets (<1000 records)

Skip LLM when:
- Quick scans
- Large datasets (>10,000 records)
- Regular automated checks

### How do I improve accuracy?

1. **Provide complete data** - All recommended fields
2. **Include context** - Mix of normal and suspicious traffic
3. **Recent data** - Within last 30 days
4. **Clean data** - No duplicates or errors

---

## 📞 Getting Help

### Where can I get help?

1. **Documentation**: Check all docs in `/docs/`
2. **Issues**: https://github.com/YOUR-USERNAME/ntd-client/issues
3. **Discussions**: https://github.com/YOUR-USERNAME/ntd-client/discussions
4. **Admin**: Contact your organization's admin

### How do I report security issues?

**DO NOT** create public issues for security vulnerabilities.

Email: security@yourdomain.com

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Install
curl -sSL https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main/install.sh | bash

# Configure
ntd-client --configure

# Test
ntd-client check

# Analyze
ntd-client analyze traffic.csv

# Help
ntd-client --help
```

### Essential Files

- Config: `~/.ntd-client/config.json`
- Results: `filename_results.json`
- Docs: https://github.com/YOUR-USERNAME/ntd-client

---

**Still have questions? Ask in [Discussions](https://github.com/YOUR-USERNAME/ntd-client/discussions)!**
