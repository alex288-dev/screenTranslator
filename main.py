import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
import pytesseract
from pynput import keyboard
import threading
import google.generativeai as genai

# --- Gemini API Helper ---
def translate_with_gemini(text, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"Translate the following text from English to Russian and write nothing else, only the translation:\n{text}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Translation error: {e}"

# --- Overlay for Region Selection ---
class ScreenSelector(tk.Toplevel):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.3)
        self.attributes('-topmost', True)
        self.config(bg='gray')
        self.start_x = self.start_y = self.rect = None
        self.canvas = tk.Canvas(self, cursor="cross", bg='gray', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_drag(self, event):
        if (
            self.rect is not None and
            self.start_x is not None and self.start_y is not None and
            event.x is not None and event.y is not None
        ):
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        if self.rect is not None:
            coords = self.canvas.coords(self.rect)
            if len(coords) == 4 and all(c is not None for c in coords):
                x1, y1, x2, y2 = coords
                self.destroy()
                self.callback((int(x1), int(y1), int(x2), int(y2)))

# --- Main Application ---
class ScreenTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Translator")
        self.root.geometry("240x160")  # Make the window bigger
        self.api_key = "AIzaSyCT6AcdNxa84FF6BV0-UwO8kVIAeLMIr5g"  # <-- Replace with your Gemini API key
        self.font_size = 12
        self.select_btn = tk.Button(root, text="Select", command=self.start_selection)
        self.select_btn.pack(padx=20, pady=(30, 10))
        # Font size option
        font_frame = tk.Frame(root)
        font_frame.pack(pady=10)
        tk.Label(font_frame, text="Font size:").pack(side=tk.LEFT)
        self.font_size_var = tk.IntVar(value=self.font_size)
        font_spin = tk.Spinbox(font_frame, from_=8, to=48, width=5, textvariable=self.font_size_var, command=self.update_font_size)
        font_spin.pack(side=tk.LEFT, padx=5)
        self.region1 = self.region2 = None
        self.translation_window = None
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def update_font_size(self):
        self.font_size = self.font_size_var.get()

    def start_selection(self):
        self.root.withdraw()
        ScreenSelector(self.on_region1_selected)

    def on_region1_selected(self, region):
        self.region1 = region
        ScreenSelector(self.on_region2_selected)

    def on_region2_selected(self, region):
        self.region2 = region
        self.root.deiconify()
        messagebox.showinfo("Ready", "Press 'Insert' to translate, 'End' to reset.")

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.insert and self.region1 and self.region2:
                threading.Thread(target=self.perform_translation).start()
            elif key == keyboard.Key.end:
                self.hide_translation_window()
        except Exception as e:
            print(e)

    def hide_translation_window(self):
        if self.translation_window:
            self.translation_window.destroy()
            self.translation_window = None

    def perform_translation(self):
        # Screenshot and OCR
        img = ImageGrab.grab(bbox=self.region1)
        text = pytesseract.image_to_string(img, lang='eng')
        translation = translate_with_gemini(text, self.api_key)
        self.show_translation(translation)

    def show_translation(self, text):
        if self.translation_window:
            self.translation_window.destroy()
        if self.region2 is None:
            return
        self.translation_window = tk.Toplevel()
        self.translation_window.overrideredirect(True)
        self.translation_window.attributes('-topmost', True)
        self.translation_window.attributes('-alpha', 0.85)  # Semi-transparent
        x1, y1, x2, y2 = self.region2
        width, height = x2 - x1, y2 - y1
        self.translation_window.geometry(f"{width}x{height}+{x1}+{y1}")

        # Use Canvas for black background only (no rounded corners)
        canvas = tk.Canvas(self.translation_window, width=width, height=height, highlightthickness=0, bg='black')
        canvas.pack(fill=tk.BOTH, expand=True)
        # Place text with user-selected font size
        canvas.create_text(width // 2, height // 2, text=text, fill='white', font=("Arial", self.font_size), width=width - 40, justify='center')

    def reset(self):
        # This method is no longer called on 'End', but can be used elsewhere if needed
        if self.translation_window:
            self.translation_window.destroy()
            self.translation_window = None
        self.region1 = self.region2 = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenTranslatorApp(root)
    root.mainloop() 