import streamlit as st
from streamlit_folium import folium_static
import folium
import requests
import wikipedia
import numpy as np
import qrcode
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from PIL import Image
apiKey = 'b7936863179b455e9c8cd404e653d48f'
def predict(testing_image):
    label_dict = {0: "Amber Fort",
                  1: "Brihadeeswarar Temple",
                  2: "Fatehpur Sikri",
                  3: 'Golden Temple',
                  4: "Hawa Mahal",
                  5: "Humayun's Tomb",
                  6: "Lotus Bahai Temple",
                  7: "Meenakshi Amman Temple",
                  8: " Mysore Palace",
                  9: "Purana Qila",
                  10: "Qutb Minar, Delhi",
                  11: "Safdarjung's Tomb",
                  12: "Sanchi Stupa",
                  13: " Taj Mahal",
                  14: "Virupaksha Temple"}

    model = load_model(r'C:\Users\jacob\OneDrive\Desktop\College\Major_Project_7th_SEM\vgg16_trained_model.h5')
    image = Image.open(testing_image).convert('RGB')
    image = image.resize((224, 224))
    image = np.array(image, dtype = 'float32')/255.0
    image = image.reshape(1, 224, 224, 3)
    result = model.predict(image).argmax()
    return label_dict[result]

def make_qr_code(direction):
    qr = qrcode.QRCode(version=1,
                            box_size=5,
                            border=1)
    qr.add_data(direction)
    qr.make(fit=True)
    img = qr.make_image(fill_color='white',
                                back_color='black')
    return img

def location_map(url):
    response = requests.get(url)
    data = response.json()
    lat = data['features'][0]['properties']['lat']
    lon = data['features'][0]['properties']['lon']
    m = folium.Map(location=[lat, lon], zoom_start=16)
    tooltip = "Liberty Bell"
    folium.Marker(
        [lat, lon], popup="Liberty Bell", tooltip=tooltip
    ).add_to(m)
    return m,lat,lon

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: #FFFAFA;font-size:50px;'>Itihas Darshan: Monument Recognition</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(['Prediction', 'Location'])
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        image = st.file_uploader('Upload Image', type=['jpg', 'jpeg', 'png'],label_visibility="hidden")
        if image is not None:
            st.image(Image.open(image),use_column_width='always')
    with col2:
        if image is not None:
            place = predict(image)
            # Prediction
            if st.button('Result', help='Prediction'):
                st.success(predict(image))
                st.markdown(f"<h2 style='color:#C0C0C0;font-size:40px;'>Information About {place}</h2>", unsafe_allow_html=True)
                if place == 'Qutb Minar, Delhi':
                    place = 'Qutab Minar'
                elif place == "Lotus Bahai Temple":
                    place = 'Lotus Temple'
                page = wikipedia.page(place, auto_suggest=False)
                result = page.summary
                st.markdown("""
                    <style>
                    .big-font {
                        font-size:22px !important;  
                    }
                    </style>
                    """, unsafe_allow_html=True)
                st.write(f'<p class="big-font">{result}</p>', unsafe_allow_html=True)
            else:
                page = wikipedia.page(place, auto_suggest=False)
                result = page.summary
                st.write(result)

try:
    if place == "Golden Temple":
        place = "Shri Harmandir Sahib"
    if place == "Qutab Minar":
        place = "Qutab Minar, Delhi"
    if place == " Taj Mahal":
        place = "Taj Mahal, Agra"
    if place == "Brihadeeswarar Temple":
        place = "Brihadeeswarar Temple, Thanjavur"
    url = f'https://api.geoapify.com/v1/geocode/search?text={place},India&apiKey={apiKey}'
    with tab2:
        col1, col2 = st.columns([3, 1])
        if  place == "Shri Harmandir Sahib":
            place = "Golden Temple"
        with col1:
            st.header(f'Location to {place}')
            m,lat,lon = location_map(url)
            folium_static(m,width=1000,height=500)

        dir = f'https://maps.google.com/?daddr={lat},{lon}'
        with col2:
            st.subheader(f'Route to {place}')
            np_img = np.array(make_qr_code(dir))
            st.image(np_img,use_column_width='always')
except NameError:
     st.info("Please Upload Image to proceed with Prediction")

