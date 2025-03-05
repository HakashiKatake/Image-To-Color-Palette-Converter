# Image Color Palette Extractor

## Project Description
The **Image Color Palette Extractor** is a desktop application built with Python and PyQt5 that allows users to extract dominant colors from an image. Users can also generate random color palettes, switch between modern UI themes, and export the generated palette to JSON or text files. The application features an intuitive drag-and-drop interface, clickable color swatches (which copy HEX codes), and dynamic theme switching to suit different aesthetics.

## Unique Features Added
- **Interactive Color Extraction:** Upload an image and extract its dominant colors using the KMeans algorithm.
- **Draggable Color Swatches:** Each extracted color is displayed as a draggable swatch; clicking a swatch copies its HEX code to the clipboard.
- **Random Color Generation:** Generate a new random palette with a single click.
- **Theme Switching:** Toggle between two distinct UI themes:
  - **Gradient Galaxy:** Dark blue-black with soft purple and pink gradients.
  - **Nature Green:** Earthy tones of green, brown, and warm yellow.
- **Palette Export:** Export the current color palette to a JSON or TXT file.
- **Integrated Image Display:** View the uploaded image alongside the extracted color palette.

## Technologies/Libraries Used
- **Python 3**  
- **PyQt5** – For building the graphical user interface.
- **Pillow (PIL)** – For image processing and conversion.
- **scikit-learn** – For applying the KMeans clustering algorithm.
- **NumPy** – For efficient array manipulation.

## Screenshots of the UI

# Galaxy Theme - 
![image](https://github.com/user-attachments/assets/1129f949-ddc2-4440-9092-0318a18fd1f5)


# Nature Theme -
![image](https://github.com/user-attachments/assets/4292bb49-fc53-4a48-811e-c1cae9be117d)


# Image Extraction Demo - 
![image](https://github.com/user-attachments/assets/68e7dd6b-fb27-48ec-9a9d-7de3f6fe2806)





## How to Run the Project
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/image-color-palette-extractor.git
   cd image-color-palette-extractor
   ```
2. **Install Dependencies:**
   Ensure you have Python 3 installed, then install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
   *(Alternatively, install manually: `pip install PyQt5 Pillow scikit-learn numpy`)*

3. **Run the Application:**
   ```bash
   python color_palette_app.py
   ```

4. **Usage:**
   - **Upload Image:** Click to select an image for color extraction.
   - **Random Colors:** Generate a random color palette.
   - **Switch Theme:** Toggle between the "Gradient Galaxy" and "Nature Green" UI themes.
   - **Export Palette:** Save the current palette as a JSON or TXT file.

## Extra Features
- **Drag-and-Drop Swatches:** Easily rearrange color swatches on the canvas.
- **Clipboard Integration:** Automatically copies the HEX code when a swatch is clicked.
- **Responsive UI:** The application adjusts the display of images and palettes dynamically for an enhanced user experience.

---
