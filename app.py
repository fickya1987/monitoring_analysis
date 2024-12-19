import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import openai

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("TKMP Planning and Monitoring Analysis with Pelindo AI")

# File upload
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.success("File successfully uploaded!")

        # Show interactive table
        st.subheader("Interactive Data Table")
        filtered_data = st.data_editor(data, use_container_width=True)

        # GPT-4o Integration for Analysis
        st.subheader("Analysis with Pelindo AI")
        analysis_query = st.text_area("Deskripsi analisis atau detail pencarian:")
        analysis_type = st.radio("Pilih Jenis Analisis Pelindo AI:", ["Analisis Berdasarkan Data", "Pencarian Global Pelindo AI"])

        if st.button("Generate AI Analysis") and analysis_query:
            try:
                if analysis_type == "Analisis Berdasarkan Data":
                    # Analisis berdasarkan data
                    prompt_data = f"Lakukan analisis mendalam tentang '{analysis_query}' berdasarkan data berikut:\n{filtered_data.to_csv(index=False)}"
                    response_data = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Anda adalah analis data berpengalaman mengenai pelabuhan dan Pelindo. Gunakan bahasa Indonesia."},
                            {"role": "user", "content": prompt_data}
                        ],
                        max_tokens=2048,
                        temperature=1.0
                    )
                    result_data = response_data['choices'][0]['message']['content']
                    st.write("#### Hasil Analisis Berdasarkan Data Pelindo AI:")
                    st.write(result_data)
                else:
                    # Pencarian global GPT-4o
                    prompt_search = f"Lakukan pencarian mendalam tentang '{analysis_query}' menggunakan pengetahuan global Anda."
                    response_search = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Anda adalah mesin pencari pintar. Gunakan bahasa Indonesia."},
                            {"role": "user", "content": prompt_search}
                        ],
                        max_tokens=2048,
                        temperature=1.0
                    )
                    result_search = response_search['choices'][0]['message']['content']
                    st.write("#### Hasil Pencarian Global Pelindo AI:")
                    st.write(result_search)
            except Exception as e:
                st.error(f"Error generating analysis: {e}")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.warning("Tidak ada file yang diunggah. Silakan unggah file CSV atau Excel.")
