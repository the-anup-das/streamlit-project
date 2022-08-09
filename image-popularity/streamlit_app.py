import torch
import torchvision.models
import torchvision.transforms as transforms
import streamlit as st

import os


from PIL import Image

st.set_page_config(
     page_title="Check your image popularity score",
     page_icon="assets/favicon(1).ico",
     layout="wide",
     initial_sidebar_state="expanded",

 )

path = os.path.dirname(__file__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open(path+'//style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

def prepare_image(image):
    if image.mode != 'RGB':
        image = image.convert("RGB")
    
    Transform = transforms.Compose([
        transforms.Resize([224,224]),
        transforms.ToTensor(),
    ])
    image = Transform(image)
    image = image.unsqueeze(0)
    return image.to(device)

def predict(image, model):
    image = prepare_image(image)
    with torch.no_grad():
        preds = model(image)
    return(preds.item())

st.write("""
# Check your picture popularity score
""")
with st.spinner('Wait for it...'):
    uploaded_file = st.sidebar.file_uploader("Upload your input image file", type=['jpg','png'])
    if uploaded_file is not None:
        st.write("""
        ### Your uploaded image
        """)
        st.image(uploaded_file, width=600)
        image = Image.open(uploaded_file)
        model = torchvision.models.resnet50()
        # model.avgpool = nn.AdaptiveAvgPool2d(1) # for any size of the input
        model.fc = torch.nn.Linear(in_features=2048, out_features=1)
        model.load_state_dict(torch.load(path+'/model/model-resnet50.pth', map_location=device)) 
        model.eval().to(device)
        pre = predict(image, model)
        # st.write()
        st.success(f"Popularity Score: {pre:.2f}")
    else:
        st.error("You need to upload an image")

    # st.success('Done!')


st.markdown('## Made with Love :heart: Anup ', unsafe_allow_html = False)
