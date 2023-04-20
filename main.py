from validate_email import validate_email
import dns.resolver
import streamlit as st
import pandas as pd
from functionforDownloadButtons import download_button
import time
df = pd.DataFrame()
result = "Your answer will appear here "
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
with st.sidebar:
   st.subheader("Credit: Sweephy.com")
   st.caption("No-code data preparing, cleaning and ML platform")
   st.caption("Contact: info@sweephy.com")
   st.divider()
   st.subheader("Check other free tools")
   st.write("[Data Profiling](https://upcoming.sweephy.com/profiling)")
   st.write("[Text Classification](https://upcoming.sweephy.com/text-classification)")
   st.write("[Data Visualization](https://upcoming.sweephy.com/text-classification)")
   st.info(f"""
            👆 Check all other [ML modules](https://www.sweephy.com/module-integrations)
            """
           )


def check_email_domain(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return True if records else False
    except dns.resolver.NXDOMAIN:
        return False
tab1, tab2, tab3 = st.tabs(["CSV Email Verifier", "Excel Email Verifier", "One Email"])
with tab3:
    st.subheader('Welcome to :blue[Sweephy] _Email Verifier_ :smiley:')
    st.text("To start, please write an _Email_.")
    def get_values(email):
        try:
            domain = email.split('@')[1]
            domain_valid = check_email_domain(domain)

            email_valid = validate_email(email)


            if domain_valid == True and email_valid == True:
                result = "Domain is valid and email is validated"
                return result

            elif domain_valid == True and email_valid == False:
                result = "Domain is valid and email is NOT validated"
                return result
            else:
                result = "Domain is not valid and email is NOT validated"
                return result
        except:

            st.error('Please enter a valid email!')


    form1 = st.form(key="annotation")
    with form1:

        text = st.text_input("Please enter an email")
        submitted = st.form_submit_button(label="Submit")

    if submitted:

        result = get_values(text)

    st.info(result + " :star:")

with tab1:
    st.subheader('Welcome to :blue[Sweephy] _Email Verifier_ :smiley:')
    st.text("To start, please upload a CSV file and select the _Email_ column.")
    uploaded_file = st.file_uploader(
        " ",
        key="1",
        type="CSV",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)


        file_container = st.expander("Check your uploaded .csv")
        file_container.write(df)

    else:
        st.info(
            f"""
                👆 Upload a .csv file first.
                """
        )




    def get_values(column_name):
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        total_rows = len(df)
        progress_step = 1 / total_rows
        progress_value = 0
        for index, row in df.iterrows():
            try:
                progress_value += progress_step
                my_bar.progress(progress_value,text=progress_text)

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
            except:
                continue

    form2 = st.form(key="annotation2")
    with form2:

        column_names = st.selectbox(
            "Please Select Email Column:", list(df.columns)
        )
        submitted = st.form_submit_button(label="Submit")

    if submitted:

        result = get_values(column_names)
        st.success('Operation is done! You can download flagged CSV file.', icon="✅")

    c29, c30, c31 = st.columns([1, 1, 2])

    with c29:
        CSVButton = download_button(
            df,
            "FlaggedFile.csv",
            "Download to CSV",
        )

with tab2:
    st.subheader('Welcome to :blue[Sweephy] _Email Verifier_ :smiley:')
    st.text("To start, please upload an Excel file and select the _Email_ column.")
    uploaded_file = st.file_uploader(
        " ",
        type="xlsx",
        key="2",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        uploaded_file.seek(0)


        file_container = st.expander("Check your uploaded .csv")
        file_container.write(df)

    else:
        st.info(
            f"""
                👆 Upload a Excel file first.
                """
        )




    def get_values(column_name):
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        total_rows = len(df)
        progress_step = 1 / total_rows
        progress_value = 0
        for index, row in df.iterrows():
            try:
                progress_value += progress_step
                my_bar.progress(progress_value,text=progress_text)

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
            except:
                continue
    form2 = st.form(key="annotation3")
    with form2:

        column_names = st.selectbox(
            "Please Select Email Column:", list(df.columns)
        )
        submitted = st.form_submit_button(label="Submit")

    if submitted:

        result = get_values(column_names)
        st.success('Operation is done! You can download flagged CSV file.', icon="✅")

    c29, c30, c31 = st.columns([1, 1, 2])

    with c29:
        CSVButton = download_button(
            df,
            "FlaggedFile.csv",
            "Download to CSV",
        )