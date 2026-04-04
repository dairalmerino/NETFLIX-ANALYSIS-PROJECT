import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---- page config ----
st.set_page_config(
    page_title="Netflix Content Strategy Analysis",
    page_icon="🎬",
    layout="wide"
)

# ---- load and clean data ----
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df = df.dropna(subset=['date_added'])
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(),format ='mixed')
    df['year_added'] = df['date_added'].dt.year.astype(int)
    df['month_added'] = df['date_added'].dt.month
    df['genre'] = df['listed_in'].str.split(', ')
    df_filtered = df[df['year_added'].between(2016, 2021)].copy()
    df_filtered['era'] = df_filtered['year_added'].apply(
        lambda x: 'pre-covid' if x <= 2019 else 'post-covid'
    )
    df_filtered['is_us'] = df_filtered['country'].str.contains('United States', na=False)
    return df_filtered

df = load_data()

# ---- header ----
st.title("🎬 Netflix Content Strategy Analysis (2016–2021)")
st.markdown("""
*How did Netflix's content strategy evolve from 2016 to 2021, 
and did COVID-19 change what they produced?*
""")

# ---- metric cards ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total titles", len(df))
col2.metric("Movies", len(df[df['type'] == 'Movie']))
col3.metric("TV Shows", len(df[df['type'] == 'TV Show']))
col4.metric("Years covered", "2016–2021")

st.divider()

# ---- section 2: content growth ----
st.header("📈 Content growth over time")

content_growth = (df
    .groupby(['year_added', 'type'])['title']
    .count()
    .reset_index()
    .rename(columns={'title': 'count'})
)

fig2 = px.line(content_growth,
    x='year_added',
    y='count',
    color='type',
    title='Netflix content growth by type (2016–2021)',
    labels={'year_added': 'Year', 'count': 'Number of titles', 'type': 'Content type'},
    color_discrete_map={'Movie': '#E50914', 'TV Show': '#221F1F'}
)
fig2.update_xaxes(tickvals=list(range(2016, 2022)))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
> 📌 Movie additions grew explosively from 2016 to 2017 (+231.6%) before tapering off. 
> Movies declined -9.8% in 2020 and -22.7% in 2021, while TV shows proved more 
> resilient, remaining virtually flat in 2020 (+0.5%).
""")

st.divider()

# ---- section 3: genre shifts ----
st.header("🎭 Genre shifts pre vs post COVID")

df_exploded = df.explode('genre')
genre_viz = (df_exploded
    .groupby(['era', 'genre'])['title']
    .count()
    .reset_index()
    .rename(columns={'title': 'count'})
)
genre_viz['avg_per_year'] = genre_viz.apply(
    lambda x: x['count'] / 4 if x['era'] == 'pre-covid' else x['count'] / 2, axis=1
).round(1)
top_genres = genre_viz.groupby('genre')['avg_per_year'].sum().nlargest(5).index
genre_viz_filtered = genre_viz[genre_viz['genre'].isin(top_genres)]
genre_viz_filtered['genre'] = genre_viz_filtered['genre'].str.replace('International ', 'Intl. ')

fig3 = px.bar(genre_viz_filtered,
    x='genre', y='avg_per_year', color='era', barmode='group',
    title='Top 5 genres: pre vs post COVID (avg per year)',
    labels={'genre': 'Genre', 'avg_per_year': 'Avg titles per year', 'era': 'Era'},
    color_discrete_map={'pre-covid': '#221F1F', 'post-covid': '#E50914'}
)
fig3.for_each_trace(lambda t: t.update(name=t.name.replace(
    'post-covid', 'Post-COVID').replace('pre-covid', 'Pre-COVID')))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
> 📌 All top 5 genres increased post-COVID when normalized by year. Comedies saw 
> the sharpest growth at +49.1%, suggesting Netflix leaned into lighter content 
> during the pandemic.
""")

st.divider()

# ---- section 4: international content ----
st.header("🌍 International content push")

intl_viz = (df
    .groupby(['year_added', 'is_us'])['title']
    .count()
    .unstack()
    .fillna(0)
    .astype(int)
    .reset_index()
)
intl_viz.columns = ['year_added', 'international', 'us']
intl_viz['total'] = intl_viz['international'] + intl_viz['us']
intl_viz['international_pct'] = (intl_viz['international'] / intl_viz['total'] * 100).round(1)

fig4 = px.line(intl_viz,
    x='year_added', y='international_pct',
    title='International content % by year (2016–2021)',
    labels={'year_added': 'Year', 'international_pct': 'International content %'},
    markers=True
)
fig4.update_traces(line_color='#E50914', marker_color='#221F1F')
fig4.add_hline(y=50, line_dash='dash', line_color='gray',
    annotation_text="50% threshold", annotation_position="bottom right")
fig4.add_annotation(x=2018, y=63.6, text="Peak: 63.6%",
    showarrow=True, arrowhead=2, yshift=15, font=dict(color='#E50914'))
