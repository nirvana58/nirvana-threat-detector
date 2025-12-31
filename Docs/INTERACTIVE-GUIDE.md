# 🎮 Interactive Mode Guide

## 🚀 Quick Start

### Launch Interactive Mode

```bash
# Client interactive mode (default)
python3 ntd-client.py
# OR
python3 ntd-client.py interactive

# Admin interactive mode
python3 ntd-admin.py
# OR
python3 ntd-admin.py interactive
```

---

## 👥 CLIENT INTERACTIVE MENU

```
  ███████████████
███████████████████
████  👁️  ████
███████████████████
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

### Option 1: Check Connection
Tests connectivity to the API server and verifies your API key is valid.

**Output:**
```
✓ Connected to API
  Status: healthy
  ML Model: ✓ Ready
```

### Option 2: List Available Models
Shows all LLM models available for threat analysis.

**Output:**
```
ℹ Available LLM models:
  ✓ llama3.2:1b
    phi3:mini
    gemma:2b
  
  Recommended: llama3.2:1b
```

### Option 3: Analyze Network Traffic (Full Analysis)
Complete analysis with ML prediction + LLM explanations.

**Prompts:**
```
Path to network data file (CSV/JSON): training_data_test.csv
Use LLM for detailed analysis? (y/n) [y]: y
Select LLM model [llama3.2:1b]: 
Confidence threshold (0.0-1.0) [0.7]: 0.8
Save results to file? (y/n) [y]: y
```

**Shows:**
- Total records analyzed
- Threats detected
- Threat distribution
- Top 10 threats with confidence
- Detailed LLM analysis for high-confidence threats
- Saves results to JSON file

### Option 4: Quick Analysis (No LLM)
Fast ML-only analysis without LLM explanations.

**Prompts:**
```
Path to network data file (CSV/JSON): data.csv
```

**Shows:**
- ML predictions only
- Much faster (seconds vs minutes)
- Good for large datasets

### Option 5: View Configuration
Displays your current API settings.

**Output:**
```
ℹ Current Configuration:
  API URL: https://ai-threat-detector.up.railway.app
  API Key: ntd_sY8WYfYoToIHTW1lW...XrOC7EyVLmA
```

### Option 6: Exit
Closes the interactive console.

---

## 🔧 ADMIN INTERACTIVE MENU

```
╔════════════════════════════════════════════════════╗
║   AI NETWORK THREAT DETECTOR - ADMIN CONSOLE      ║
╚════════════════════════════════════════════════════╝

Admin Menu:
  [1] Check System Health
  [2] Create API Key
  [3] List API Keys
  [4] Revoke API Key
  [5] Train Model
  [6] Exit

Select option:
```

### Option 1: Check System Health
Verifies the API server is running and models are loaded.

**Output:**
```
✓ API is healthy
  ML Model: ✓ Loaded
  Preprocessor: ✓ Loaded
  Timestamp: 2024-12-27T15:53:44
```

### Option 2: Create API Key
Generate new API key for a user.

**Prompts:**
```
User ID: john_doe
Description (optional): John's development key
Rate limit [1000]: 500
```

**Output:**
```
✓ API key created successfully
═══════════════════════════════════════════════════
User ID: john_doe
API Key: ntd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Created: 2024-12-27T16:00:00
═══════════════════════════════════════════════════
⚠ Save this API key securely. It won't be shown again.
```

### Option 3: List API Keys
Shows all generated API keys and their status.

**Output:**
```
ℹ Total API keys: 3

Key (prefix)              User ID         Active   Usage    Created     
===========================================================================
ntd_sY8WYfYoToIHTW1lW... user1           ✓        25       2024-12-27  
ntd_abc123xyz456def78... john_doe        ✓        5        2024-12-27  
ntd_old_key_revoked12... alice           ✗        0        2024-12-20  
```

### Option 4: Revoke API Key
Disable an API key.

**Prompts:**
```
API key prefix to revoke: ntd_abc123
Revoke key starting with 'ntd_abc123'? (yes/no): yes
```

**Output:**
```
✓ API key revoked: ntd_abc123...
```

### Option 5: Train Model
Upload training data and train the ML model.

**Prompts:**
```
Path to training data (CSV/JSON): training_data.csv
```

**Process:**
- Uploads data to server
- Trains Random Forest model
- Shows accuracy metrics
- Saves model on server

**Output:**
```
ℹ Uploading training data: training_data.csv
✓ Model trained successfully!
  Accuracy: 97.23%
  Records: 8000
  Timestamp: 2024-12-27T16:05:00
```

### Option 6: Exit
Closes the admin console.

---

## 💡 Usage Examples

### Typical Client Workflow
```
1. Launch: python3 ntd-client.py
2. Select [1] - Verify connection
3. Select [3] - Analyze traffic
   - Enter file path
   - Choose settings
   - Review results
4. Select [6] - Exit
```

### Typical Admin Workflow
```
1. Launch: python3 ntd-admin.py
2. Select [1] - Check health
3. Select [5] - Train model (if needed)
4. Select [2] - Create user keys
5. Select [3] - Monitor usage
6. Select [6] - Exit
```

### Quick Analysis Workflow
```
1. python3 ntd-client.py
2. Select [4] - Quick analysis
3. Enter file: large_dataset.csv
4. Get results in seconds
```

---

## 🎯 Tips & Best Practices

### For Users:
- Use **Quick Analysis** [4] for large datasets (1000+ records)
- Use **Full Analysis** [3] for detailed threat investigation
- **Check Connection** [1] first if you have issues
- Results are auto-saved to `filename_results.json`

### For Admins:
- **Check Health** [1] before creating keys or training
- Train with at least 1000+ records for good accuracy
- Monitor usage with **List Keys** [3] regularly
- Use descriptive names when creating keys

---

## 🔥 Keyboard Shortcuts

While in interactive mode:
- Type number + Enter to select option
- Ctrl+C to exit immediately
- Ctrl+D to exit gracefully

---

## 📊 Sample Session Output

### Client Analysis Session
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

Select option: 3

Path to network data file (CSV/JSON): test_traffic.csv
Use LLM for detailed analysis? (y/n) [y]: y
Select LLM model [llama3.2:1b]: 
Confidence threshold (0.0-1.0) [0.7]: 
Save results to file? (y/n) [y]: y

ℹ Loading data from: test_traffic.csv
✓ Loaded 800 records
ℹ Analyzing with ML model...
ℹ Using LLM: llama3.2:1b

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
...

✓ Results saved to: test_traffic_results.json

Select option: 6

Goodbye!
```

---

## 🆘 Troubleshooting

### "Cannot connect to API"
1. Check connection: Select [1]
2. Verify config: Select [5]
3. Test manually: `curl https://api-url/health`

### "Invalid API key"
1. Contact admin for new key
2. Reconfigure: `python3 ntd-client.py --configure`

### "ML model not available"
Admin needs to train model:
1. `python3 ntd-admin.py`
2. Select [5] - Train Model

---

## 🎉 You're Ready!

Interactive mode makes it easy to:
- ✅ No need to remember commands
- ✅ Guided prompts for all inputs
- ✅ Visual menus and options
- ✅ Clear error messages
- ✅ Perfect for beginners

**Launch now:**
```bash
python3 ntd-client.py    # For users
python3 ntd-admin.py     # For admins
```

Happy threat hunting! 🛡️