#### streamlit run funnel_app.py --server.enableXsrfProtection=false

import streamlit as st
import pandas as pd
from graph.funel_graph import FunelGraph

import matplotlib.pyplot as plt


def main():
    st.set_page_config(
        page_title="Funnel Graph",
        page_icon = "🌴",
        layout="centered"
    )
    st.title('Upload graph data')
    st.write('''Upload data and lables CSV's sources for your funnel graph''')
    # data upload
    uploaded_data = st.file_uploader("Choose a CSV with data")
    if uploaded_data:
        df_data = pd.read_csv(uploaded_data, sep=";")
        N_rows, N_cols = df_data.shape
        # st.write(df_data)
    uploaded_labels = st.file_uploader("Choose a CSV file with labels")
    if uploaded_labels:
        df_labels = pd.read_csv(uploaded_labels, sep=";")
        # st.write(df_labels)

    # color choice
    if uploaded_data:
        st.title("Set colors")
        col0, col1= st.columns(2)
        color0, color1 = ['']*N_rows, ['']*N_rows
    else:
        st.title("Load data to set colors")
    
    colors = [
        ['#C33764', '#1BFFFF'],
        ['#FBB03B', '#D4145A'],
        ['#FCEE21', '#009245'],
        ['#1BFFFF', '#e05153'],
        ['#009245', '#FCEE21']
        ]

    if uploaded_data:
        with col0:
            for i in range(N_rows):
                color0[i] = st.color_picker(
                    f'Left {i}th color', 
                    colors[i][0] if i<len(colors) else '#000000', 
                    key="0"+str(i))
        with col1:
            for i in range(N_rows):
                color1[i] = st.color_picker(
                    f'Right {i}th color', 
                    colors[i][1] if i<len(colors) else '#000000', 
                    key="1"+str(i))


    generate = st.button("Generate funnel graph")
    if generate == True:
        fg = FunelGraph()
        fg.load_data(df_data)
        fg.load_labels(df_labels)
        fg.normalize_data(normaliseQ=True)
        fg.create_paths()
        colors_from_pickers = map(list,list(zip(color0, color1)))
        fg.draw(colors=colors_from_pickers, visible=False, axesQ=False)
        fig, ax = fg.fig, fg.ax
        st.pyplot(fig)

    # # st.file_uploader()
    # # st.latex(r'''e^{i\pi}+1=0''')
    # fig = plt.figure(figsize=(8,8))
    # # ...
    # st.pyplot(fig)

if __name__ == "__main__":
    main()