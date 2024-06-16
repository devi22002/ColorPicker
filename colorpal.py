import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Function to extract dominant colors
def extract_colors(image, num_colors=5):
    image_np = np.array(image)
    image_np = image_np.reshape((image_np.shape[0] * image_np.shape[1], 3))

    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(image_np)

    colors = kmeans.cluster_centers_
    return colors

# Function to plot color patches
def plot_colors(colors):
    color_patches = []
    for color in colors:
        color_patch = np.zeros((100, 100, 3), dtype=np.uint8)
        color_patch[:, :, :] = color.astype(int)
        color_patches.append(color_patch)

    return color_patches

# Function to convert RGB to Hex
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*map(int, rgb))

# Main Streamlit app
def main():
    # Set page configuration
    st.set_page_config(
        page_title="Dominant Color Picker",
        page_icon="🎨",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for gradient background
    st.markdown(
         """
        <style>
        body {
            background-color: #f0f0f0;
            background-image: linear-gradient(to right, #ffffff, #FF6347, #FFFF00, #6495ED, #ffffff);
            color: #333333;
            font-family: Arial, sans-serif;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .header-decoration {
            height: 100px;
            background-image: linear-gradient(to right, #ffffff, #FF6347, #FFFF00, #6495ED, #ffffff);
            border-bottom-left-radius: 50% 20%;
            border-bottom-right-radius: 50% 20%;
        }

        .footer {
            bottom: 10px;
            width: 100%;
            text-align: center;
            font-size: 12px;
            color: #666666;
            margin-top: 15rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="header-decoration"></div>', unsafe_allow_html=True)
    # Main content
    st.title("Dominant Color Picker")
    st.markdown(
        "Upload an image to generate a color palette of the five most dominant colors."
    )

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        st.markdown("---")  # Horizontal separator

        st.subheader("Color Palette")

        colors = extract_colors(image)
        color_patches = plot_colors(colors)

        # Display each color patch in a separate box with Hex and RGB values centered below
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.image(color_patches[i], caption=f"Color {i+1}", width=130, use_column_width=False)
                hex_value = rgb_to_hex(colors[i])
                st.markdown(
                    f"<div style='display: flex; flex-direction: column; align-items: center; text-align: center;"
                    f"            background-color: #f0f0f0; padding: 8px; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>"
                    f"    <p style='font-size: 14px; font-weight: bold;'>Hex: {hex_value}</p>"
                    f"    <p style='font-size: 14px;'>RGB: {colors[i].astype(int)}</p>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        st.markdown("---") 

        st.subheader("About")
        st.markdown(
            "This app extracts the five most dominant colors from the uploaded image and displays them along with their Hex and RGB values."
        )

        st.markdown(
            '<div class="footer">Copyright 2024 (c) Devi Humaira</div>',
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
