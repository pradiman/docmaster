# DocMaster – PDF Toolkit

A simple Flask web app for merging PDFs, splitting PDFs, and converting images into PDFs with QR code generation for every output. Built as a final project for a 20-day Python training course.

## Features
- Merge PDFs: Combine 2 or more PDF files into one document.
- Split PDF: Extract a specific page range (e.g. `1-3`) from a PDF.
- Images to PDF: Convert multiple JPG/JPEG/PNG images into a single multi-page PDF.
- QR Code generation: Every generated output gets a "Generate QR Code" button that creates a scannable QR code (via the [QRServer API](https://goqr.me/api/)) linking to the file's download URL.

## Tech Stack

- Python 3.12
- Flask + Flask-WTF (forms, CSRF protection)
- Jinja2 templates + Bootstrap 5
- pypdf (PDF operations)
- Pillow (image operations)
- requests (QR code API calls)
- [uv](https://docs.astral.sh/uv/) for dependency management

## Project Structure
docmaster/
├── app.py # Flask routes
├── services/
│ ├── pdf_manager.py # PDFManager: merge_pdf(), split_pdf()
│ ├── image_manager.py # ImageManager: images_to_pdf()
│ └── qr_helper.py # generate_qr_code() helper
├── forms/
│ └── pdf_forms.py # Flask-WTF form classes
├── templates/ # Jinja2 HTML templates
├── static/
│ └── style.css
├── uploads/ # temporary upload storage (cleaned after processing)
└── outputs/ # generated PDFs and QR code images

## Setup & Running Locally

1. Clone the repository:
   git clone https://github.com/pradiman/docmaster.git
   cd docmaster


2. Install dependencies with uv:
   uv sync


3. Run the app:
   uv run python app.py


4. Open your browser to `http://127.0.0.1:5000`

## Known Limitations

- QR codes point to localhost by default. Since the app runs locally, the download URL encoded in each QR code (e.g. `http://127.0.0.1:5000/download/merged.pdf`) is only reachable from the same machine. QR codes can be tested via online QR scanner tools which will point to the download url for the output file. To test QR codes on a phone, run the app with `host="0.0.0.0"` in `app.py` and access it via your machine's local network IP (e.g. `http://192.168.x.x:5000`) from a device on the same Wi-Fi network. 
- No authentication or user accounts — this is a single-user local tool by design.
- Uploads are limited to 20MB per request.
- Output files use a random suffix (e.g. `merged_a1b2c3d4.pdf`) to avoid overwriting previous results, but `outputs/` will grow over time since there's no automatic cleanup of old generated files.

## Possible Future Improvements

- PDF compression (merge/split/convert results could optionally be compressed)
- Deployment to a public host so QR codes work from any device

## Course Context

This project was built incrementally over multiple phases as the final assignment for a 20-day Python training course, covering Flask fundamentals, form handling, file processing, external API integration, error handling, and the full Git/GitHub workflow.