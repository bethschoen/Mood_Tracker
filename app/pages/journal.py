import streamlit as st
import matplotlib.pyplot as plt

def show_slider_visual(value, min_val=0, max_val=100):
    fig, ax = plt.subplots(figsize=(6, 1))
    ax.plot([min_val, max_val], [0, 0], 'k-', lw=2)
    ax.plot(value, 0, 'ro', markersize=10)
    ax.set_xlim(min_val, max_val)
    ax.axis('off')
    ax.annotate(value, xy=(0, value))
    ax.annotate(value, xy=(-10, value))
    st.pyplot(fig)

# Example usage
st.write("Previously selected value:")
show_slider_visual(42)
