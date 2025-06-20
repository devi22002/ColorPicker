import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

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
    st.set_page_config(
        page_title="Dominant Color Picker",
        page_icon="🎨",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # Custom CSS
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

    st.title("Dominant Color Picker")
    st.markdown("Upload an image to generate a color palette of the five most dominant colors.")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        st.markdown("---")

        st.subheader("Color Palette")

        colors = extract_colors(image)
        color_patches = plot_colors(colors)

        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.image(color_patches[i], caption="", width=100)
                hex_value = rgb_to_hex(colors[i])
                rgb_value = tuple(colors[i].astype(int))

                st.markdown(
                    f"""
                    <div style='display: flex; flex-direction: column; align-items: center;
                                background-color: #fefefe; padding: 10px; border-radius: 10px;
                                box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1); margin-top: 10px;'>
                        <p style='font-size: 13px; font-weight: bold; margin: 4px 0;'>Hex: {hex_value}</p>
                        <p style='font-size: 13px; margin: 4px 0;'>RGB: {rgb_value}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("---")

        st.subheader("About")
        st.markdown(
            "This app extracts the five most dominant colors from the uploaded image and displays them along with their Hex and RGB values."
        )

        st.markdown(
            '<div class="footer">Copyright 2024 (c) devi22002 on GitHub</div>',
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
