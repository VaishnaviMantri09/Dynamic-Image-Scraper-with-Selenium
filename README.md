#  Dynamic Image Scraper with Selenium:

This Python script allows you to scrape and download **all images** (including lazy-loaded and background images) from a given webpage using Selenium and Requests.

## What the Script Does?

- Opens the webpage using a **headless Chrome browser**.
- Scrolls the page to **load all images dynamically**, including lazy-loaded content.
- Extracts and downloads all unique image URLs (including background images) into a folder called `downloaded_images/`.

## Features

- Handles lazy-loaded images by smart scrolling
- Extracts image sources from `src`, `data-src`, and `srcset`
- Also captures background images from inline styles
- Downloads all found images to a local folder

## Requirements

- Python 3.7+
- Google Chrome installed
- ChromeDriver (managed automatically)

## 🛠 Execution of Script Locally

1. **Clone the repository**

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
```

3. **Activate the environment**
   
 - Windows: `venv\Scripts\activate`
 - Mac/Linux: `source venv/bin/activate`

4. **Install required packages**

```bash
pip install -r requirements.txt
```

5. **Run the script by passing the URL of the target webpage**

```bash
python scraper.py
```

## Run with Docker (Recommended)

1. **Clone the repository**

2. **Build the Docker image**

```bash
docker build -t image-scraper .
```

3. **Make sure the downloaded_images directory exists or Docker might fail to mount it**
```bash
mkdir downloaded_images
```

4. **Run the scraper**

 On Windows, %cd% will work in Command Prompt, while PowerShell requires $PWD.
```bash
docker run --rm -v %cd%\downloaded_images:/app/downloaded_images image-scraper
```

 On PowerShell, use:
```bash
docker run --rm -v "${PWD}/downloaded_images:/app/downloaded_images" image-scraper
```

## Output

You can find the images in this folder, and they will be saved with their appropriate file extensions (.jpg, .png, etc.).

```bash
downloaded_images/
├── image_001.jpg
├── image_002.png
└── ...
```

## ⚠️ Notes

- Some websites may use anti-bot measures that block headless browsers. If the script fails to load content, try using a non-headless browser for debugging.
- This script is designed for public webpages — **do not use it to scrape content from websites without permission**.
