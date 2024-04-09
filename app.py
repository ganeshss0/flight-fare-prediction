from flight.utility import load_object, read_yaml
from flight.components.data_transformation import DataTransformation
from flight.logger import logging
import streamlit as st
from flight.constants import (
    START_DATE, SCHEMA_FILE_PATH, HOURS_STRINGS, MINUTES_STRINGS
    )
from time import sleep

schema = read_yaml(SCHEMA_FILE_PATH)


if __name__ == '__main__':
    logging.info('Starting Streamlit Page')

    # Page Config
    st.set_page_config(page_title='Flight Price Predictor', page_icon='templates/images/page_icon.jpg')
    # Adding Image to page
    st.image('templates/images/bg.jpg')
    # Title 
    st.title('Flight Price Predictor')

    st.info('Flight Price Predictor is a machine learning model that predicts the price of flights based on the given inputs.')
    st.sidebar.title('Ganesh')
    github_url = 'https://github.com/ganeshss0/flight-fare-prediction'
    linkedin_url = 'https://linkedin.com/in/ganesh0'
    st.sidebar.markdown(f'[GitHub Repo]({github_url})')
    st.sidebar.markdown(f'[Linkedin]({linkedin_url})')
    

    # Srouce Selectbox
    source = st.selectbox(
        "Source",
        options=schema['Source'],
        key='Source',
        help="""Select the source of the flight."""
    )
    # destination Selectbox
    destination = st.selectbox(
        'Destination',
        options=schema['Destination'],
        index=1,
        help="""Select the destination of the flight."""
    )



    dep_1, dep_2, dep_3 = st.columns(3)

    date_of_journey = dep_1.date_input(
        "Date of Journey", 
        min_value=START_DATE,
        help='''Select date of journey.'''
    )
    departure_hour = dep_2.selectbox(
        "Departure Time (Hour)",
        HOURS_STRINGS,
        help='Select depature time.'
    )
    departure_minute = dep_3.selectbox(
        "Departure Time (Minute)",
        MINUTES_STRINGS,
        help='Select depature time.'
    )


    avl_1, avl_2, avl_3 = st.columns(3)

    arrive_next_day = avl_1.checkbox(
        'Next Day',
        help='Flight arrive at next day.'
    )
    arrival_hour = avl_2.selectbox(
        "Arrival Time (Hour)",
        HOURS_STRINGS,
        help='Select arrival time.',
    )
    arrival_minute = avl_3.selectbox(
        "Arrival Time (Minute)",
        MINUTES_STRINGS,
        help='Select arrival time.',
    )

    stops = st.selectbox(
        'Stops',
        ['non-stop', '1 stop', '2 stops', '3 stops', '4 stops'],
        help='Select number of stops in flight.'
    )
    airline = st.selectbox(
        'Airline',
        options=schema['Airlines'],
        help='Select flight airline.'
    )

    



    # button to trigger predictions
    if st.button("Predict Price"):
        # Data User entered

        if source == destination:
            logging.warning('Source and Destination entered by user are same.')
            st.error('Source and Destination are same.')

        elif (departure_hour == arrival_hour) and (departure_minute == arrival_minute):
            logging.warning('Deparuture Time and Arrival Time entered by user are same.')
            st.error('Depature Time and Arrival Time are same.')
        else:
            progressbar = st.progress(0)
            status = st.empty()
            raw_data = {
                'Airline' : airline,
                'Date_of_Journey': date_of_journey,
                'Source' : source,
                'Destination' : destination,
                'Dep_Hour' : departure_hour,
                'Dep_Min' : departure_minute,
                'Arrival_Hour' : arrival_hour,
                'Arrival_Minute' : arrival_minute,
                'Total_Stops' : stops,
                'Arrive_Next_Day' : arrive_next_day
            }
            logging.info(f'User Request: {raw_data}')
            logging.info('Transforming Data')
            data_transformation = DataTransformation(raw_data)
            transformed_data = data_transformation.transform()
            
            model_path = './models/model.joblib'
            logging.info('Loading the model')
            model = load_object(model_path)
            logging.info('Model Predicting...')
            pred = model.predict(transformed_data)
            import time
            logging.info(f'Prediction Result: {pred}')

            for i in range(100):
                sleep(0.015)
                progressbar.progress(i+1)
                status.text(f'Progress: {i+1}%')
            status.text('Complete')

            st.success(f"Predicted Price: $ {pred[0]:.2f}")