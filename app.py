import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff



df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.set_page_config(
   page_title="Olympics Data Analysis",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
option = st.sidebar.radio(
    'Select Option',('Medal Tally','OverAll-Analysis','Country-Wise-Analysis','Athlete-Wise-Analysis')
)

if option=="Medal Tally":
    st.header('Medal Tally')
    years,country = helper.country_year_list(df)
    selected_country = st.sidebar.selectbox('Select Country',country)
    selected_year = st.sidebar.selectbox('Select Year',years)
    mt= helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=="Overall" and selected_country=="Overall":
        pass
    elif selected_year!="Overall" and selected_country=="Overall":
        st.subheader('All country in '+str(selected_year))
    elif selected_year=="Overall" and selected_country!="Overall":
        st.subheader(selected_country+' In All Years')
    elif selected_year!="Overall" and selected_country!="Overall":
        st.subheader(selected_country+' In Year '+str(selected_year))
    st.table(mt)

if option=="OverAll-Analysis":
    st.header('Top Statistics')
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1,col2,col3 = st.columns(3,gap="small")
    with col1:
        st.subheader('Editions')
        st.subheader(editions)
    with col2:
        st.subheader('Cities')
        st.subheader(cities)
    with col3:
        st.subheader('Sports')
        st.subheader(sports)

    col1,col2,col3 = st.columns(3,gap="small")
    with col1:
        st.subheader('Events')
        st.subheader(events)
    with col2:
        st.subheader('Athletes')
        st.subheader(athletes)
    with col3:
        st.subheader('Nations')
        st.subheader(nations)

    participating_nation_df = helper.participating_nation(df,'region')
    fig = px.line(participating_nation_df,x="Editions",y="No Of region")
    st.header("Participating Nations Over Years")
    st.plotly_chart(fig)
    col1,col2 = st.columns(2,gap="small")
    with col1:      
       events_df = helper.participating_nation(df,'Event')
       fig = px.line(events_df,x="Editions",y="No Of Event")
       st.header("No Of Events Over Years")
       st.plotly_chart(fig)
    with col2:
       athletes_df = helper.participating_nation(df,'Name')
       fig = px.line(athletes_df,x="Editions",y="No Of Name")
       st.header("Athletes Over Years")
       st.plotly_chart(fig)

    st.header('No of events over time (Every Sports)')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


    st.header('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if option == "Country-Wise-Analysis":
    # st.header('Country Wise Analysis')
    country = df['region'].dropna().unique().tolist()
    country.sort()

    selected_country = st.sidebar.selectbox('Select Country',country)

    new_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(new_df,x="Year",y="Medal")
    st.header(selected_country +" Medal Tally Over Years")
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df,selected_country)
    st.header(selected_country+' Excels In Following Sports ')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(pt.astype('int'),annot=True)
    st.pyplot(fig)

    st.header('Top 10 Athletes Of '+selected_country)
    y= helper.most_succesful_countrywise(df,selected_country)
    st.table(y)

if option == "Athlete-Wise-Analysis":
    athlet_df = df.drop_duplicates(subset=['Name','region'])

    x1 = athlet_df['Age'].dropna()
    x2 = athlet_df[athlet_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlet_df[athlet_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlet_df[athlet_df['Medal']=='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=800,height=600)
    st.title('Distribution Of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlet_df[athlet_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age WRT Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)



