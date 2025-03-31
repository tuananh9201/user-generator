# User Generator

A Python desktop application for generating bulk user credentials with customizable prefixes and export to Excel.

![Application Screenshot](docs/images/app_screenshot.png)

## Features

- 🚀 Generate multiple user accounts quickly
- 📝 Customizable username prefixes and patterns
- 🔐 Secure random password generation
- 📊 Export to Excel with formatted output
- 📂 Built-in file management and quick access
- 📝 Real-time logging and progress tracking
- 🖥️ Cross-platform support (Windows, macOS, Linux)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Option 1: Using pip

```bash
# Clone the repository
git clone https://github.com/tuananh9201/user-generator.git
cd user-generator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/base.txt
```

### Option 2: Using executable

Download the latest release from the [releases page](https://github.com/tuananh9201/user-generator/releases).

## Usage

### Running from Source

```bash
python src/main.py
```

### Using the Application

1. Enter the number of users to generate
2. Specify the username prefix
3. Enter the contract number
4. Click "Generate Users"
5. Find the generated Excel file in the application's file list

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements/dev.txt

# Install test dependencies
pip install -r requirements/test.txt
```

### Running Tests

```bash
pytest tests/
```

### Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller app.spec
```

## Project Structure

```
user_generator/
├── src/
│   ├── core/           # Core business logic
│   ├── gui/            # GUI components
│   └── utils/          # Utility functions
├── resources/          # Application resources
├── tests/             # Test suite
├── requirements/      # Dependencies
└── scripts/          # Build and utility scripts
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [pandas](https://pandas.pydata.org/) for Excel file handling
- [Faker](https://faker.readthedocs.io/) for generating realistic test data

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/tuananh9201/user-generator](https://github.com/tuananh9201/user-generator)

## Changelog

### [1.0.0] - 2024-01-20

- Initial release
- Basic user generation functionality
- Excel export feature
- File management system
