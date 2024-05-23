import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns 
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import altair as alt


st.set_page_config(
    layout="wide",
    page_title="Freelancer Analytics",
    page_icon="📊"
)

@st.cache_data()
def load_data(path):
    df = pd.read_csv('upwork-jobs.csv')

with st.spinner('Processing upwork data'):
    df=pd.read_csv('upwork-jobs.csv')
with st.container():
    st.title('Freelancer Data-Analysis')
    st.image("https://media.licdn.com/dms/image/C4D12AQGpjhobQhP7aw/article-cover_image-shrink_720_1280/0/1646143796142?e=2147483647&v=beta&t=bnsBi-8aMS5fV7VRv4zWGGy49me6i1elYx-SSVqfZHg", caption='Freelancer Data Analysis')
    st.subheader("Data Summary",divider='red')
c1,c2,c3=st.columns(3)


total_vacancy=df.shape[0]
type_trend="Freelancer Jobs"

c1.metric("Total Post",total_vacancy)
c2.metric("Type",type_trend)
c1.subheader("Insight: ")
st.info("""This app contains various freelancer 
analysis and its graphs based on total 
53058 number of post.
""")
st.info(" Total record in 2023 are 7.")
st.info(" Total record in 2024 are 53051.")

st.header("Top 5 Countries by Number of Titles:",divider='rainbow')

st.subheader('Top 5 Countries:-', divider='blue')
country_counts = df.groupby('country')['title'].count().sort_values(ascending=False)
top_countries = pd.DataFrame(country_counts).head()

fig = px.bar(top_countries, x=top_countries.index, y='title', labels={'Number of Titles': 'Number of Titles'})
st.plotly_chart(fig, use_container_width=True)




st.header("Top 10 Countries by Number of Hourly Jobs:",divider='rainbow')
top_10_countries = df.groupby('country')['is_hourly'].count().sort_values(ascending=False).head(10)
df_plot = pd.DataFrame(top_10_countries)

# Plotting with Plotly Express
fig = px.pie(df_plot, values='is_hourly', names=df_plot.index, labels={'is_hourly': 'Count', 'index': 'Country'})
fig.update_traces(textinfo='percent+label')
fig.update_layout(title='Distribution of Hourly Jobs Across Top 10 Countries')
st.plotly_chart(fig, use_container_width=True)


st.subheader('Top 10 Countries by Number of Titles:',divider='green')
st.info("This bar plot shows the top 10 countries by the number of titles.")

 # Group by country and count titles, then get the top 10
top_10_countries = df.groupby('country')['title'].count().sort_values(ascending=False).head(10)
df_plot = pd.DataFrame(top_10_countries)

# Plot the bar plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df_plot.index, df_plot['title'])
ax.set_xlabel('Country')
ax.set_ylabel('Count')
ax.set_title('Top 10 Countries by Number of Titles')
plt.xticks(rotation=45)
col1, col2 = st.columns([3, 2])
with col1:
  st.pyplot(fig)

with col2:
     st.info("""This bar plot provides insight into the distribution of titles among the top 10 countries. 
        It visualizes the number of titles attributed to each country, helping to identify the countries with the highest production of titles. 
        From the plot, it's evident that the USA has the highest number of titles, followed by China and India. 
        Such information can be valuable for various analyses, such as market research or content localization strategies.
        """)
     
st.header("Top 20 Titles by Number of Budgets:",divider='green')
top_20_titles = df.groupby('title')['budget'].count().sort_values(ascending=False).head(20)
df_plot = pd.DataFrame(top_20_titles).reset_index()

# Plotting with Plotly Express
fig_violin = px.violin(df_plot, y='title', x='budget',
                        labels={'budget': 'Count', 'title': 'Title'},
                        title='Distribution of Budgets Across Top 20 Titles',
                        orientation='h')
st.plotly_chart(fig_violin, use_container_width=True)


# st.markdown('<hr style="border-top: 2px solid red;">', unsafe_allow_html=True)
st.header("Number of Job Postings by Country & Distribution of Hourly Rates:", divider='red')
df_country_count = df['country'].value_counts()
df_country_count = df_country_count[df_country_count > 1000]
df_country_count = df_country_count.sort_values(ascending=True)

# Calculate hourly gigs with positive low hourly rates
df_gigs_low = df[(df['is_hourly'] == True) & (df['hourly_low'] > 0)]['hourly_low']
df_gigs_high = df[(df['is_hourly'] == True) & (df['hourly_low'] > 0)]['hourly_high']

# Split the app into two columns
col1, col2 = st.columns(2)

# Plotting Number of Job Postings by Country in the first column
with col1:
    st.markdown("**Number of Job Postings by Country:**")
    st.markdown('<hr style="border-top: 2px solid black;">', unsafe_allow_html=True)
    fig_country = px.bar(df_country_count, orientation='h', labels={'index': 'Country', 'value': 'Number of job postings'})
    st.plotly_chart(fig_country, use_container_width=True)

