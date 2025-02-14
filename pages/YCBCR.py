import streamlit as st  
from utils import *
import tempfile

st.set_page_config(layout='wide')
st.title('Hidden Message')

try:
    file = st.file_uploader('Choose an image')
    if (file is not None):
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.read())
        name = tfile.name
        st.write('please wait reading image ...')
        image = cv2.cvtColor(cv2.imread(name), cv2.COLOR_BGR2RGB)
except:
    image = cv2.imread('Test_Image.jpg').astype(np.uint16)
    message = 'Test message'

st.image(image)

message = st.text_input('Message')

og_img_col, slider_col, new_img_col = st.columns([2, 1, 2])

with og_img_col:
    st.write('Choosen image')
    st.image(image.astype(np.uint8), caption='Shape: '+str(image.shape)+', type:'+str(image.dtype)) # channels, output_format
    st.write('Message: ' + message)

with slider_col:
    slider = st.select_slider('Send', options=['Sender', 'Receiver'], label_visibility='hidden')

if slider == 'Receiver' and image is not None and message != '':
    new_img, enc_message = encode_ycbr(cv2.cvtColor(image, cv2.COLOR_RGB2YCR_CB), message)
    with new_img_col:
        st.write('Image containing the message')
        st.image(enc_message.astype(np.uint8), caption='Shape: '+str(enc_message.shape)+', type:'+str(enc_message.dtype)) 
        decoded_message = decode_ycbr(new_img)
        print(decoded_message.shape)
        st.image(decoded_message.astype(np.uint8))