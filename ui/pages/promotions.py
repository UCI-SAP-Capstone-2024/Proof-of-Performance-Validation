import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page


def main():
    # Title of the application
    st.title('Current Promotions')

    # Filepath to your CSV file
    csv_file_path = 'promotions.csv'
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the DataFrame
    # st.write("### Displaying the CSV file:")
    st.dataframe(df)

    if st.button("Promotion Validation"):
        switch_page("promotion_seg")

if __name__ == "__main__":
    main()