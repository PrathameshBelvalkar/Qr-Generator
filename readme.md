# QR Code Generator API

This Flask-based API generates customizable QR codes with various styles, colors, and formats. The API supports generating QR codes in both PNG and SVG formats and allows extensive customization of QR code markers, modules, and logos.

## Features

- Generate QR codes with customizable:
  - Colors (background, foreground, marker colors)
  - Marker shapes (square, rounded, circles, etc.)
  - Module shapes (square, circle, vertical bars, etc.)
  - Logo placement with customizable scaling and background
- Generate high-definition QR codes in SVG format.
- Error correction levels for better reliability.
- Supports quiet zone and border customization.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/qrcode-generator-api.git
   cd qrcode-generator-api
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app:**

   ```bash
   python app.py
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. `/generate_qr`

Generates a customizable QR code with various style and color options.

- **Method:** `POST`
- **Content-Type:** `application/json`
- **Request Body:**

  ```json
  {
    "qr_code_text": "https://example.com",
    "image_format": "PNG",
    "background_color": "#ffffff",
    "foreground_color": "#000000",
    "marker_right_inner_color": "#000000",
    "marker_right_outer_color": "#000000",
    "marker_left_inner_color": "#000000",
    "marker_left_outer_color": "#000000",
    "marker_bottom_inner_color": "#000000",
    "marker_bottom_outer_color": "#000000",
    "marker_shape": "square",
    "module_shape": "square",
    "logo_image_url": "https://example.com/logo.png",
    "logo_scale": 0.2,
    "error_correction_level": "H",
    "quiet_zone": 4,
    "border": 4,
    "version": 1,
    "style": "classic"
  }
  ```

- **Response:**

  Returns the generated QR code image in the specified format.

- **Example:**

  ```bash
  curl -X POST http://127.0.0.1:5000/generate_qr -H "Content-Type: application/json" -d '{
      "qr_code_text": "https://example.com",
      "image_format": "PNG"
  }' --output qr_code.png
  ```

### 2. `/generate_qr_hd`

Generates a high-definition QR code in SVG format with minimal customization options.

- **Method:** `POST`
- **Content-Type:** `application/json`
- **Request Body:**

  ```json
  {
    "qr_code_text": "https://example.com",
    "border": 1
  }
  ```

- **Response:**

  Returns the generated QR code as an SVG image.

- **Example:**

  ```bash
  curl -X POST http://127.0.0.1:5000/generate_qr_hd -H "Content-Type: application/json" -d '{
      "qr_code_text": "https://example.com"
  }' --output qr_code.svg
  ```

## Code Overview

- **Main Files:**

  - `app.py`: The main Flask application file containing the QR code generation logic.
  - `requirements.txt`: Lists the dependencies required to run the application.

- **Key Functions:**
  - `generate_qr`: Handles generating customizable QR codes in various formats (PNG, JPG, etc.).
  - `generate_qr_hd`: Handles generating high-definition QR codes in SVG format with basic customization (text and border).

## Dependencies

- `Flask`: Web framework used to build the API.
- `qrcode`: Library for generating QR codes.
- `Pillow`: Python Imaging Library (PIL) fork, required for image processing.
- `requests`: Library for making HTTP requests, used for fetching logos.

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the Flask application, simply run:

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/` by default.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contribution

Feel free to submit issues, fork the repository and send pull requests! Contributions are welcome.
