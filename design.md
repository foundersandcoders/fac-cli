# FAC CLI System Design & Architecture

## Architecture Overview

### System Architecture Pattern
- **Pattern**: Functional Architecture with Clear Separation of Concerns
- **Approach**: Single-responsibility functions with data pipeline processing
- **Style**: Functional programming, terse naming, single-word verbs

### Component Interaction Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Routing   │    │   Command       │    │   Data Sources  │
│   (fac.py)      │    │   Handlers      │    │   (airtable.py) │
│                 │    │   (gr.py)       │    │                 │
│ • route()       │───►│ • fetch()       │───►│ • get()         │
│ • parse()       │    │ • process()     │    │ • auth()        │
│ • dispatch()    │    │ • display()     │    │ • request()     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Terminal      │
                       │   Display       │
                       │   (display.py)  │
                       │                 │
                       │ • format()      │
                       │ • table()       │
                       │ • print()       │
                       └─────────────────┘
```

## Technology Stack

### Core Technologies
- **Runtime**: Python 3.9+
- **HTTP Client**: `requests` library for Airtable API calls
- **CLI Framework**: Native `sys.argv` for lightweight command parsing
- **Data Processing**: Native Python data structures (dicts, lists)
- **Table Display**: `tabulate` library for terminal table formatting
- **Environment**: `python-dotenv` for secure credential management

### Development Tools
- **Testing**: `pytest` with functional testing approach
- **Linting**: `black` (formatter), `flake8` (linter), `mypy` (type checking)
- **Dependencies**: `pip` with `requirements.txt`
- **Version Control**: Git with conventional commits
- **Code Quality**: Pre-commit hooks, automated testing

### Project Dependencies
```txt
requests>=2.31.0
tabulate>=0.9.0
python-dotenv>=1.0.0
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
```

## Project Structure

```
/
├── .kiro/                  # Kiro AI IDE configuration
│   ├── hooks/             # Agent hooks and automations
│   ├── steering/          # Code generation standards
│   └── config.json        # Kiro configuration
├── fac.py                 # Main CLI entry point and routing
├── commands/              # Command handler modules
│   └── gr.py             # Gateway recent command handler
├── sources/               # Data source modules
│   └── airtable.py       # Airtable API integration
├── display.py            # Terminal display formatting
├── config.py             # Configuration and credential management
├── tests/                # Test files
│   ├── test_fac.py       # Main routing tests
│   ├── test_gr.py        # Gateway recent command tests
│   ├── test_airtable.py  # Airtable source tests
│   └── test_display.py   # Display formatting tests
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
├── requirements.md       # EARS format requirements
├── design.md            # This file
├── tasks.md             # Implementation roadmap
└── README.md            # Project setup and usage
```

## Design Principles

### FAC CLI Code Standards
1. **Functional Programming**: Pure functions, no classes except when absolutely necessary
2. **Terse Naming**: Single-word verbs for functions (fetch, process, display, route)
3. **Single Responsibility**: Each function does exactly one thing
4. **Separation of Concerns**: Routing, fetching, processing, display in separate modules
5. **Data Pipeline**: Input → Fetch → Process → Display → Output

### Module Responsibilities

#### fac.py (Main Router)
```python
def route(args: List[str]) -> None:
    """Route command to appropriate handler"""

def parse(args: List[str]) -> Tuple[str, List[str]]:
    """Parse command line arguments"""

def dispatch(command: str, args: List[str]) -> None:
    """Dispatch to command handler"""
```

#### commands/gr.py (Gateway Recent)
```python
def run(args: List[str]) -> None:
    """Execute gateway recent command"""

def fetch() -> List[Dict]:
    """Fetch data via airtable source"""

def process(data: List[Dict]) -> List[Dict]:
    """Transform raw data for display"""

def display(data: List[Dict]) -> None:
    """Format and show data in terminal"""
```

#### sources/airtable.py (Data Source)
```python
def get(view_url: str) -> List[Dict]:
    """Get data from Airtable view"""

def auth(api_key: str) -> Dict[str, str]:
    """Create authentication headers"""

def request(url: str, headers: Dict) -> requests.Response:
    """Make HTTP request to Airtable API"""
```

#### display.py (Terminal Output)
```python
def table(data: List[Dict], headers: List[str]) -> str:
    """Format data as table"""

def format(data: List[Dict]) -> List[Dict]:
    """Format data for display"""

def print(output: str) -> None:
    """Print to terminal"""
