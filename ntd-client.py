#!/usr/bin/env python3
"""
Network Threat Detector - User CLI Client
Analyze network traffic for threats using cloud-based ML + LLM
"""

import requests
import json
import sys
import argparse
from typing import List, Dict, Any, Optional
from pathlib import Path
import os
import pandas as pd

# Import the CSV reorganizer
try:
    from reorganize_csv import rearrange_threat_data, create_sample_datasets
    CSV_REORGANIZER_AVAILABLE = True
except ImportError:
    CSV_REORGANIZER_AVAILABLE = False
    print("Warning: reorganize_csv module not found. CSV reorganization features disabled.")

class Colors:
    RED ='\033[38;5;196m'
    RED2 ='\033[38;5;203m'
    PINK ='\033[38;5;210m'
    LIGHT_PINK ='\033[38;5;217m'
    WHITE ='\033[38;5;231m'
    CYAN ='\033[38;5;51m'
    YELLOW ='\033[38;5;226m'
    RESET ='\033[0m'
    NC = '\033[0m'
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'

class ThreatDetectorClient:
    def __init__(self, api_url: str, api_key: str):
        # Ensure proper URL format
        if not api_url.startswith('http'):
            api_url = f"https://{api_url}"
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _print_banner(self):
        print()
        print()
        print(f"        {Colors.RED} ███╗   ██╗ ██╗ ██████╗  ██╗   ██╗  █████╗  ███╗   ██╗  █████╗ {Colors.RESET}")
        print(f"        {Colors.RED} ████╗  ██║ ██║ ██╔══██╗ ██║   ██║ ██╔══██╗ ████╗  ██║ ██╔══██╗{Colors.RESET}")
        print(f"        {Colors.RED2} ██╔██╗ ██║ ██║ ██████╔╝ ██║   ██║ ███████║ ██╔██╗ ██║ ███████║{Colors.RESET}")
        print(f"        {Colors.PINK} ██║╚██╗██║ ██║ ██╔══██╗ ╚██╗ ██╔╝ ██╔══██║ ██║╚██╗██║ ██╔══██║{Colors.RESET}")
        print(f"        {Colors.LIGHT_PINK} ██║ ╚████║ ██║ ██║  ██║  ╚████╔╝  ██║  ██║ ██║ ╚████║ ██║  ██║{Colors.RESET}")
        print(f"        {Colors.WHITE} ╚═╝  ╚═══╝ ╚═╝ ╚═╝  ╚═╝   ╚═══╝   ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝  ╚═╝{Colors.RESET}")
        print()
        print(f"                        {Colors.CYAN}ai-threat detector{Colors.RESET}")
        print()
        print()

    def _log_success(self, msg):
        print(f"{Colors.GREEN}✓ {msg}{Colors.NC}")

    def _log_error(self, msg):
        print(f"{Colors.RED}✗ {msg}{Colors.NC}")

    def _log_info(self, msg):
        print(f"{Colors.BLUE}ℹ {msg}{Colors.NC}")

    def _log_warning(self, msg):
        print(f"{Colors.YELLOW}⚠ {msg}{Colors.NC}")

    def check_connection(self):
        """Check API connection"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self._log_success("Connected to API")
                print(f"  Status: {data.get('status', 'unknown')}")
                print(f"  ML Model: {'✓ Ready' if data.get('ml_model') else '✗ Not trained'}")
                return True
            else:
                self._log_error(f"API returned error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"  Details: {error_data}")
                except:
                    print(f"  Response: {response.text}")
                return False
        except requests.exceptions.ConnectionError as e:
            self._log_error(f"Cannot connect to API: {e}")
            print(f"  Check if URL is correct: {self.api_url}")
            return False
        except Exception as e:
            self._log_error(f"Error: {e}")
            return False

    def list_models(self):
        """List available LLM models"""
        try:
            response = requests.get(
                f"{self.api_url}/models",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                self._log_info("Available LLM models:")
                for model in data['models']:
                    marker = "✓ " if model == data['recommended'] else "  "
                    print(f"  {marker}{model}")
                print(f"\n  Recommended: {Colors.GREEN}{data['recommended']}{Colors.NC}")
            elif response.status_code == 401:
                self._log_error("Invalid API key. Get a valid key from your admin.")
            elif response.status_code == 403:
                self._log_error("Access denied. Check your API key.")
            else:
                self._log_error(f"Failed with status {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"  Details: {error_data}")
                except:
                    print(f"  Response: {response.text[:200]}")
        except requests.exceptions.ConnectionError:
            self._log_error(f"Cannot connect to: {self.api_url}")
            print("  Check if the API URL is correct")
        except Exception as e:
            self._log_error(f"Error: {e}")

    def reorganize_csv(self, input_file: str, output_file: str = None):
        """Reorganize pipe-delimited CSV into clean format"""
        if not CSV_REORGANIZER_AVAILABLE:
            self._log_error("CSV reorganizer not available. Ensure reorganize_csv.py is in the same directory.")
            return False

        print(f"\n{Colors.CYAN}{'='*70}{Colors.NC}")
        print(f"{Colors.WHITE}CSV DATA REORGANIZER{Colors.NC}")
        print(f"{Colors.CYAN}{'='*70}{Colors.NC}\n")

        try:
            # Check if file exists
            if not Path(input_file).exists():
                self._log_error(f"File not found: {input_file}")
                return False

            # Run reorganization
            self._log_info(f"Reorganizing: {input_file}")
            df_full, df_ml = rearrange_threat_data(input_file, output_file)

            if df_full is not None and df_ml is not None:
                self._log_success("CSV reorganization complete!")
                
                # Ask about sample datasets
                create_samples = input(f"\n{Colors.CYAN}Create sample datasets for testing? (y/n):{Colors.NC} ").strip().lower()
                if create_samples == 'y':
                    output_dir = Path(input_file).parent
                    create_sample_datasets(df_ml, output_dir)
                
                return True
            else:
                self._log_error("Reorganization failed")
                return False

        except Exception as e:
            self._log_error(f"Error during reorganization: {e}")
            return False

    def load_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load network data from file"""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            else:
                raise ValueError("Unsupported format. Use CSV or JSON.")

            return df.to_dict('records')
        except Exception as e:
            self._log_error(f"Failed to load data: {e}")
            return []

    def analyze(
        self,
        data_file: str,
        use_llm: bool = True,
        llm_model: str = "llama3.2:1b",
        confidence_threshold: float = 0.7,
        save_results: bool = True
    ):
        """Analyze network traffic"""
        self._print_banner()

        # Load data
        self._log_info(f"Loading data from: {data_file}")
        network_data = self.load_data(data_file)

        if not network_data:
            return

        self._log_success(f"Loaded {len(network_data)} records")

        # Prepare request
        payload = {
            "network_data": network_data,
            "use_llm": use_llm,
            "llm_model": llm_model,
            "confidence_threshold": confidence_threshold
        }

        # Send to API
        self._log_info("Analyzing with ML model...")
        if use_llm:
            self._log_info(f"Using LLM: {llm_model}")

        try:
            response = requests.post(
                f"{self.api_url}/analyze",
                headers=self.headers,
                json=payload,
                timeout=300  # 5 minutes for LLM analysis
            )

            if response.status_code == 200:
                result = response.json()
                self._display_results(result)

                if save_results:
                    output_file = Path(data_file).stem + "_results.json"
                    with open(output_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    self._log_success(f"Results saved to: {output_file}")

            elif response.status_code == 401:
                self._log_error("Invalid API key")
            elif response.status_code == 503:
                self._log_error("ML model not available. Contact admin to train model.")
            else:
                self._log_error(f"Analysis failed: {response.text}")

        except Exception as e:
            self._log_error(f"Error: {e}")

    def _display_results(self, result: Dict):
        """Display analysis results"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.NC}")
        print(f"{Colors.WHITE}ANALYSIS RESULTS{Colors.NC}")
        print(f"{Colors.CYAN}{'='*70}{Colors.NC}\n")

        # Summary
        print(f"Total Records:    {result['total_records']}")
        print(f"Threats Detected: {Colors.RED}{result['threats_detected']}{Colors.NC}")
        print(f"Avg Confidence:   {result['average_confidence']:.2%}")

        # Threat distribution
        threats = {}
        for pred in result['predictions']:
            label = pred['prediction']
            threats[label] = threats.get(label, 0) + 1

        print(f"\n{Colors.CYAN}Threat Distribution:{Colors.NC}")
        for threat, count in sorted(threats.items(), key=lambda x: x[1], reverse=True):
            color = Colors.GREEN if threat == 'normal' else Colors.RED
            print(f"  {color}{threat:15}{Colors.NC} {count:5} ({count/result['total_records']:.1%})")

        # Top threats - Simple table without tabulate
        threats_only = [p for p in result['predictions'] if p['is_threat']]
        if threats_only:
            threats_only.sort(key=lambda x: x['confidence'], reverse=True)

            print(f"\n{Colors.CYAN}Top 10 Threats (by confidence):{Colors.NC}\n")
            print(f"{'Record':<10} {'Threat Type':<20} {'Confidence':<12}")
            print("=" * 45)
            for p in threats_only[:10]:
                print(f"{p['record_id']:<10} {p['prediction']:<20} {p['confidence']:>10.2%}")

        # LLM Analysis
        if result.get('llm_analysis'):
            print(f"\n{Colors.CYAN}{'='*70}{Colors.NC}")
            print(f"{Colors.WHITE}DETAILED LLM ANALYSIS{Colors.NC}")
            print(f"{Colors.CYAN}{'='*70}{Colors.NC}\n")

            for analysis in result['llm_analysis']:
                pred = result['predictions'][analysis['record_id']]

                print(f"{Colors.YELLOW}{'─'*70}{Colors.NC}")
                print(f"{Colors.WHITE}Record #{analysis['record_id']}{Colors.NC} - "
                      f"{Colors.RED}{pred['prediction']}{Colors.NC} "
                      f"({pred['confidence']:.2%})")
                print(f"{Colors.YELLOW}{'─'*70}{Colors.NC}")
                print(analysis['analysis'])
                print()

    def interactive_mode(self):
        """Interactive client console"""
        self._print_banner()

        while True:
            print(f"\n{Colors.CYAN}Client Menu:{Colors.NC}")
            print("  [1] Check Connection")
            print("  [2] List Available Models")
            print("  [3] Analyze Network Traffic")
            print("  [4] Quick Analysis (No LLM)")
            print("  [5] Reorganize CSV File")
            print("  [6] View Configuration")
            print("  [7] Exit")

            choice = input(f"\n{Colors.WHITE}Select option:{Colors.NC} ").strip()

            if choice == '1':
                print()
                self.check_connection()

            elif choice == '2':
                print()
                self.list_models()

            elif choice == '3':
                print()
                data_file = input("Path to network data file (CSV/JSON): ").strip()
                if not data_file:
                    self._log_error("File path required")
                    continue

                use_llm = input("Use LLM for detailed analysis? (y/n) [y]: ").strip().lower()
                use_llm = use_llm != 'n'

                if use_llm:
                    print("\nAvailable models: llama3.2:1b (fast), phi3:mini, gemma:2b")
                    llm_model = input("Select LLM model [llama3.2:1b]: ").strip() or "llama3.2:1b"
                    threshold = input("Confidence threshold (0.0-1.0) [0.7]: ").strip() or "0.7"
                    threshold = float(threshold)
                else:
                    llm_model = "llama3.2:1b"
                    threshold = 0.7

                save = input("Save results to file? (y/n) [y]: ").strip().lower()
                save_results = save != 'n'

                print()
                self.analyze(data_file, use_llm, llm_model, threshold, save_results)

            elif choice == '4':
                print()
                data_file = input("Path to network data file (CSV/JSON): ").strip()
                if not data_file:
                    self._log_error("File path required")
                    continue

                print()
                self._log_info("Running quick analysis (ML only, no LLM)")
                self.analyze(data_file, use_llm=False, save_results=True)

            elif choice == '5':
                if not CSV_REORGANIZER_AVAILABLE:
                    print()
                    self._log_error("CSV reorganizer not available")
                    self._log_info("Ensure reorganize_csv.py is in the same directory")
                    continue

                print()
                input_file = input("Path to pipe-delimited CSV file: ").strip()
                if not input_file:
                    self._log_error("File path required")
                    continue

                output_file = input("Output file path (optional, press Enter for auto): ").strip()
                output_file = output_file if output_file else None

                print()
                self.reorganize_csv(input_file, output_file)

            elif choice == '6':
                print()
                self._log_info("Current Configuration:")
                print(f"  API URL: {Colors.CYAN}{self.api_url}{Colors.NC}")
                print(f"  API Key: {Colors.CYAN}{self.api_key[:20]}...{self.api_key[-10:]}{Colors.NC}")
                print(f"  CSV Reorganizer: {Colors.GREEN if CSV_REORGANIZER_AVAILABLE else Colors.RED}"
                      f"{'Available' if CSV_REORGANIZER_AVAILABLE else 'Not Available'}{Colors.NC}")

            elif choice == '7':
                print(f"\n{Colors.GREEN}Goodbye!{Colors.NC}\n")
                sys.exit(0)

            else:
                self._log_error("Invalid option")
                print("  Please select 1-7")

def load_config():
    """Load configuration from ~/.ntd-client/config.json"""
    config_dir = Path.home() / '.ntd-client'
    config_file = config_dir / 'config.json'

    if config_file.exists():
        with open(config_file) as f:
            return json.load(f)
    return {}

def save_config(api_url: str, api_key: str):
    """Save configuration"""
    # Ensure proper URL format
    if not api_url.startswith('http'):
        api_url = f"https://{api_url}"

    config_dir = Path.home() / '.ntd-client'
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / 'config.json'

    with open(config_file, 'w') as f:
        json.dump({'api_url': api_url, 'api_key': api_key}, f, indent=2)

    print(f"{Colors.GREEN}✓ Configuration saved to {config_file}{Colors.NC}")
    print(f"  API URL: {api_url}")
    print(f"  API Key: {api_key[:20]}...{api_key[-10:]}")

def main():
    parser = argparse.ArgumentParser(
        description='AI Network Threat Detector Client',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--api-url', help='API URL')
    parser.add_argument('--api-key', help='Your API key')
    parser.add_argument('--configure', action='store_true', help='Configure credentials')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Check connection
    subparsers.add_parser('check', help='Check API connection')

    # List models
    subparsers.add_parser('models', help='List available LLM models')

    # Analyze
    analyze_parser = subparsers.add_parser('analyze', help='Analyze network traffic')
    analyze_parser.add_argument('data_file', help='Network data file (CSV/JSON)')
    analyze_parser.add_argument('--no-llm', action='store_true', help='Disable LLM analysis')
    analyze_parser.add_argument('--llm-model', default='llama3.2:1b', help='LLM model to use')
    analyze_parser.add_argument('--threshold', type=float, default=0.7, help='Confidence threshold')
    analyze_parser.add_argument('--no-save', action='store_true', help='Don\'t save results')

    # Reorganize CSV
    reorganize_parser = subparsers.add_parser('reorganize', help='Reorganize pipe-delimited CSV')
    reorganize_parser.add_argument('input_file', help='Input CSV file (pipe-delimited)')
    reorganize_parser.add_argument('--output', help='Output CSV file (optional)')

    # Interactive mode
    subparsers.add_parser('interactive', help='Interactive mode')

    args = parser.parse_args()

    # Configuration
    if args.configure:
        print(f"{Colors.CYAN}Network Threat Detector - Configuration{Colors.NC}\n")
        print("Enter your API details (provided by your admin):\n")

        api_url = input("API URL (e.g., ai-threat-detector.up.railway.app): ").strip()

        # Add https:// if not present
        if not api_url.startswith('http'):
            api_url = f"https://{api_url}"

        api_key = input("API Key (starts with 'ntd_'): ").strip()

        # Validate API key format
        if not api_key.startswith('ntd_'):
            print(f"\n{Colors.YELLOW}⚠ Warning: API key should start with 'ntd_'{Colors.NC}")
            confirm = input("Continue anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Configuration cancelled.")
                return

        # Test connection before saving
        print(f"\n{Colors.BLUE}Testing connection...{Colors.NC}")
        try:
            test_url = api_url.rstrip('/') + '/health'
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                print(f"{Colors.GREEN}✓ API is reachable{Colors.NC}")
            else:
                print(f"{Colors.YELLOW}⚠ API returned status {response.status_code}{Colors.NC}")
        except Exception as e:
            print(f"{Colors.RED}✗ Cannot reach API: {e}{Colors.NC}")
            confirm = input("Save configuration anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Configuration cancelled.")
                return

        save_config(api_url, api_key)
        print(f"\n{Colors.GREEN}✓ Configuration complete!{Colors.NC}")
        print(f"\nTest your connection with: {Colors.CYAN}ntd-client check{Colors.NC}")
        print(f"Or launch interactive mode: {Colors.CYAN}ntd-client interactive{Colors.NC}")
        return

    # Load config
    config = load_config()
    api_url = args.api_url or config.get('api_url') or os.getenv('NTD_API_URL')
    api_key = args.api_key or config.get('api_key') or os.getenv('NTD_API_KEY')

    if not api_url or not api_key:
        print(f"{Colors.RED}Error: API URL and API Key required{Colors.NC}")
        print(f"\nOption 1: Run configuration wizard")
        print(f"  {Colors.CYAN}ntd-client --configure{Colors.NC}")
        print(f"\nOption 2: Set environment variables")
        print(f"  {Colors.CYAN}export NTD_API_URL='https://your-api.railway.app'{Colors.NC}")
        print(f"  {Colors.CYAN}export NTD_API_KEY='your-api-key'{Colors.NC}")
        sys.exit(1)

    client = ThreatDetectorClient(api_url, api_key)

    # Execute command
    if args.command == 'check':
        client._print_banner()
        client.check_connection()

    elif args.command == 'models':
        client.list_models()

    elif args.command == 'analyze':
        client.analyze(
            args.data_file,
            use_llm=not args.no_llm,
            llm_model=args.llm_model,
            confidence_threshold=args.threshold,
            save_results=not args.no_save
        )

    elif args.command == 'reorganize':
        if not CSV_REORGANIZER_AVAILABLE:
            print(f"{Colors.RED}Error: CSV reorganizer not available{Colors.NC}")
            print(f"Ensure reorganize_csv.py is in the same directory as ntd-client.py")
            sys.exit(1)
        
        client.reorganize_csv(args.input_file, args.output)

    elif args.command == 'interactive':
        client.interactive_mode()

    else:
        # Default to interactive mode if no command specified
        client.interactive_mode()

if __name__ == '__main__':
    try:
        import pandas
        import tabulate
    except ImportError:
        print("Installing required packages...")
        os.system(f"{sys.executable} -m pip install pandas tabulate requests")

    main()
