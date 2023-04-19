from validate_email import validate_email
import dns.resolver
import streamlit as st
import pandas as pd
from functionforDownloadButtons import download_button
import re
df = pd.DataFrame()
result = ""
email_column = None
def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="images/logo.png", page_title="Email Verifier")

c2, c3 = st.columns([6, 1])

with c2:
    c31, c32 = st.columns([12, 2])
    with c31:
        st.caption("")
        st.title("Email Verifier")
    with c32:
        st.image(
            "images/logo.png",
            width=200,
        )

def is_email(string):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(email_regex, string))
def check_email_domain(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return True if records else False
    except dns.resolver.NXDOMAIN:
        return False
tab1, tab2 = st.tabs(["One Email Verifier", "CSV Email Verifier"])
with tab1:

    def get_values(email):

        domain = email.split('@')[1]
        domain_valid = check_email_domain(domain)

        email_valid = validate_email(email)


        if domain_valid == True and email_valid == True:
            result = "Domain is valid and email is validated"
            return result

        elif domain_valid == True and email_valid == False:
            result = "Domain is valid and email is not validated"
            return result
        else:
            result = "Domain is not valid and email is not validated"
            return result

    form1 = st.form(key="annotation")
    with form1:

        text = st.text_input("Please enter an email")
        submitted = st.form_submit_button(label="Submit")

    if submitted:

        result = get_values(text)

    c29, c30, c31 = st.columns([1, 1, 2])

    with c29:
        st.write(result)

with tab2:
    uploaded_file = st.file_uploader(
        " ",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        for column in df.columns:
            if is_email(column):

                email_column = column
                st.write(email_column)

        file_container = st.expander("Check your uploaded .csv")
        file_container.write(df)

    else:
        st.info(
            f"""
                👆 Upload a .csv file first.
                """
        )

    def get_values(column_name):
        for index, row in df.iterrows():

            email = row[column_name]

            domain = email.split('@')[1]
            domain_valid = check_email_domain(domain)

            email_valid = validate_email(email)


            if domain_valid == True and email_valid == True:
                df.loc[index, "Domain"] = "Valid"
                df.loc[index, "Valid Check"] = "Valid"

            elif domain_valid == True and email_valid == False:
                df.loc[index, "Domain"] = "Valid"
                df.loc[index, "Valid Check"] = "Invalid"
            else:
                df.loc[index, "Verification"] = "Invalid"

    form2 = st.form(key="annotation2")
    with form2:

        column_names = st.selectbox(
            "Please Select Email Column:", list(df.columns)
        )
        submitted = st.form_submit_button(label="Submit")

    if submitted:

        result = get_values(email_column)

    c29, c30, c31 = st.columns([1, 1, 2])

    with c29:

        CSVButton = download_button(
            df,
            "FlaggedFile.csv",
            "Download to CSV",
        )