```

### Testing Strategy
- **Function-Level Testing**: Each function tested independently
- **Data Pipeline Testing**: Input/output validation at each stage
- **Integration Testing**: Full command execution testing
- **Error Scenario Testing**: Network failures, invalid data, missing credentials

### Error Handling Philosophy
- **Explicit Returns**: Functions return success/error states clearly
- **Early Validation**: Check inputs before processing
- **User-Friendly Messages**: Clear error messages for CLI users
- **Graceful Failures**: System exits cleanly on errors

## Data Flow Architecture

### FAC CLI Request Processing Flow
```
CLI Args → Parse → Route → Command Handler → Data Source → Process → Display → Terminal
    ↓         ↓       ↓           ↓               ↓           ↓        ↓         ↓
 sys.argv   Extract  Dispatch   gr.run()     airtable.get() Transform Format   Print
           Command   to Module  Function     API Request    Data     Table    Output
```

### Gateway Recent (gr) Command Flow
```
./fac.py gr → route() → dispatch() → gr.run() → gr.fetch() → airtable.get() → API Request
                                        ↓           ↓             ↓            ↓
                                   gr.process() ← Raw Data ← JSON Response ← HTTP 200
                                        ↓
                                   gr.display() → display.table() → Terminal Output
```

### Error Handling Flow
```
Error Occurs → Catch → Format Message → Print to stderr → Exit Code
     ↓           ↓           ↓              ↓               ↓
Network Fail   Try/Except  User-Friendly  sys.stderr    sys.exit(1)
API Error      Exception   Error Text     .write()      Non-zero
Invalid Data   Handling    Clear Action   Red Text      Return
```

## Security Considerations

### Credential Management
- API keys stored in `.env` file (not in source code)
- `.env` file added to `.gitignore` to prevent accidental commits
- Environment variables loaded via `python-dotenv`
- `.env.example` template provided for setup guidance

### API Security
- HTTPS-only communication with Airtable API
- API key included in headers, not URL parameters
- Request timeout limits to prevent hanging connections
- No sensitive data logged to terminal or files

### Input Validation
- Command line arguments validated before processing
- API response data validated before display
- URL validation for Airtable view endpoints
- Error messages don't expose internal system details

## Performance Requirements

### Response Times
- CLI command execution: < 2 seconds for normal operations
- Airtable API requests: < 1 second under typical network conditions
- Data processing: < 100ms for typical datasets (< 1000 records)
- Terminal display: < 50ms for formatted output

### Optimization Strategies
- Minimal dependencies to reduce startup time
- Efficient data structures (native Python lists/dicts)
- Request timeouts to prevent hanging
- Lazy loading of modules when possible

## Error Handling Strategy

### Error Categories
- **Network Errors**: Connection failures, timeouts, DNS issues
- **API Errors**: Invalid credentials, rate limiting, service unavailable
- **Data Errors**: Malformed responses, missing fields, type mismatches
- **CLI Errors**: Invalid commands, missing arguments, permission issues

### Error Response Format
```python
def handle_error(error_type: str, message: str, exit_code: int = 1) -> None:
    """Standard error handling for CLI"""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)
```

### User-Friendly Error Messages
- **Network Error**: "Unable to connect to Airtable. Check your internet connection."
- **Auth Error**: "Invalid Airtable credentials. Check your API key in .env file."
- **Data Error**: "Unexpected response from Airtable. The view may have changed."
- **CLI Error**: "Unknown command 'xyz'. Available commands: gr"

## Extensibility Design

### Adding New Commands
1. Create new file in `commands/` directory (e.g., `commands/new_cmd.py`)
2. Implement `run(args)` function with fetch/process/display pattern
3. Add command mapping in `fac.py` dispatcher
4. Add tests in `tests/test_new_cmd.py`

### Adding New Data Sources
1. Create new file in `sources/` directory (e.g., `sources/github.py`)
2. Implement `get(url)` function with auth/request pattern
3. Import and use in command handlers
4. Add tests in `tests/test_github.py`

### Command Template
```python
# commands/template.py
from sources import airtable
from display import table

def run(args: List[str]) -> None:
    """Template command handler"""
    data = fetch()
    processed = process(data)
    display(processed)

def fetch() -> List[Dict]:
    """Fetch data from source"""
    return airtable.get(CONFIG.view_url)

def process(data: List[Dict]) -> List[Dict]:
    """Transform data for display"""
    return data

def display(data: List[Dict]) -> None:
    """Show formatted data"""
    table(data, headers=['Col1', 'Col2'])
```

---

*This design document should be reviewed and updated as the project evolves. All architectural decisions should align with the requirements specified in requirements.md.*