# 🔧 Troubleshooting Guide

Common issues and solutions for Network Threat Detector Client.

---

## 🚨 Connection Issues

### "Cannot connect to API"

**Symptoms:**
```
✗ Cannot connect: HTTPSConnectionPool... Max retries exceeded
```

**Solutions:**

1. **Check Internet Connection**
   ```bash
   ping 8.8.8.8
   curl https://google.com
   ```

2. **Verify API URL**
   ```bash
   cat ~/.ntd-client/config.json
   # Should show: {"api_url": "https://..."}
   
   # Test manually
   curl https://your-api-url/health
   ```

3. **Test Connection**
   ```bash
   ntd-client check
   ```

4. **Reconfigure**
   ```bash
   rm -rf ~/.ntd-client
   ntd-client --configure
   ```

---

### "Network is unreachable"

**Symptoms:**
```
[Errno 101] Network is unreachable
```

**Solutions:**

1. **WSL/Linux Networking**
   ```bash
   # Fix DNS
   sudo rm /etc/resolv.conf
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
   echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf
   
   # Restart WSL (if on Windows)
   wsl --shutdown
   # Then restart terminal
   ```

2. **Check Firewall**
   ```bash
   # Temporarily disable to test
   sudo ufw disable  # Linux
   # Or check Windows Firewall settings
   ```

3. **Use Proxy (if behind corporate proxy)**
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ntd-client check
   ```

---

## 🔐 Authentication Issues

### "Invalid API key" (401 Unauthorized)

**Symptoms:**
```
✗ Error: API returned status 401
Authentication failed
```

**Solutions:**

1. **Verify API Key**
   ```bash
   cat ~/.ntd-client/config.json
   # Check if API key starts with "ntd_"
   ```

2. **Get New API Key**
   - Contact your administrator
   - They will run: `ntd-admin create-key your-username`

3. **Reconfigure with New Key**
   ```bash
   ntd-client --configure
   # Enter new API key
   ```

4. **Check Key Status with Admin**
   - Key might be revoked or expired
   - Admin can check: `ntd-admin list-keys`

---

### "Access forbidden" (403 Forbidden)

**Symptoms:**
```
✗ Error: API returned status 403
Access denied
```

**Solutions:**

1. **API Key Disabled**
   - Contact admin to reactivate key
   - Admin runs: `ntd-admin list-keys` to check status

2. **Wrong Endpoint**
   - Ensure you're using correct API URL
   - Should be: `https://your-api.railway.app` (no trailing slash)

---

## 📊 Analysis Issues

### "ML model not available" (503 Service Unavailable)

**Symptoms:**
```
✗ Error: API returned status 503
ML model not available
```

**Solutions:**

1. **Model Not Trained**
   - Admin needs to train the model first
   - Contact admin to run: `ntd-admin train training_data.csv`

2. **Server Starting Up**
   - Wait 2-3 minutes after deployment
   - Try again: `ntd-client check`

3. **Server Issue**
   - Check with admin if server is running
   - Admin checks Railway dashboard for errors

---

### "File format error"

**Symptoms:**
```
✗ Error loading data: ...
Unsupported file format
```

**Solutions:**

1. **Check File Format**
   ```bash
   # File should be .csv or .json
   file your_data.csv
   
   # Check first few lines
   head your_data.csv
   ```

2. **Verify CSV Structure**
   ```bash
   # Should have headers in first line
   # Example:
   # src_ip,dst_ip,src_port,dst_port,protocol
   ```

3. **Required Fields**
   - See [DATA_FORMAT.md](DATA_FORMAT.md)
   - Minimum: src_ip, dst_ip, src_port, dst_port, protocol

4. **Fix Common Issues**
   ```bash
   # Remove empty lines
   sed -i '/^$/d' your_data.csv
   
   # Check for special characters
   file -bi your_data.csv
   # Should be: text/plain; charset=utf-8
   ```

---

### "LLM analysis timeout"

**Symptoms:**
```
LLM analysis taking very long or timing out
```

**Solutions:**

1. **Use Faster Model**
   ```bash
   ntd-client analyze data.csv --llm-model llama3.2:1b
   ```

2. **Disable LLM for Large Datasets**
   ```bash
   ntd-client analyze large_data.csv --no-llm
   ```

3. **Adjust Threshold**
   ```bash
   # Only analyze high-confidence threats
   ntd-client analyze data.csv --threshold 0.9
   ```

4. **Split Large Files**
   ```bash
   # Split into smaller chunks
   split -l 1000 large_file.csv chunk_
   
   # Analyze each chunk
   for file in chunk_*; do
       ntd-client analyze $file
   done
   ```

---

## 🐍 Python/Module Issues

### "ModuleNotFoundError: No module named 'requests'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solutions:**

1. **Install Dependencies**
   ```bash
   pip3 install requests pandas
   
   # Or
   pip3 install --user requests pandas
   ```

2. **Check Python Version**
   ```bash
   python3 --version
   # Should be 3.9 or higher
   ```

