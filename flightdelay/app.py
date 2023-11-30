import streamlit as st
import datetime
from data.options_distance_lookup import *
import requests

def get_day_of_week(date):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_num = date.weekday()
    return days[day_num]

def get_month_number(date):
    return date.month


def get_delay_output(airline, origin, destination, departure_time, arrival_time, day_of_week, month):

    # flight_data = {
    #     "airline": airline,
    #     "origin": origin,
    #     "destination": destination,
    #     "departure_bracket": departure_time,
    #     "arrival_bracket": arrival_time,
    #     "day_of_week": day_of_week,
    #     "month_number": month
    # }

    # url = "#### EXAMPLE #####"

    # response = requests.get(url, params=flight_data)

    # if response.status_code == 200:
    #     predicted_delay = response.json().get("predicted_delay")
    # else:
    #     return "ERROR"

    predicted_delay = 160

    if predicted_delay > 15:
        message = f"We predict your flight to be delayed by: {predicted_delay} minutes"
        color = 'red'
    else:
        message = "We predict your flight will be on time!"
        color = 'green'

    st.markdown(
        f"""
        <div style="text-align: center; font-size: 24px; padding: 10px; color: #f0f0f0; background-color: {color}; border-radius: 5px;">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )

available_options = get_available_options()

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

# Streamlit app
def main():
    st.markdown(
        """
        <style>
        body {
            background-color: red;
            color: white;
        }
        h1 {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("Flight Delay Prediction App")
    st.markdown("<h2 style='text-align: center;'>Welcome to the Flight Delay Prediction App!<br>Enter the details below to predict the delay of your flight.</h2>", unsafe_allow_html=True)

    # default_origin = "ATL"
    # default_destination = "JFK"
    # default_airline = "DL"
    # default_departure_time = "08:00 AM"
    # default_arrival_time = "04:00 PM"
    default_departure_date = datetime.date.today() + datetime.timedelta(days=1)

        # Input components
    col1, col2 = st.columns([1, 1])
    with col1:
        origin_city = st.selectbox("Origin Airport", options=available_options.keys())
        destination_city = st.selectbox("Destination Airport", options=available_options[origincityname].keys())
        airline = st.selectbox("Airline Code", options=available_options[origincityname][destcityname])
    with col2:
        time_options = [datetime.time(hour, minute) for hour in range(24) for minute in range(0, 60, 15)]
        formatted_time_options = [time.strftime("%I:%M %p") for time in time_options]
        departure_date = st.date_input("Departure Date", value=default_departure_date)
        departure_time = st.selectbox("Departure Time", options=formatted_time_options)
        arrival_time = st.selectbox("Arrival Time", options=formatted_time_options)


 # Button to trigger prediction
    if st.button("Predict Delay"):
        if departure_date and departure_time and arrival_time and airline and origin_city and destination_city:
            selected_departure_time = datetime.datetime.strptime(departure_time, "%I:%M %p").time()
            selected_arrival_time = datetime.datetime.strptime(arrival_time, "%I:%M %p").time()

            origin = get_airport_code(origin_city)
            destination = get_airport_code(destination_city)
            airline = get_airline_code(airline)

            day_of_week = get_day_of_week(departure_date)
            month_number = get_month_number(departure_date)

            departure_bracket = get_time_bracket(selected_departure_time)
            arrival_bracket = get_time_bracket(selected_arrival_time)

            get_delay_output(
                    airline, origin, destination, departure_bracket, arrival_bracket,
                    day_of_week, month_number
                )

if __name__ == "__main__":
    main()