fig4.update_xaxes(tickvals=list(range(2016, 2022)))
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
> 📌 International content peaked at 63.6% in 2018 before dipping to 55.9% in 2020, 
> suggesting COVID disrupted rather than accelerated Netflix's global push. A partial 
> recovery to 58.1% in 2021 suggests the strategy was beginning to bounce back.
""")

st.divider()

# ---- section 5: content ratings ----
st.header("🔞 Content maturity ratings")

rating_counts = (df
    .groupby(['era', 'rating'])['title']
    .count()
    .unstack(level=0)
    .fillna(0)
    .astype(int)
)
rating_counts['pre_covid_avg'] = (rating_counts['pre-covid'] / 4).round(1)
rating_counts['post_covid_avg'] = (rating_counts['post-covid'] / 2).round(1)
ratings_viz = rating_counts[['pre_covid_avg', 'post_covid_avg']].reset_index()
ratings_viz = ratings_viz.sort_values('post_covid_avg', ascending=False).head(5)
ratings_melted = ratings_viz.melt(
    id_vars='rating',
    value_vars=['pre_covid_avg', 'post_covid_avg'],
    var_name='era', value_name='avg_per_year'
)
ratings_melted['era'] = ratings_melted['era'].map({
    'pre_covid_avg': 'Pre-COVID', 'post_covid_avg': 'Post-COVID'
})

fig5 = px.bar(ratings_melted,
    x='rating', y='avg_per_year', color='era', barmode='group',
    title='Top 5 content ratings: pre vs post COVID (avg per year)',
    labels={'rating': 'Rating', 'avg_per_year': 'Avg titles per year', 'era': 'Era'},
    color_discrete_map={'Pre-COVID': '#221F1F', 'Post-COVID': '#E50914'}
)
fig5.add_annotation(x='PG-13', y=134, text="+143.6%",
    showarrow=True, arrowhead=2, yshift=15, font=dict(color='#E50914'))
st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
> 📌 Netflix shifted toward more mature content post-COVID. PG-13 grew the most 
> sharply (+143.6%), R-rated content nearly doubled (+81.4%), while family-friendly 
> TV-PG declined -19.0%.
""")

st.divider()

# ---- section 6: seasonal patterns ----
st.header("📅 Seasonal release patterns")

seasonal = (df
    .groupby(['era', 'month_added'])['title']
    .count()
    .unstack(level=0)
    .fillna(0)
)
seasonal['pre_covid_avg'] = (seasonal['pre-covid'] / 4).round(1)
seasonal['post_covid_avg'] = (seasonal['post-covid'] / 2).round(1)
seasonal_melted = seasonal[['pre_covid_avg', 'post_covid_avg']].reset_index()

fig6 = px.line(seasonal_melted,
    x='month_added', y=['pre_covid_avg', 'post_covid_avg'],
    title='Monthly content additions: pre vs post COVID',
    labels={'month_added': 'Month', 'value': 'Avg titles added', 'variable': 'Era'},
    color_discrete_map={'pre_covid_avg': '#221F1F', 'post_covid_avg': '#E50914'}
)
fig6.for_each_trace(lambda t: t.update(name=t.name.replace(
    'pre_covid_avg', 'Pre-COVID').replace('post_covid_avg', 'Post-COVID')))
fig6.update_xaxes(
    tickvals=list(range(1, 13)),
    ticktext=['Jan','Feb','Mar','Apr','May','Jun',
              'Jul','Aug','Sep','Oct','Nov','Dec'],
    range=[1, 12]
)
fig6.add_vline(
    x=9.5,  # between Sep and Oct
    line_dash='dash',
    line_color='gray',
    annotation_text="Q4 →",
    annotation_position="top right"
)

fig6.add_annotation(
    x=6,  # June is the 6th position
    y=seasonal.loc[6, 'post_covid_avg'],
    text="Peak: +102.8% in June",
    showarrow=True,
    arrowhead=2,
    yshift=15,
    font=dict(color='#E50914')
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("""
> 📌 Netflix dramatically front-loaded its release calendar post-COVID. June peaked 
> at +102.8% more titles per year while December dropped -45.0%, consistent with 
> global production shutdowns disrupting Netflix's traditional end-of-year content push.
""")

st.divider()
st.header("📋 Summary & key findings")

st.markdown("""
**Content growth**
Movie additions grew explosively from 2016 to 2017 (+231.6%) before tapering off. 
Movies declined -9.8% in 2020 and -22.7% in 2021, while TV shows proved more 
resilient, remaining virtually flat in 2020 (+0.5%).

**Genre shifts**
All top 5 genres increased post-COVID when normalized by year. Comedies saw the 
sharpest growth at +49.1%, suggesting Netflix leaned into lighter content during 
the pandemic.

**International content**
International content peaked at 63.6% in 2018 before dipping to 55.9% in 2020, 
suggesting COVID disrupted rather than accelerated Netflix's global push. A partial 
recovery to 58.1% in 2021 suggests the strategy was beginning to bounce back.

**Content maturity**
Netflix shifted toward more mature content post-COVID. PG-13 grew the most sharply 
(+143.6%), R-rated content nearly doubled (+81.4%), while family-friendly TV-PG 
declined -19.0%.

**Seasonal patterns**
Netflix dramatically front-loaded its release calendar post-COVID. June peaked at 
+102.8% more titles per year while December dropped -45.0%, consistent with global 
production shutdowns disrupting Netflix's traditional end-of-year content push.
""")

st.info("""
**Overall conclusion:** COVID-19 acted as a catalyst that accelerated and in some 
cases disrupted existing Netflix trends rather than creating entirely new ones. 
Content growth was already slowing before 2020, international expansion had peaked 
in 2018, and the shift toward mature content likely reflects both changing viewer 
preferences during lockdowns and practical production constraints.
""")

st.warning("""
**Limitations:** 
- Dataset covers 2016–2021 only; Post-COVID window limited to 2 years. 
- 9% of titles missing country data
- Statistical significance limited by small sample size (TVD p=0.143).
""")

st.markdown("""
**Future work**
- Incorporate 2022–2024 data to confirm whether trends persisted
- Analyze Netflix original vs licensed content separately  
- Cross-reference with Netflix subscriber growth data
- Apply a recommender system to predict what content Netflix might prioritize next
""")


# ---- footer ----
st.markdown("""
---
*Analysis by Daira Merino | Data source: Kaggle Netflix Movies and TV Shows dataset*
""")