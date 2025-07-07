import streamlit as st
import pandas as pd
from streamlit import session_state as ss

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stActionButtonIcon {visibility: hidden;}
    .css-eczf16 {display: none}  /* Hides the GitHub, Share, etc. icons */
    </style>
""", unsafe_allow_html=True)

if 'authentication_status' not in ss:
    st.switch_page('./pages/Account.py')
elif ss['authentication_status'] is None:
    st.switch_page('./pages/Account.py')
else:
    #set the page as wide
    st.title('Powerplant Forecasting')

    data, approach, models, test = st.tabs(['Data', 'Approach', 'Models', 'Results'])

    with data:
        st.info('Considered the demand, actual and forecast data for the months of January, February, and March 2022.')
        with st.expander('January 2022'):
            df = pd.read_csv('data/jan_actuals.csv')
            st.dataframe(df, hide_index=True)

        with st.expander('February 2022'):
            df = pd.read_csv('data/feb_actuals.csv')
            st.dataframe(df, hide_index=True)

        with st.expander('March 2022'):
            df = pd.read_csv('data/mar_actuals.csv')
            st.dataframe(df, hide_index=True)

    with approach:
        st.subheader('Adaptive Automated Time Series Forecasting Framework')

        #display image
        st.image('assets/ts_framework.png', use_container_width=True)

        st.info("Training Start Date: 01-01-2022")
        st.success("Training End Date: 14-03-2022")
        st.warning("Testing Start Date: 15-03-2022")
        st.info("Training window: Last 75 days")
        st.success("Forecasting window: 1 day (96 blocks)")

    with models:
        st.subheader('Models Used')
        model_df = pd.read_csv('data/models.csv')
        st.dataframe(model_df, hide_index=True)

    with test:
        st.subheader('Model Testing')
        st.info('The model was tested on the actual data for the month of March 2022.')
        result = pd.read_csv('data/actuals_forecast_comparison.csv')

        overall_deviation_df = pd.DataFrame({'Average Absolute Deviation (Original)': [result['Absolute_Deviation_original'].abs().mean()], 
                                            'Average Absolute Deviation (Model)': [result['Absolute_Deviation_model'].abs().mean()],
                                            'Average Deviation Percentage (Original)': [result['Absolute_Percentage_Deviation_original'].mean()],
                                            'Average Deviation Percentage (Model)': [result['Absolute_Percentage_Deviation_model'].mean()]})
        
        #round the values to 2 decimal places
        overall_deviation_df['Average Absolute Deviation (Original)'] = overall_deviation_df['Average Absolute Deviation (Original)'].apply(lambda x: round(x, 2))
        overall_deviation_df['Average Absolute Deviation (Model)'] = overall_deviation_df['Average Absolute Deviation (Model)'].apply(lambda x: round(x, 2))

        #make the percentage formatting in the dataframe only for the percentage columns
        overall_deviation_df['Average Deviation Percentage (Original)'] = overall_deviation_df['Average Deviation Percentage (Original)'].apply(lambda x: "{:.2f}%".format(x))
        overall_deviation_df['Average Deviation Percentage (Model)'] = overall_deviation_df['Average Deviation Percentage (Model)'].apply(lambda x: "{:.2f}%".format(x))

        overall_deviation_df = overall_deviation_df.T
        overall_deviation_df.columns = ['Values']
        st.dataframe(overall_deviation_df)  

        #group the data by Date and calculate the mean of the Absolute_Deviation_original, Absolute_Deviation_model, Absolute_Percentage_Deviation_original, and Absolute_Percentage_Deviation_model
        deviation_df = result.groupby('Date')[['Absolute_Deviation_original', 'Absolute_Deviation_model', 'Absolute_Percentage_Deviation_original', 'Absolute_Percentage_Deviation_model']].mean()

        
        #plot not a stacked bar chart to compare the Average Deviation Percentage (Original) and Average Deviation Percentage (Model) and have the format as a percentage
        st.bar_chart(deviation_df[['Absolute_Percentage_Deviation_original', 'Absolute_Percentage_Deviation_model']], stack=False, y_label='Percentage (%)')
            

        st.subheader('Daily Forecast Analysis')
        #dropdown to select date from 15-03-2022 to 31-03-2022
        date = st.selectbox('Select Date', result['Date'].unique())

        #filter data based on selected date 
        filtered_data = result[result['Date'] == date]
        st.subheader("Forecast Output")
        st.dataframe(filtered_data, hide_index=True)

        st.subheader("Block-wise Forecast for the day")

        #plot Power_Consumption, Original_Forecast, and Model_Forecast in a line chart
        st.line_chart(filtered_data[['Power_Consumption', 'Original_Forecast', 'Model_Forecast']])

        #put the above values in a dataframe
        deviation_df = pd.DataFrame({'Average Absolute Deviation (Original)': [filtered_data['Absolute_Deviation_original'].abs().mean()],
                                        'Average Absolute Deviation (Model)': [filtered_data['Absolute_Deviation_model'].abs().mean()],
                                        'Average Deviation Percentage (Original)': [filtered_data['Absolute_Percentage_Deviation_original'].mean()],
                                        'Average Deviation Percentage (Model)': [filtered_data['Absolute_Percentage_Deviation_model'].mean()]})
        
        #round the values to 2 decimal places
        deviation_df['Average Absolute Deviation (Original)'] = deviation_df['Average Absolute Deviation (Original)'].apply(lambda x: round(x, 2))
        deviation_df['Average Absolute Deviation (Model)'] = deviation_df['Average Absolute Deviation (Model)'].apply(lambda x: round(x, 2))

        #make the percentage formatting in the dataframe only for the percentage columns
        deviation_df['Average Deviation Percentage (Original)'] = deviation_df['Average Deviation Percentage (Original)'].apply(lambda x: "{:.2f}%".format(x))
        deviation_df['Average Deviation Percentage (Model)'] = deviation_df['Average Deviation Percentage (Model)'].apply(lambda x: "{:.2f}%".format(x))

        deviation_df = deviation_df.T
        deviation_df.columns = ['Values']
        st.dataframe(deviation_df)
        

        #plot the Deviation_original and Deviation_model in a line chart
        st.line_chart(filtered_data[['Deviation_original', 'Deviation_model']])




        