3. **Use Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # Or: venv\Scripts\activate  # Windows
   
   pip install requests pandas
   python ntd-client.py analyze data.csv
   ```

---

### "Command not found: ntd-client"

**Symptoms:**
```bash
ntd-client
bash: ntd-client: command not found
```

**Solutions:**

1. **Add to PATH**
   ```bash
   echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Run with Full Path**
   ```bash
   python3 ~/bin/ntd-client analyze data.csv
   ```

3. **Reinstall**
   ```bash
   curl -sSL https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main/install.sh | bash
   ```

---

## 📁 File Issues

### "File not found"

**Symptoms:**
```
✗ Error: File not found: data.csv
```

**Solutions:**

1. **Check File Path**
   ```bash
   # Use absolute path
   ntd-client analyze /full/path/to/data.csv
   
   # Or navigate to directory
   cd /path/to/data
   ntd-client analyze data.csv
   ```

2. **Verify File Exists**
   ```bash
   ls -lh data.csv
   pwd  # Show current directory
   ```

---

### "Permission denied"

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. **Check File Permissions**
   ```bash
   ls -l data.csv
   # Should be readable
   
   # Fix if needed
   chmod 644 data.csv
   ```

2. **Run Without sudo**
   ```bash
   # Don't use sudo with ntd-client
   ntd-client analyze data.csv  # Good
   # sudo ntd-client analyze data.csv  # Bad
   ```

---

## 🖥️ Platform-Specific Issues

### Windows (WSL)

**Issue: Network connectivity in WSL**

```powershell
# In PowerShell (as Administrator)
wsl --shutdown

# Reset network
netsh winsock reset
netsh int ip reset

# Restart WSL
wsl
```

**Issue: Slow performance**

```bash
# Use Windows native Python instead
/mnt/c/Python39/python.exe ntd-client.py analyze data.csv
```

---

### macOS

**Issue: SSL certificate errors**

```bash
# Install certificates
/Applications/Python\ 3.9/Install\ Certificates.command

# Or update certifi
pip3 install --upgrade certifi
```

**Issue: Command line tools**

```bash
# Install Xcode Command Line Tools
xcode-select --install
```

---

### Linux

**Issue: Python not found**

```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo yum install python3 python3-pip  # CentOS/RHEL
```

---

## 🔍 Debugging

### Enable Verbose Output

```bash
# Add debug flag (if available)
python3 ntd-client.py analyze data.csv --verbose

# Or check with Python directly
python3 -v ntd-client.py analyze data.csv
```

### Check Configuration

```bash
# View config
cat ~/.ntd-client/config.json

# View in pretty format
python3 -m json.tool ~/.ntd-client/config.json

# Test config
python3 << 'EOF'
import json
with open('/home/user/.ntd-client/config.json') as f:
    config = json.load(f)
    print("API URL:", config['api_url'])
    print("API Key:", config['api_key'][:20] + "...")
EOF
```

### Test API Manually

```bash
# Test health endpoint
curl https://your-api-url/health

# Test with API key
curl -H "Authorization: Bearer your_api_key" \
  https://your-api-url/models

# Expected response: {"models": [...], "recommended": "..."}
```

---

## 🆘 Still Having Issues?

### Collect Diagnostic Information

```bash
# Create diagnostic report
cat > diagnostic.txt << EOF
Python Version: $(python3 --version)
OS: $(uname -a)
Config: $(cat ~/.ntd-client/config.json)
Test Connection: $(curl -s https://your-api-url/health)
EOF

cat diagnostic.txt
```

### Get Help

1. **Check Existing Issues**
   - https://github.com/YOUR-USERNAME/ntd-client/issues

2. **Create New Issue**
   - Include diagnostic information
   - Steps to reproduce
   - Error messages
   - Expected vs actual behavior

3. **Community Help**
   - https://github.com/YOUR-USERNAME/ntd-client/discussions

---

## 📋 Quick Fixes Checklist

- [ ] Internet connection working
- [ ] API URL correct (ends with .railway.app)
- [ ] API key starts with "ntd_"
- [ ] Python 3.9+ installed
- [ ] Dependencies installed (requests, pandas)
- [ ] File format is CSV or JSON
- [ ] File has required fields
- [ ] Server is running (admin can check)
- [ ] Model is trained (admin responsibility)

---

## 💡 Prevention Tips

1. **Keep Dependencies Updated**
   ```bash
   pip3 install --upgrade requests pandas
   ```

2. **Test Connection First**
   ```bash
   ntd-client check
   ```

3. **Validate Data Before Analysis**
   ```bash
   head -20 data.csv  # Check format
   wc -l data.csv     # Check size
   ```

4. **Start Small**
   ```bash
   # Test with small sample first
   head -100 large_data.csv > test.csv
   ntd-client analyze test.csv
   ```

---

## 🔄 Reset Everything

If nothing works, complete reset:

```bash
# Remove configuration
rm -rf ~/.ntd-client

# Reinstall
curl -sSL https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main/install.sh | bash

# Reconfigure
ntd-client --configure

# Test
ntd-client check
```

---

**Need more help? Open an issue with diagnostic info!**

https://github.com/YOUR-USERNAME/ntd-client/issues/new