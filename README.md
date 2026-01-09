# NIRVANA - AI Network Threat Detector

```
         ███╗   ██╗ ██╗ ██████╗  ██╗   ██╗  █████╗  ███╗   ██╗  █████╗ 
         ████╗  ██║ ██║ ██╔══██╗ ██║   ██║ ██╔══██╗ ████╗  ██║ ██╔══██╗
         ██╔██╗ ██║ ██║ ██████╔╝ ██║   ██║ ███████║ ██╔██╗ ██║ ███████║
         ██║╚██╗██║ ██║ ██╔══██╗ ╚██╗ ██╔╝ ██╔══██║ ██║╚██╗██║ ██╔══██║
         ██║ ╚████║ ██║ ██║  ██║  ╚████╔╝  ██║  ██║ ██║ ╚████║ ██║  ██║
         ╚═╝  ╚═══╝ ╚═╝ ╚═╝  ╚═╝   ╚═══╝   ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝  ╚═╝
                                                                          
                            ai-threat detector
```

An intelligent network threat detection system powered by Machine Learning and Large Language Models (LLMs). NIRVANA analyzes network traffic patterns to identify and explain potential security threats in real-time.

## Features

- **Advanced ML Detection**: Uses trained machine learning models to identify network threats
- **LLM-Powered Analysis**: Provides detailed, human-readable explanations of detected threats
- **Multiple LLM Support**: Compatible with Llama, Phi, Gemma, and other Ollama models
- **Flexible Input**: Supports both CSV and JSON network data formats
- **Interactive CLI**: User-friendly command-line interface with real-time feedback
- **Cloud-Ready**: Designed for deployment on Railway, AWS, or any cloud platform
- **API-First Design**: RESTful API for easy integration with existing systems

## Architecture

NIRVANA consists of two main components:

1. **API Server** (FastAPI + ML/LLM)
   - Handles threat detection using scikit-learn models
   - Integrates with Ollama for LLM analysis
   - Provides RESTful endpoints for analysis

2. **Client CLI** (Python)
   - User-friendly command-line interface
   - Supports batch analysis and interactive mode
   - Configurable threat detection parameters

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Network data in CSV or JSON format

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nirvana-threat-detector.git
cd nirvana-threat-detector
```

2. Run the setup script:
```bash
chmod +x run_ntd.sh
./run_ntd.sh
```

The script will automatically:
- Check Python installation
- Install all required dependencies
- Launch the client in interactive mode

### Configuration

Configure your API credentials:

```bash
./run_ntd.sh --configure
```

Or manually set environment variables:

```bash
export NTD_API_URL='https://ai-threat-detector.up.railway.app'
export NTD_API_KEY='your-api-key-here'
```

## Usage

### Interactive Mode

Launch the interactive menu:

```bash
./run_ntd.sh
# or
python3 ntd-client.py interactive
```

### Command-Line Usage

**Check API connection:**
```bash
python3 ntd-client.py check
```

**List available LLM models:**
```bash
python3 ntd-client.py models
```

**Analyze network traffic:**
```bash
python3 ntd-client.py analyze network_data.csv
```

**Quick analysis (ML only, no LLM):**
```bash
python3 ntd-client.py analyze network_data.csv --no-llm
```

**Custom LLM model and threshold:**
```bash
python3 ntd-client.py analyze data.csv --llm-model phi3:mini --threshold 0.8
```

## Data Format

### CSV Format

Your network data should include columns such as:

```csv
src_ip,dst_ip,src_port,dst_port,protocol,packet_size,duration,flags
192.168.1.100,10.0.0.5,54321,80,TCP,1024,0.5,SYN
```

### JSON Format

```json
[
  {
    "src_ip": "192.168.1.100",
    "dst_ip": "10.0.0.5",
    "src_port": 54321,
    "dst_port": 80,
    "protocol": "TCP",
    "packet_size": 1024,
    "duration": 0.5,
    "flags": "SYN"
  }
]
```

## API Reference

### Health Check
```
GET /health
```

### List Models
```
GET /models
Authorization: Bearer YOUR_API_KEY
```

### Analyze Traffic
```
POST /analyze
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "network_data": [...],
  "use_llm": true,
  "llm_model": "llama3.2:1b",
  "confidence_threshold": 0.7
}
```

## Configuration Files

NIRVANA stores configuration in `~/.ntd-client/config.json`:

```json
{
  "api_url": "https://your-api.railway.app",
  "api_key": "ntd_your_api_key_here"
}
```

## Dependencies

### Core Dependencies
- `fastapi` - Web framework for the API server
- `pandas` - Data manipulation and analysis
- `scikit-learn` - Machine learning models
- `ollama` - LLM integration
- `requests` - HTTP client for API calls

### Full Dependencies
See `requirements.txt` for complete list.

## Supported LLM Models

NIRVANA supports any Ollama-compatible model:

- **Llama 3.2** (1B, 3B) - Fast and efficient
- **Phi-3** - Microsoft's compact model
- **Gemma** - Google's lightweight model
- **Mistral** - High-performance model
- **Custom models** - Any Ollama-compatible model

## Development

### Project Structure

```
nirvana-threat-detector/
├── ntd-client.py       # Client CLI application
├── requirements.txt    # Python dependencies
├── run_ntd.sh         # Setup and launcher script
├── README.md          # This file
└── SETUP.md           # Detailed setup guide
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Troubleshooting

### Connection Issues

If you can't connect to the API:

1. Verify your API URL is correct
2. Check your API key is valid
3. Ensure the API server is running
4. Check firewall settings

### Missing Dependencies

If you get import errors:

```bash
pip install -r requirements.txt
```

### LLM Model Issues

If LLM analysis fails:

1. Verify Ollama is running on the server
2. Check the model is installed: `ollama list`
3. Try a different model with `--llm-model`

## Performance

- **ML Detection**: < 1 second for 1000 records
- **LLM Analysis**: 2-5 seconds per threat (depends on model)
- **Recommended**: Use `--no-llm` for large datasets, then analyze specific threats

## Security

- All API calls require valid API keys
- Keys are stored securely in `~/.ntd-client/config.json`
- Never share your API key publicly
- Use environment variables in production

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions:

- GitHub Issues: [Report a bug](https://github.com/nirvana58/ai-threat-detector/issues)
- Documentation: See SETUP.md for detailed setup instructions
- Email: laksmeesha.s.999@gmail.com

## Roadmap

- [ ] Real-time network monitoring
- [ ] Web dashboard interface
- [ ] Custom ML model training
- [ ] Integration with SIEM systems
- [ ] Multi-user support with role-based access
- [ ] Automated threat response actions

## Acknowledgments

Built with:
- FastAPI - Modern web framework
- scikit-learn - Machine learning library
- Ollama - Local LLM runtime
- Railway - Cloud deployment platform

---

**Made with ❤️ for network security professionals**
