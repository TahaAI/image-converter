from customtkinter import *
from tkinter import filedialog
from PIL import Image
import os
import tempfile
import shutil

# -------------------- THEME --------------------
set_appearance_mode("dark")
set_default_color_theme("green")

uploaded_image_path = None
converted_image_path = None


# -------------------- WINDOW --------------------
def setup_windows():
    window = CTk()

    width = 720
    height = 460

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)
    window.title("Image Converter")

    return window


# -------------------- FRAMES --------------------
def top_create_frame(window):
    top_frame = CTkFrame(window, height=120, fg_color="#1e1e2e", corner_radius=20)
    top_frame.pack(fill="x", padx=20, pady=(20, 10))
    return top_frame


def center_create_frame(window):
    cen_frame = CTkFrame(window, fg_color="#2a2a3d", corner_radius=25)
    cen_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    return cen_frame


# -------------------- TITLE --------------------
def title_dis(top_frame):
    title = CTkLabel(
        top_frame,
        text="Image Converter",
        font=("Segoe UI", 26, "bold"),
        text_color="#00ffcc",
    )
    dis = CTkLabel(
        top_frame,
        text="Convert PNG & JPG images to WEBP",
        font=("Segoe UI", 14),
        text_color="#a0a0c0",
    )
    title.pack(pady=(25, 5))
    dis.pack()


# -------------------- BACKEND --------------------
def upload_img():
    global uploaded_image_path, converted_image_path

    uploaded_image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if uploaded_image_path:
        converted_image_path = None
        status_label.configure(text="Image uploaded ✅", text_color="#00ffcc")
        convert_btn.configure(state="normal")
        download_btn.configure(state="disabled")


def convert_img():
    global converted_image_path

    if not uploaded_image_path:
        return

    img = Image.open(uploaded_image_path)

    temp_dir = tempfile.gettempdir()
    base_name = os.path.splitext(os.path.basename(uploaded_image_path))[0]
    temp_path = os.path.join(temp_dir, f"{base_name}.webp")

    img.save(temp_path, "WEBP", quality=85)

    converted_image_path = temp_path
    status_label.configure(text="Converted to WEBP ✅", text_color="#7dff7a")
    download_btn.configure(state="normal")


def download_img():
    if not converted_image_path:
        return

    save_path = filedialog.asksaveasfilename(
        initialfile=os.path.basename(converted_image_path),
        defaultextension=".webp",
        filetypes=[("WEBP Image", "*.webp")],
    )

    if save_path:
        shutil.copy(converted_image_path, save_path)
        status_label.configure(text="Downloaded successfully ✅", text_color="#4c7dff")


# -------------------- UI --------------------
def working_part(cen_frame):
    global status_label, convert_btn, download_btn

    btn_style = {
        "width": 240,
        "height": 45,
        "corner_radius": 12,
        "font": ("Segoe UI", 15, "bold"),
    }

    upload_btn = CTkButton(
        cen_frame,
        text="📤 Upload Image",
        command=upload_img,
        fg_color="#00ffcc",
        text_color="#000",
        hover_color="#00d9b0",
        **btn_style,
    )

    convert_btn = CTkButton(
        cen_frame,
        text="⚙️ Convert to WEBP",
        command=convert_img,
        fg_color="#4c7dff",
        hover_color="#3b65d9",
        state="disabled",
        **btn_style,
    )

    download_btn = CTkButton(
        cen_frame,
        text="💾 Download",
        command=download_img,
        fg_color="#ff4c7d",
        hover_color="#d93b65",
        state="disabled",
        **btn_style,
    )

    status_label = CTkLabel(
        cen_frame,
        text="Waiting for image...",
        font=("Segoe UI", 14),
        text_color="#a0a0c0",
    )

    upload_btn.pack(pady=(35, 15))
    convert_btn.pack(pady=15)
    status_label.pack(pady=15)
    download_btn.pack(pady=15)


# -------------------- MAIN --------------------
def mainPanel():
    window = setup_windows()
    top_fr = top_create_frame(window)
    center_fr = center_create_frame(window)

    title_dis(top_fr)
    working_part(center_fr)

    window.mainloop()


if __name__ == "__main__":
    mainPanel()
