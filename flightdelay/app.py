import streamlit as st
import datetime
from data.options_distance_lookup import *
import base64
import requests
import numpy as np
import time

def get_day_of_week(date):
    day_num = date.weekday() + 1
    return day_num

def get_month_number(date):
    return date.month

@st.cache_data
def get_delay_output(airline, origin, destination, departure_time, arrival_time, day_of_week, month, distance_group):

    flight_params = {
        "airline": airline,
        "origin": origin,
        "destination": destination,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "day_of_week": day_of_week,
        "month": month,
        "distance_group": distance_group
    }

    url = "https://flight-delay-1234-oloqibljcq-ew.a.run.app/request"

    response = requests.get(url, params=flight_params)

    if response.status_code == 200:
        predicted_delay = response.json().get('result')
        predicted_prob = response.json().get('prob')
    else:
        return "ERROR"

    # predicted_delay = 160

    if predicted_delay == '1':
        message1 ="DELAYED"
        message2 = f"We predict your flight to be delayed with a probability of {predicted_prob}%!"
        color = 'red'
    else:
        message1 ="ON TIME"
        message2 = f"We predict your flight will be on time with a probability of {predicted_prob}%!"
        color = 'green'

    st.markdown(
        f"""
        <div style="text-align: center; font-size: 24px; padding: 10px; color: #f0f0f0; background-color: {color}; border-radius: 5px;">
            {message1}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 24px; padding: 10px; color: black; border-radius: 5px;">
            {message2}
        </div>
        """,
        unsafe_allow_html=True
    )
@st.cache_data
def load_available_options():
    return get_available_options()

available_options = load_available_options()

def get_time_bracket(selected_time):
    time_brackets = [
        '0001-0559', '0600-0659', '0700-0759', '0800-0859', '0900-0959', '1000-1059', '1100-1159',
        '1200-1259', '1300-1359', '1400-1459', '1500-1559', '1600-1659', '1700-1759',
        '1800-1859', '1900-1959', '2000-2059', '2100-2159', '2200-2259', '2300-2359'
    ]
    time_str = selected_time.strftime("%H%M")
    if time_str == '0000':
        return '0001-0559'
    else:
        for time_range in time_brackets:
            start, end = time_range.split('-')
            if int(start) <= int(time_str) <= int(end):
                return time_range
    return 'Invalid Time'


# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
# Streamlit app
# @st.cache
def main():
#     bin_str = get_base64('airport.png')
#     page_bg_img = '''
#     <style>
#     .stApp {
#         background-image: url("data:image/png;base64,%s");
#         background-size: cover;
#     }
#     .boxed-title {
#     padding: 10px;
#     text-align: center;
#     color: #FFFFFF;
#     border-radius: 5px;
# }
#     </style>
#     ''' % bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center;'><h1>Predict the delay of your flight!</h1></div>",
        unsafe_allow_html=True
    )
    # st.markdown(
    #     "<div class='boxed-text'><h2>Enter your flight details below.</h2></div>",
    #     unsafe_allow_html=True
    # )
    # st.markdown(
    #     "<div class='boxed-text'><h2>Enter your flight details below.</h2></div>",
    #     unsafe_allow_html=True
    # )

    # default_origin = "ATL"
    # default_destination = "JFK"
    # default_airline = "DL"
    default_departure_time = "07:00 PM"
    default_arrival_time = "11:00 PM"
    default_departure_date = datetime.date.today() + datetime.timedelta(days=16)
    default_origin = "Los Angeles, CA"
    default_airline = "Southwest Airlines Co."
        # Input components

    col1, col2 = st.columns([1, 1])
    with col1:

        origin_city = st.selectbox("Origin",  options=list(available_options.keys()), index=list(available_options.keys()).index(default_origin) if default_origin in available_options.keys() else 0)
        if origin_city:
            destination_options = list(available_options[origin_city].keys())
            destination_city = st.selectbox("Destination", options=destination_options)
            if destination_city:
                airline_options = available_options[origin_city][destination_city]
                airline = st.selectbox("Airline", options=airline_options, index=airline_options.index(default_airline) if default_airline in airline_options else 0)
    with col2:
        time_options = [datetime.time(hour, minute) for hour in range(24) for minute in range(0, 60, 15)]
        formatted_time_options = [time.strftime("%I:%M %p") for time in time_options]
        departure_date = st.date_input("Date", value=default_departure_date)
        departure_time = st.selectbox("Departure Time", options=formatted_time_options, index=formatted_time_options.index(default_departure_time))
        arrival_time = st.selectbox("Arrival Time", options=formatted_time_options, index=formatted_time_options.index(default_arrival_time))


 # Button to trigger prediction
    if st.button("Predict Delay"):
        progress_bar = st.progress(0)

        for i in range(100):
            # Update progress bar.
            progress_bar.progress(i + 1)

            # Pretend we're doing some computation that takes time.
            time.sleep(0.01)

        if departure_date and departure_time and arrival_time and airline and origin_city and destination_city:
            selected_departure_time = datetime.datetime.strptime(departure_time, "%I:%M %p").time()
            selected_arrival_time = datetime.datetime.strptime(arrival_time, "%I:%M %p").time()

            origin = get_airport_code(origin_city)
            destination = get_airport_code(destination_city)
            airline = get_airline_code(airline)
            distance_group = get_distance_groups(origin, destination)

            day_of_week = get_day_of_week(departure_date)
            month_number = get_month_number(departure_date)

            departure_bracket = get_time_bracket(selected_departure_time)
            arrival_bracket = get_time_bracket(selected_arrival_time)


            get_delay_output(
                    airline, origin, destination, departure_bracket, arrival_bracket,
                    day_of_week, month_number, distance_group
                )

            st.balloons()


    st.markdown('#####')
    st.markdown('***')
    left_co, cent_co,last_co = st.columns(3)

    with cent_co:
        st.image("flightdelay/le_voyage.jpg")

if __name__ == "__main__":
    main()
