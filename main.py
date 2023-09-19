import streamlit as st
from fastai.tabular.all import *
import pathlib

st.set_page_config(
    page_title="WannaDance",
    page_icon='https://cdn.pic.in.th/file/picinth/image-removebg-preview8240db53fbc97808.png',
    layout='wide',
    menu_items={
        'Report a bug' : 'https://github.com/thunni-noi/bicycle-prediction/issues',
        'About' : 'https://github.com/thunni-noi/bicycle-prediction'
    }
)

if 'prediction_result' not in st.session_state: st.session_state['prediction_result'] = ""
if 'song_details' not in st.session_state: st.session_state['song_details'] = {
    'bpm' : 0,
    'energy' : 'n/a',
    'acoustic' : 'n/a',
    'instrument' : 'n/a',
    'mood' : 'n/a'
}

@st.cache_resource
def load_ml_model():
    if st.secrets['current_platform'] != "pc":
        pathlib.WindowsPath = pathlib.PosixPath
        model_path = "./models/model.pkl"
    else:
        model_path = pathlib.Path('models\model.pkl')
    loaded_model = load_learner(model_path)
    return loaded_model

dancability_cat = ['High', 'Low', 'Medium', 'Very High'] #!It isn't normal order but this need to be this way to work!

def model_predict(ml_model, bpm, energy, acoutic, instrumental, mood):
    
    #?Adjustment
    if instrumental == "Low" : instrumental = "Very Low"
    
    to_predict = pd.Series([bpm, energy, acoutic, instrumental, mood], index=['bpm', 'energy_.', 'acousticness_.', 'instrumentalness_.', 'song_mood'])
    raw_result = ml_model.predict(to_predict)[0].items['danceability_.']
    return dancability_cat[raw_result[0].astype(int)]

st.markdown(
    """
    <style>
        [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)
st.image('https://media.tenor.com/oA5ClfmykW8AAAAi/alice-aris.gif')

st.markdown(
    """<h1 style='text-align: center;
        font-size:72px; 
        color: #67AAF9;
        '>WannaDance
        </h1>
    """, unsafe_allow_html=True
    )

st.markdown(
    """<h1 style='text-align: center;
        font-size:36px; 
        color: #C4E0F9;
        '>Predict danceability of music!
        </h1>
    """, unsafe_allow_html=True
    )

#Display result
if st.session_state['prediction_result'] != "":
    st.markdown(
    """<h1 style='text-align: center;
        font-size:30px; 
        color: #9BBDF9;
        '>Song details :
        </h1>
    """, unsafe_allow_html=True
    )
    
    #!this is some complex html stuff idk what i'm doing ;-;
    txt1 = '''BPM : {} //  Energy : {} //  Acousticness : {}'''.format(st.session_state['song_details']['bpm'], st.session_state['song_details']['energy'], st.session_state['song_details']['acoustic'])
    txt2 = ('Instrumentalness : {} //  Mood : {}'.format(st.session_state['song_details']['instrument'], st.session_state['song_details']['mood']))
    
    st.markdown(
    f"""<p style='text-align: center;
        font-size:24px;
        color: #FFFADD'>
        {txt1}
        </p>
    """, unsafe_allow_html=True
    )
    
    st.markdown(
    f"""<p style='text-align: center;
        font-size:24px; 
        color: #FFFADD;'>
        {txt2}
        </p>
        
    """, unsafe_allow_html=True
    )
    if st.session_state['prediction_result'] == "Low":
        txt3 = ('No dance ;-;')
        col3 = '#EF9595'
    elif st.session_state['prediction_result'] == "Medium":
        txt3 = ('Kinda dancable?')
        col3 = '#EBEF95'
    elif st.session_state['prediction_result'] == "High":
        txt3 = ('Dance time! Lessgooooooo :D')
        col3 = '#A6FF96'
    elif st.session_state['prediction_result'] == "Very High":
        txt3 = ('Dance overload!!!!')
        col3 = '#FFA1F5'
    else :
        txt3 = ('Ummmm, Is this supposed to happened?')
        col3 = '#FF3FA4'
    
    
    st.markdown(
    f"""<h1 style='text-align: center;
        font-size:30px; 
        color: {col3};
        '>
        Danceability : {st.session_state['prediction_result']}
        </h1>
    """, unsafe_allow_html=True
    )
    
    st.markdown(
    f"""<p style='text-align: center;
        font-size:15px; 
        color: #E4F1FF;'>
        {txt3}
        </p>"""
    , unsafe_allow_html=True)
        
stat_input_format = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
mood_input_format = ['Happy', 'Normal', 'Sad']


#need bpm, energy, acoutic, instrumental, mood
with st.form("input"):
    st.write('Variable settings')
    bpm = st.number_input("Song's beat per minute : ", min_value = 1, max_value = 299, value=120)
    energy = st.selectbox("Song's overall energy level : ", options=stat_input_format, index=2, help='How energetic is your song? (Just use your feeling!)')
    acoustic = st.selectbox("Song's overall acousticness : ", options=stat_input_format, index=2, help='How acoustic a song sound. (Acoustic being that almost no electronic instrument or element in incorporated into music)')
    instrumental = st.selectbox("Song's overall instrumentalness : ", options=stat_input_format, index=2, help='How acoustic a song sound. (Instrumentalness being the absence of audible lyrics/vocals in the song - For example most of BGM will have almost no lyrics at all thus higher instrumentalness.)')
    mood= st.selectbox("Song's mood : ", options=mood_input_format, index=1, help="How's overall mood? (If you don't know lyrics - Again, Just use your feeling!)")
    predict_button = st.form_submit_button('Start predict')

if predict_button:
    with st.status('Fetching variable...') as status:
        st.write('Saving Data.....')
        st.session_state['song_details'] = {
        'bpm' : bpm,
        'energy' : energy,
        'acoustic' : acoustic,
        'instrument' : instrumental,
        'mood' : mood
        }
        st.write('Loading Machine Learning Model...')
        ml_model = load_ml_model()
        st.write('Predicting the result....')
        result = model_predict(ml_model, bpm, energy, acoustic, instrumental, mood)
        st.session_state['prediction_result'] = result
        status.update(label='Predicting complete!', state="complete")
        st.experimental_rerun()
        
        
if st.button('Refresh'):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()