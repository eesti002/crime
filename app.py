import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

# loading in the scaler object for scaling features
with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# loading in the saved model
with open('rfc_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

def main():
    

    area_mapping = {
        'Southwest': 3, 'Central': 1,'N Hollywood': 15, 'Mission': 19, 'Devonshire': 17,
        'Northeast': 11, 'Harbor': 5,'Van Nuys': 9, 'West Valley': 10,'West LA': 8, 'Wilshire': 7, 'Pacific': 14, 'Rampart': 2,
        '77th Street': 12, 'Hollenbeck': 4, 'Southeast': 18,'Hollywood': 6,'Newton': 13,'Foothill': 16, 'Olympic': 20, 'Topanga': 21
    }


    status_mapping = {
        'Adult Other': 1, 'Invest Cont': 3,
        'Adult Arrest': 0,'Juvenile Arrest': 4,
        'Juvenile Other': 5,'UNK': 2
        }

    weapon_mapping = {
    'STRONG-ARM (HANDS, FIST, FEET OR BODILY FORCE)': 400,
    'UNKNOWN WEAPON/OTHER WEAPON': 500,
    'No Weapon Found': 0,
    'ROCK/THROWN OBJECT': 306,
    'VERBAL THREAT': 511,
    'FOLDING KNIFE': 204,
    'BLUNT INSTRUMENT': 302,
    'BOTTLE': 212,
    'SEMI-AUTOMATIC PISTOL': 109,
    'CLUB/BAT': 304,
    'OTHER CUTTING INSTRUMENT': 218,
    'HAND GUN': 102,
    'PHYSICAL PRESENCE': 515,
    'VEHICLE': 307,
    'SCISSORS': 216,
    'STICK': 308,
    'MACHETE': 215,
    'OTHER KNIFE': 207,
    'SHOTGUN': 104,
    'ICE PICK': 214,
    'KNIFE WITH BLADE 6INCHES OR LESS': 200,
    'FIRE': 506,
    'GLASS': 221,
    'SIMULATED GUN': 113,
    'KNIFE WITH BLADE OVER 6 INCHES IN LENGTH': 201,
    'DEMAND NOTE': 504,
    'BOMB THREAT': 501,
    'PIPE/METAL PIPE': 312,
    'UNKNOWN FIREARM': 106,
    'MACE/PEPPER SPRAY': 512,
    'HAMMER': 311,
    'RAZOR': 208,
    'OTHER FIREARM': 107,
    'BELT FLAILING INSTRUMENT/CHAIN': 301,
    'UNKNOWN TYPE CUTTING INSTRUMENT': 223,
    'SCREWDRIVER': 219,
    'KITCHEN KNIFE': 205,
    'AIR PISTOL/REVOLVER/RIFLE/BB GUN': 114,
    'BRASS KNUCKLES': 303,
    'REVOLVER': 101,
    'SWITCH BLADE': 206,
    'STUN GUN': 513,
    'AXE': 211,
    'RIFLE': 103,
    'ASSAULT WEAPON/UZI/AK47/ETC': 115,
    'ANTIQUE FIREARM': 116,
    'FIXED OBJECT': 305,
    'SEMI-AUTOMATIC RIFLE': 110,
    'CAUSTIC CHEMICAL/POISON': 503,
    'TIRE IRON': 514,
    'MARTIAL ARTS WEAPONS': 508,
    'CONCRETE BLOCK/BRICK': 310,
    'BOARD': 309,
    'DIRK/DAGGER': 203,
    'TOY GUN': 112,
    'MAC-11 SEMIAUTOMATIC ASSAULT WEAPON': 120,
    'EXPLOXIVE DEVICE': 505,
    'HECKLER & KOCH 93 SEMIAUTOMATIC ASSAULT RIFLE': 122,
    'SAWED OFF RIFLE/SHOTGUN': 105,
    'DOG/ANIMAL (SIC ANIMAL ON)': 516,
    'SYRINGE': 220,
    'SCALDING LIQUID': 510,
    'RAZOR BLADE': 210,
    'CLEAVER': 213,
    'ROPE/LIGATURE': 509,
    'BOW AND ARROW': 502,
    'AUTOMATIC WEAPON/SUB-MACHINE GUN': 108,
    'LIQUOR/DRUGS': 507,
    'SWORD': 217,
    'M1-1 SEMIAUTOMATIC ASSAULT RIFLE': 123,
    'STARTER PISTOL/REVOLVER': 111,
    'MAC-10 SEMIAUTOMATIC ASSAULT WEAPON': 119,
    'BOWIE KNIFE': 202,
    'STRAIGHT RAZOR': 209,
    'BLACKJACK': 300,
    'RELIC FIREARM': 125,
    'HECKLER & KOCH 91 SEMIAUTOMATIC ASSAULT RIFLE': 121,
    'UZI SEMIAUTOMATIC ASSAULT RIFLE': 118,
    'UNK TYPE SEMIAUTOMATIC ASSAULT RIFLE': 117,
    'M-14 SEMIAUTOMATIC ASSAULT RIFLE': 124
    }
    day_of_week_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    direction_mapping = {'Unknown':0, 'East':1, 'West':2, 'North':3, 'South':4}
    month_mapping = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    location_type_mapping = {'Crossroad': 0, 'Building Block': 1}

    st.sidebar.title("Crime Prediction App")
    st.sidebar.header("Navigation")
    selected_option = st.sidebar.radio("Select an option", ["Project Description", "Developer Info", "Crime Prediction App"])

    # About the Project section
    if selected_option == "Project Description":
        st.title("About the Project")
        st.write("This is a Crime Prediction Model project.")
        # Add more information about the project here

    # Student Info section
    elif selected_option == "Developer Info":
        st.title("Developer Info")
        st.write("Student Name: John Doe")
        st.write("Student ID: 123456")
        # Add more student information here
        
    
    elif selected_option == "Crime Prediction App":

        st.title("Crime Prediction Model")
        # Creating form for input fields
        with st.form(key='crime_input_form'):
            time_occ = st.time_input("Time of Occurrence")
            vict_age = st.number_input("Victim's Age", min_value=0, max_value=120, step=1)
            area = st.selectbox("Area Name", options= area_mapping.keys())
            rpt_dist_no = st.selectbox("Report District Number", ['1','2', '3', '4','5', '6', '7', 'Unknown'])
            location = st.selectbox("Location of Incident", options = location_type_mapping.keys())
            weapon_used = st.selectbox("Weapon Used During Incident", options = weapon_mapping.keys())
            part_1_2 = st.selectbox("Part 1-2", options=['Part 1', 'Part 2'])
            status = st.selectbox("Incident Status", options=status_mapping.keys())
            days_since_reference_date_occ = st.number_input("Number of Days Since Incident Occured", step= 1)
            days_since_reference_date_rptd = st.number_input("Number of Days Since Incident Reported",  step=1)
            month = st.selectbox("Month", options = month_mapping.keys())
            day = st.selectbox("Day of Week", options = day_of_week_mapping.keys())
            lat = st.number_input("Latitude", format="%.6f", min_value=0.0, max_value=34.3343)
            lon = st.number_input("Longitude", format="%.6f", min_value=-118.6676, max_value=0.0)
            direction = st.selectbox("Direction", options=direction_mapping.keys())

            # submit button
            submit_button = st.form_submit_button(label='Predict')

        if submit_button:
            # Process the input data
            # You can also call the prediction function here
            st.write("Processing your input...")

            # trying to collect the time of day of occurance, eg = Morning or Afternoon or Evening or Night
            hour_of_day = time_occ.hour
            # converting it to
            if hour_of_day < 6:
                day_division = 0
            elif hour_of_day > 6 and hour_of_day < 12:
                day_division = 1
            elif hour_of_day > 12 and hour_of_day < 18:
                day_division = 2
            else:
                day_division = 3

            # handling the district number feature
            if rpt_dist_no == 'Unknown':
                rpt_dist_no = 0
            else:
                int(rpt_dist_no)

            # Convert to string (if not already) and remove colons
            formatted_time = str(time_occ).replace(':', '')
            area = area_mapping[area]
            day = day_of_week_mapping[day]
            month = month_mapping[month]
            location = location_type_mapping[location]
            direction = direction_mapping[direction]
            formatted_time = int(formatted_time[:4])
            part_1_2 = int(part_1_2[-1])
            weapon_used = weapon_mapping[weapon_used]
            status = status_mapping[status]


            # Column names
            columns = ['time occ', 'vict age', 'direction_0', 'area', 'days_since_reference_date_rptd', 'Weapon Used Cd', 
            'days_since_reference_date_occ', 'rpt dist no', 'status', 'part 1-2', 'day_of_week_encoded', 
            'month_encoded', 'day_division_encoded', 'lat', 'lon',]


            features = [formatted_time, vict_age, direction, area, days_since_reference_date_rptd, weapon_used, 
            days_since_reference_date_occ, rpt_dist_no, status, part_1_2, day, month, day_division, lat, lon]

            # Create the DataFrame
            df = pd.DataFrame([features], columns=columns)

            # scaling the numerical columns 
            numeric_columns = ['days_since_reference_date_rptd', 'days_since_reference_date_occ', 'vict age', 'area', 'part 1-2', 'lat', 'lon', 
                    'day_of_week_encoded', 'month_encoded', 'day_division_encoded', 'direction_0']
            
            df[numeric_columns]= scaler.transform(df[numeric_columns])
            df = df.rename(columns={'day_of_week_encoded': 'day_of_week'})
            print(model.predict(df))

        # features to feed the prediction model
       







if __name__ == "__main__":
    main()