# Plotting Distribution of Hourly Rates in the second column
with col2:
    st.markdown("**Distribution of Hourly Rates:**")
    st.markdown('<hr style="border-top: 2px solid black;">', unsafe_allow_html=True)
    fig_hourly = px.histogram(df_gigs_low, nbins=100, opacity=0.35, labels={'value': '$ per hour offered'})
    fig_hourly.add_trace(px.histogram(df_gigs_high, nbins=100, opacity=0.35).data[0],)
    fig_hourly.update_layout(barmode='overlay', legend={'title': 'Rate'})
    st.plotly_chart(fig_hourly, use_container_width=True)

st.header("Most Frequent Jobs:",divider='green')
df_title_counts = df['title'].value_counts()
df_title_counts = df_title_counts[df_title_counts > 25]

# Create a DataFrame with the filtered data
df_plot = pd.DataFrame({'Title': df_title_counts.index, 'Number of job postings': df_title_counts.values})

# Plotting with Plotly Express: Horizontal Bar Chart
fig = px.bar(df_plot, y='Title', x='Number of job postings', orientation='h',
             labels={'Number of job postings': 'Number of job postings'},
             title='Most Frequent Jobs (without clustering)')
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig, use_container_width=True)


st.header("Distribution of Hourly Rates per Country of Posting:",divider='red')

# Filter countries with only >1000 jobs
df_top_countries = df[df['country'].isin(df_country_count.index)]

# Define max minimum rate for filtering
max_minimum_rate = 90

# Filter jobs based on maximum hourly rate
df_filtered = df_top_countries[df_top_countries['hourly_high'] <= max_minimum_rate]

# Plotting Distribution of hourly rates per country of posting using Plotly Express
fig1 = px.box(df_filtered, x='country', y='hourly_low', title='Distribution of Hourly Rates per Country of Posting',
             labels={'hourly_low': 'Rate per hour', 'country': 'Country'})
fig1.update_layout(xaxis={'title': 'Country'}, yaxis={'title': 'Rate per hour'})

# Filter jobs based on maximum hourly rate again for the second plot
df_filtered = df_top_countries[df_top_countries['hourly_low'] <= max_minimum_rate]

# Plotting the second Distribution of hourly rates per country of posting using Plotly Express
fig2 = px.box(df_filtered, x='country', y='hourly_low', title='Distribution of Hourly Rates per Country of Posting',
             labels={'hourly_low': 'Rate per hour', 'country': 'Country'})
fig2.update_layout(xaxis={'title': 'Country'}, yaxis={'title': 'Rate per hour'})

# Display the plots in two columns
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)


st.subheader('Analysis on Hourly vs Non-Hourly Jobs:', divider='green')
df_is_hourly = df['is_hourly'].value_counts()
df_is_hourly.index = ['Hourly', 'Not Hourly']
df_is_hourly = df_is_hourly.reset_index()
df_is_hourly.columns = ['Job Type', 'Count']

c1, c2 = st.columns(2)

# Create a bar plot using Plotly
fig = px.bar(df_is_hourly, x='Job Type', y='Count', title='Count of Hourly vs Non-Hourly Jobs',
             labels={'Job Type': 'Job Type', 'Count': 'Count'}, color='Job Type')
fig.update_layout(title={'text': 'Count of Hourly vs Non-Hourly Jobs', 'x': 0.5})

# Display the plot in the first column
with c1:
    st.plotly_chart(fig, use_container_width=True)

# Display the image in the second column and ensure it has the same height as the plot
with c2:
    st.image('https://img.freepik.com/premium-vector/young-man-sits-his-desk-workplace-using-his-personal-desktop-computer-working-online-program-work-home-concept-vector-illustration-isolated-white-background_37895-775.jpg', use_column_width=True)



st.subheader('Average hourly rate across all entries:', divider='orange')
hourly = df[df['is_hourly'] == True]
# Calculate average budget
avg_budget = round(((hourly['hourly_low'].sum() + hourly['hourly_high'].sum() + hourly['budget'].sum()) / len(df)) * 100, 2)
fig = go.Figure()

# Add box plot for budget
fig.add_trace(go.Box(y=df['budget'], name='Budget', boxmean=True))

# Update layout for the plot
fig.update_layout(
    title='Distribution of Budget',
    yaxis_title='Budget',
    xaxis_title='',
)
col1, col2 = st.columns([3, 2])
with col1:
  st.plotly_chart(fig)

with col2:
    st.info(f"The average hourly rate across all entries is ${avg_budget}.")    


# st.altair_chart(chart)
st.subheader('Checking Distribution of budgets:',divider='blue')
st.markdown("***", unsafe_allow_html=True)  # Adding a horizontal rule

col1, col2 = st.columns([1, 2])  # Split the layout into two columns

with col2:
        # Plot the KDE plot using Altair
        # chart = alt.Chart(df).transform_density(
        #     'budget',
        #     as_=['budget', 'density'],
        # ).mark_area().encode(
        #     x='budget:Q',
        #     y='density:Q',
        # ).properties(
        #     width=600,
        #     height=400
        # )
        # st.altair_chart(chart)
        chart = alt.Chart(df).transform_density(
            'budget',
            as_=['budget', 'density'],
        ).mark_area().encode(
            x=alt.X('budget:Q', scale=alt.Scale(type='log')),  # Logarithmic scaling for x-axis
            y='density:Q',
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(chart)

with col1:
        st.info("The KDE plot provides a comprehensive visualization of the distribution of the budget, allowing users to gain insights into its characteristics and make informed decisions based on the data.")
