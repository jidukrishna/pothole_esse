import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.ndimage import gaussian_filter

def generate_pothole_simulation(grid_size=100, num_potholes=5,selling_slider=1,manu_slider=1):
    # Create the grid


    x = np.linspace(-25, 25, grid_size)
    y = np.linspace(-25, 25, grid_size)
    X, Y = np.meshgrid(x, y)

    # Function to create multiple potholes
    def multi_pothole(X, Y, centers, depths, widths):
        Z_multi = np.zeros_like(X)
        for (cx, cy, depth, width) in zip(centers[:, 0], centers[:, 1], depths, widths):
            Z_multi += -np.exp(-((X - cx)**2 + (Y - cy)**2) / (2 * width**2)) * depth
        return Z_multi

    # Define random pothole centers, depths, and widths
    np.random.seed(50)  # Use system time for randomness
    centers = np.random.uniform(-3*10, 3*10, (num_potholes, 2))  # Random locations
    depths = np.random.uniform(1, 1, num_potholes)  # Random depths
    widths = np.random.uniform(0.8*10, 1.5*10, num_potholes)  # Random width variations

    # Generate multiple potholes
    Z_multi_uneven = multi_pothole(X, Y, centers, depths, widths)

    # Add depth-only noise for an uneven bottom
    depth_noise_multi = (np.random.rand(*X.shape) - 0.5) * 0.8
    Z_multi_uneven += depth_noise_multi * np.exp(-0.5 * (X**2 + Y**2))

    # Ensure the road surface remains flat at the top
    Z_multi_uneven = np.minimum(0, Z_multi_uneven)

    # Apply Gaussian smoothing to the pothole bottoms
    Z_multi_smoothed = gaussian_filter(Z_multi_uneven, sigma=2)

    # Find the max dimensions
    max_length = np.max(X) - np.min(X)  # X-axis range
    max_height = np.max(Y) - np.min(Y)  # Y-axis range
    max_depth = round(np.abs(np.min(Z_multi_smoothed)),2)  # Max depth

    # # Scale down
    # scaled_length = max_length * scale_factor
    # scaled_height = max_height * scale_factor
    # scaled_depth = max_depth * scale_factor

    # # Scale down the X and Y coordinates
    # x_scaled = np.linspace(-scaled_length / 2, scaled_length / 2, grid_size)
    # y_scaled = np.linspace(-scaled_height / 2, scaled_height / 2, grid_size)
    # X_scaled, Y_scaled = np.meshgrid(x_scaled, y_scaled)

    # Scale down the pothole depths
    # Z_scaled = Z_multi_smoothed * (scaled_depth / max_depth)

    # Calculate volumes
    dx_original = np.abs(x[1] - x[0])
    dy_original = np.abs(y[1] - y[0])
    volume_original = np.sum(np.abs(Z_multi_uneven) * dx_original * dy_original)

    cuboid=round(max_depth*max_height*max_length,4)
    # Streamlit UI
    volume=round(max_depth*max_height*max_length,3)
    st.title("3D Pothole Simulation")
    st.markdown(f"**Original Volume:** {volume_original:.2f} cm<sup>3</sup>",unsafe_allow_html=True)
    st.write(f"cuboid height : {max_height}cm  length :{max_length}cm  depth : {max_depth}cm")

    st.markdown(f"**cuboid for volume :** {max_depth*max_height*max_length}cm<sup>3</sup>",unsafe_allow_html=True)
    sp=round((max_depth*0.01)*max_height*0.01*max_length*0.01*selling_slider*1000,2)
    mp=round((max_depth*0.01)*max_height*0.01*max_length*0.01*manu_slider*1000,2)

    st.write(f"total cost of blocks (selling price) : {sp} rs")
    st.write(f"total cost of blocks (manufacturing price) : {mp} rs")
    st.write(f"total profit : {round(sp-mp,2)} rs")
    st.write(f"profit margin : {round(((sp-mp)/sp)*100,2)}%")




    # st.write(f"**cuboid waste :** {round(((cuboid - volume_scaled) / cuboid),2)} cubic units")
    # st.write(f"**cuboid waste :** {round(((cuboid - volume_scaled) / cuboid) * 100,2)} %")


    # Create a side-by-side comparison plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={"projection": "3d"})

    # Plot Original Rough Pothole Surface
    ax1 = axes[0]
    ax1.plot_surface(X, Y, Z_multi_uneven, cmap='gray', edgecolor='k')
    ax1.set_title(f"Original Rough Potholes\nLength: {max_length:.2f}, Height: {max_height:.2f}, Depth: {max_depth:.2f}\nVolume: {volume_original:.2f} cubic units")
    ax1.set_xlabel("X-axis")
    ax1.set_ylabel("Y-axis")
    ax1.set_zlabel("Depth")

    # Plot Scaled-Down Smoothed Pothole Surface
    # ax2 = axes[1]
    # ax2.plot_surface(X_scaled, Y_scaled, Z_scaled, cmap='gray', edgecolor='k')
    # ax2.set_title(f"Scaled-Down ({scale_factor*100:.0f}%) Smoothed Potholes\nLength: {scaled_length:.2f}, Height: {scaled_height:.2f}, Depth: {scaled_depth:.2f}\nVolume: {volume_scaled:.2f} cubic units")
    # ax2.set_xlabel("X-axis")
    # ax2.set_ylabel("Y-axis")
    # ax2.set_zlabel("Depth")

    # Show the plots in Streamlit
    st.pyplot(fig)

# Streamlit user inputs
grid_size = st.slider("Grid Size", min_value=50, max_value=300, value=100, step=10)
num_potholes = st.slider("Number of Potholes", min_value=1, max_value=300, value=5)
selling_slider = st.slider("Cost Slider in thousands/m3 (selling price)", min_value=1, max_value=100, value=40)
manu_slider = st.slider("Cost Slider in thousands/m3 (manufacturing price)", min_value=1, max_value=100, value=27)

generate_pothole_simulation(grid_size, num_potholes,selling_slider,manu_slider)
