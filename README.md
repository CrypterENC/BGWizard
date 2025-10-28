# BGWizard

A powerful AI-powered background removal tool with both web interface and CLI support.

## ✨ Features

- **AI-Powered**: Uses advanced U2Net models for precise background removal
- **Web Interface**: Modern drag-and-drop UI with real-time previews
- **Batch Processing**: Handle multiple images with ZIP downloads
- **CLI Tool**: Command-line interface for automation
- **Multiple Formats**: Export as PNG (transparent), JPG, or WebP
- **Advanced Settings**: Fine-tune foreground/background thresholds
- **Docker Ready**: Easy deployment with Docker Compose

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
  - **Windows**: Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Python 3.10+ (for local development)

### Running with Docker (Recommended)
```bash
cd BackGroundRemover
docker-compose up --build
```
Access at: http://localhost:5100

### Local Development
```bash
cd BackGroundRemover
pip install -r requirements.txt
python app.py
```

## 📁 Project Structure
```
TOOLS/
├── BackGroundRemover/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Docker container config
│   ├── docker-compose.yml  # Docker Compose setup
│   └── templates/
│       └── index.html      # Web interface
└── README.md
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `FLASK_APP`: Main application file (app.py)

### AI Model Options
- **u2net**: General-purpose background removal
- **u2net_human_seg**: Optimized for human subjects
- **u2netp**: Specialized for portrait photography

## 🌐 Usage

1. **Upload Images**: Drag and drop or click to select PNG/JPG/WebP files
2. **Configure Settings**:
   - Choose AI model based on image type
   - Select output format
   - Adjust advanced parameters if needed
3. **Process**: Click "Process Images" to start AI processing
4. **Download**: Single images download automatically, batches come as ZIP

## 🤝 Contributing

Feel free to add more tools to this collection! Each tool should:
- Be web-based with a clean, modern UI
- Include proper documentation
- Have Docker support for easy deployment
- Follow the established project structure

## 📄 License

This project is open-source. See individual tool directories for specific licensing.

## ⚠️ Disclaimer

This tool uses AI/ML models for image processing. Ensure you have proper rights to process and modify uploaded images.s