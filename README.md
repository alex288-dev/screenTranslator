# Screen Translator

A Python application that translates text directly from your screen using OCR (Optical Character Recognition) and the Gemini API. Select a region to capture text from, and another region to display the translation.

## Features

*   **Screen Region Selection:** Easily select any area of your screen for text extraction.
*   **Real-time Translation:** Translate captured text using the powerful Gemini API.
*   **Overlay Display:** Display translated text as an overlay on a designated screen region.
*   **Customizable Font Size:** Adjust the font size of the translated text.
*   **Hotkey Control:** Use keyboard shortcuts for translation and resetting.

## Prerequisites

Before you begin, ensure you have the following installed:

*   Python 3.x
*   `pip` (Python package installer)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/screenTranslator.git
    cd screenTranslator
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Note: You'll need to create a `requirements.txt` file if it doesn't exist yet, containing the project's dependencies: `Pillow`, `pytesseract`, `pynput`, `google-generativeai`, `tkinter` (usually built-in).)*

3.  **Install Tesseract OCR:**

    This project relies on Tesseract OCR. Download and install it from the [Tesseract-OCR GitHub page](https://tesseract-ocr.github.io/tessdoc/Installation.html). Make sure to add Tesseract to your system's PATH.

    On Windows, you might need to specify the path to `tesseract.exe` in your `main.py` if it's not automatically found. For example:
    ```python
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    ```

## Configuration

1.  **Get a Gemini API Key:**

    Obtain an API key from the [Google AI Studio](https://aistudio.google.com/).

2.  **Update `main.py` with your API Key:**

    Open `main.py` and replace `"YOUR_GEMINI_API_KEY"` with your actual Gemini API key:

    ```python
    self.api_key = "YOUR_GEMINI_API_KEY" # Replace with your Gemini API key
    ```

## Usage

1.  **Run the application:**

    ```bash
    python main.py
    ```

2.  **Select Translation Regions:**
    *   Click the "Select" button.
    *   Drag your mouse to select the first region (where text will be captured from).
    *   Repeat to select the second region (where the translated text will be displayed).
    *   A message box will confirm that the application is ready.

3.  **Translate Text:**
    *   Press the `Insert` key on your keyboard to capture text from the first region and display its translation in the second region.

4.  **Hide Translation Window:**
    *   Press the `End` key on your keyboard to hide the translation overlay.

## Project Structure

*   `main.py`: The main application script containing the UI, screen selection, OCR, and translation logic.

## Dependencies

*   `tkinter`: For the graphical user interface.
*   `Pillow` (PIL): For image manipulation (screenshots).
*   `pytesseract`: Python wrapper for Tesseract-OCR.
*   `pynput`: For keyboard event listening.
*   `google-generativeai`: Google Gemini API client library.
