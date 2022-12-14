import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
#import tensorflow as tf
#tf.keras.utils.custom_object_scope
#from tensorflow import keras
#import keras
#from keras.utils.np_utils import to_categorical
#from keras.utils import to_categorical
#from keras.models import Sequential
#from tensorflow.keras.model import backend as K
#import os
#import time
#import io
from PIL import Image
import plotly.express as px


def render_header():
    st.write("""
        <p align="center"> 
            <H1> Skin cancer Analyzer 
        </p>

    """, unsafe_allow_html=True)

@st.cache
def load_mekd():
    img = Image.open('images.jpg')
    return img

@st.cache
def data_gen(x):
    img = np.asarray(Image.open(x).resize((100, 75)))
    x_test = np.asarray(img.tolist())
    x_test_mean = np.mean(x_test)
    x_test_std = np.std(x_test)
    x_test = (x_test - x_test_mean) / x_test_std
    x_validate = x_test.reshape(1, 75, 100, 3)

    return x_validate

@st.cache
def data_gen_(img):
    img = img.reshape(100,75)
    x_test = np.asarray(img.tolist())
    x_test_mean = np.mean(x_test)
    x_test_std = np.std(x_test)
    x_test = (x_test - x_test_mean) / x_test_std
    x_validate = x_test.reshape(1, 75, 100, 3)

    return x_validate


def load_models():
    #global model
#     from pathlib import Path
#     path_name = "https://github.com/Html5intheway4/streamlit_app/blob/3150f69b911fd1763edddc35051f17c790422bca/model.h5"
#     p = Path(path_name)
#     if p.is_file():
#         print("File exists")
#         model = tf.keras.models.load_model(path_name)    
#         #Execute other file operations here
        
    
#     else:
#         print("File does not exist! IOError has occured")

    model = tf.keras.models.load_model("model.h5")
    return model

# def load_models():
#     model = load_model('model.h5')
#     return model



@st.cache
def predict(x_test, model):
    #import tensorflow as tf
    Y_pred = model.predict(x_test)
    #ynew = model.predict_proba(x_test)
    ynew = model.predict(x_test)
    tf.keras.backend.clear_session()
    #K.clear_session()
    ynew = np.round(ynew, 2)
    ynew = ynew*100
    y_new = ynew[0].tolist()
    Y_pred_classes = np.argmax(Y_pred, axis=1)
    tf.keras.backend.clear_session()
    #K.clear_session()
    return y_new, Y_pred_classes


@st.cache
def display_prediction(y_new):
    """Display image and preditions from model"""

    result = pd.DataFrame({'Probability': y_new}, index=np.arange(7))
    result = result.reset_index()
    result.columns = ['Classes', 'Probability']
    lesion_type_dict = {2: 'Benign keratosis-like lesions', 4: 'Melanocytic nevi', 3: 'Dermatofibroma',
                        5: 'Melanoma', 6: 'Vascular lesions', 1: 'Basal cell carcinoma', 0: 'Actinic keratoses'}
    result["Classes"] = result["Classes"].map(lesion_type_dict)
    return result


def main():
    st.sidebar.header('Skin cancer Analyzer by Aman Prakash Kanth')
    st.sidebar.subheader('Choose a page to proceed:')
    page = st.sidebar.selectbox("", ["Sample Data", "Upload Your Image"])
    st.sidebar.subheader('This is the demo web app for skin cancer detection by AmanPKanth')

    if page == "Sample Data":
        st.header("Sample Data Prediction for Skin Cancer")
        st.markdown("""
        **Now, this is probably why you came here. Let's get you some Predictions**

        You need to choose Sample Data
        """)

        mov_base = ['Sample Data I']
        movies_chosen = st.multiselect('Choose Sample Data', mov_base)

        if len(movies_chosen) > 1:
            st.error('Please select Sample Data')
        if len(movies_chosen) == 1:
            st.success("You have selected Sample Data")
        else:
            st.info('Please select Sample Data')

        if len(movies_chosen) == 1:
            if st.checkbox('Show Sample Data'):
                st.info("Showing Sample data---->>>")
                image = load_mekd()
                st.image(image, caption='Sample Data', use_column_width=True)
                st.subheader("Choose Training Algorithm!")
                if st.checkbox('Keras'):
                    model1 = load_models()
                    st.success("Hooray !! Keras Model Loaded!")
                    if st.checkbox('Show Prediction Probablity on Sample Data'):
                        x_test = data_gen('angry542545.jfif')
                        y_new, Y_pred_classes = predict(x_test, model1)
                        result = display_prediction(y_new)
                        st.write(result)
                        if st.checkbox('Display Probability Graph'):
                            fig = px.bar(result, x="Classes",
                                         y="Probability", color='Classes')
                            st.plotly_chart(fig, use_container_width=True)

    if page == "Upload Your Image":

        st.header("Upload Your Image")

        file_path = st.file_uploader('Upload an image', type=['png', 'jpg'])

        if file_path is not None:
            x_test = data_gen(file_path)
            image = Image.open(file_path)
            img_array = np.array(image)

            st.write(image.format,image.size,image.mode)
            st.success('File Upload Success!!')
        else:
            st.info('Please upload Image file')

        if st.checkbox('Show Uploaded Image'):
            st.info("Showing Uploaded Image ---->>>")
            st.image(img_array, caption='Uploaded Image',
                     use_column_width=True)
            st.subheader("Choose Training Algorithm!")
            if st.checkbox('Keras'):
                model1 = load_models()
                st.success("Hooray !! Keras Model Loaded!")
                if st.checkbox('Show Prediction Probablity for Uploaded Image'):
                    y_new, Y_pred_classes = predict(x_test, model1)
                    result = display_prediction(y_new)
                    st.write(result)
                    if st.checkbox('Display Probability Graph'):
                        fig = px.bar(result, x="Classes",
                                     y="Probability", color='Classes')
                        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
