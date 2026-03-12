import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ==========================================
# 1. PAGE SETUP & EXECUTIVE CSS
# ==========================================
st.set_page_config(page_title="Atlantic Records | France Intel", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    [data-testid="stMetricValue"] { color: #ff4b4b !important; font-weight: 800; font-size: 28px !important; }
    .stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid #30363d; padding-bottom: 5px; }
    .stTabs [data-baseweb="tab"] { background-color: transparent; color: #8b949e; font-size: 16px; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: #ff4b4b !important; border-bottom: 3px solid #ff4b4b; }
    .executive-card { background-color: #161b22; border-left: 5px solid #ff4b4b; padding: 20px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #30363d; }
    .help-text { font-size: 13px; color: #8b949e; font-style: italic; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA PIPELINE
# ==========================================
@st.cache_data
def load_and_prep_data():
    file_path = 'Atlantic_France.csv'
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    df = df.dropna(subset=['date', 'song'])
    
    for col in ['position', 'popularity', 'duration_ms', 'total_tracks']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    df['duration_minutes'] = df['duration_ms'] / 60000
    df['is_explicit'] = df['is_explicit'].astype(bool)
    df['album_type'] = df['album_type'].astype(str).str.lower()
    
    def categorize_dur(m):
        if m < 2.5: return "Short (< 2.5 mins)"
        elif m <= 3.5: return "Medium (2.5 - 3.5 mins)"
        else: return "Long (> 3.5 mins)"
    df['duration_bucket'] = df['duration_minutes'].apply(categorize_dur)
    df['rank_tier'] = pd.cut(df['position'], bins=[0, 10, 25, 50], labels=['Top 10', 'Top 25', 'Top 50'])
    
    return df

df_master = load_and_prep_data()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/d/d4/Atlantic_Records_logo.svg", width=140)
st.sidebar.markdown("### 🎛️ Analysis Controls")

if not df_master.empty:
    min_date, max_date = df_master['date'].min().date(), df_master['date'].max().date()
    
    date_range = st.sidebar.date_input("Analysis Period", [min_date, max_date], min_value=min_date, max_value=max_date)
    start_date = date_range[0]
    end_date = date_range[1] if len(date_range) > 1 else date_range[0]

    tier_filter = st.sidebar.multiselect("Chart Depth", ['Top 10', 'Top 25', 'Top 50'], default=['Top 10', 'Top 25', 'Top 50'])
    content_filter = st.sidebar.radio("Content Compliance", ["All", "Explicit Only", "Clean Only"])
    format_filter = st.sidebar.multiselect("Release Format", df_master['album_type'].unique(), default=df_master['album_type'].unique())
    
    # Apply Filters
    df = df_master[(df_master['date'].dt.date >= start_date) & (df_master['date'].dt.date <= end_date)]
    df = df[df['rank_tier'].isin(tier_filter)]
    df = df[df['album_type'].isin(format_filter)]
    if content_filter == "Explicit Only": df = df[df['is_explicit'] == True]
    elif content_filter == "Clean Only": df = df[df['is_explicit'] == False]

# ==========================================
# 4. TOP HEADER & KPIs
# ==========================================
    st.title("🇫🇷 France Market Intelligence")
    st.subheader("Audience Sensitivity & Format Preference Analysis")

    if df.empty:
        st.warning("⚠️ No data matches the selected filters.")
    else:
        # KPI SUMMARY PANEL
        total_songs = len(df)
        exp_share = (df['is_explicit'].sum() / total_songs) * 100
        clean_ratio = 100 - exp_share
        
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total Records", total_songs)
        k2.metric("Explicit Share", f"{round(exp_share, 1)}%")
        k3.metric("Clean Dominance", f"{round(clean_ratio, 1)}%")
        k4.metric("Avg Duration", f"{round(df['duration_minutes'].mean(), 1)}m")
        k5.metric("Avg Popularity", round(df['popularity'].mean(), 1))
        st.divider()

# ==========================================
# 5. NEW VISUAL TABS
# ==========================================
        tabs = st.tabs([
            "🏆 Top Hits Showcase", "⚖️ Compliance & Formats", "🎵 Structure & Impact", "🎤 Artist Deep-Dive", "🧠 Strategy Output"
        ])

        # TAB 1: VISUAL SHOWCASE (NEW FEATURE)
        with tabs[0]:
            st.markdown("### Highest Ranking Tracks in Selection")
            st.markdown('<p class="help-text">The most popular tracks currently matching your sidebar filters.</p>', unsafe_allow_html=True)
            
            top_3 = df.nsmallest(3, 'position').drop_duplicates(subset=['song'])
            if not top_3.empty:
                cols = st.columns(len(top_3))
                for idx, (_, row) in enumerate(top_3.iterrows()):
                    with cols[idx]:
                        if 'album_cover_url' in row and pd.notna(row['album_cover_url']):
                            st.image(row['album_cover_url'], use_container_width=True)
                        st.markdown(f"**#{row['position']} - {row['song']}**")
                        st.caption(f"Artist: {row['artist']}")
                        st.caption(f"Format: {row['album_type'].capitalize()} | {'Explicit 🔴' if row['is_explicit'] else 'Clean 🟢'}")
            
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Top Artists by Popularity")
                top_artists = df.groupby('artist')['popularity'].mean().nlargest(5).reset_index()
                st.plotly_chart(px.bar(top_artists, x='popularity', y='artist', orientation='h', template='plotly_dark', color='popularity', color_continuous_scale='Reds').update_layout(yaxis={'categoryorder':'total ascending'}), use_container_width=True)

        # TAB 2: COMPLIANCE & FORMATS (Easy to read)
        with tabs[1]:
            cl1, cl2 = st.columns(2)
            with cl1:
                st.subheader("Explicit vs Clean Share")
                st.markdown('<p class="help-text">Shows if the audience prefers family-friendly lyrics or explicit content.</p>', unsafe_allow_html=True)
                st.plotly_chart(px.pie(df, names='is_explicit', hole=0.5, template='plotly_dark', color='is_explicit', color_discrete_map={True: '#ff4b4b', False: '#1f77b4'}), use_container_width=True)
            with cl2:
                st.subheader("Format Market Share")
                st.markdown('<p class="help-text">Compares the success of standalone Singles vs. tracks from full Albums.</p>', unsafe_allow_html=True)
                st.plotly_chart(px.pie(df, names='album_type', hole=0.5, template='plotly_dark', color_discrete_sequence=['#9b59b6', '#3498db']), use_container_width=True)

        # TAB 3: STRUCTURE & IMPACT
        with tabs[2]:
            s1, s2 = st.columns(2)
            with s1:
                st.subheader("Ideal Song Length")
                st.markdown('<p class="help-text">The most common track durations for hit songs in France.</p>', unsafe_allow_html=True)
                st.plotly_chart(px.histogram(df, x='duration_bucket', template='plotly_dark', color_discrete_sequence=['#ff4b4b']), use_container_width=True)
            with s2:
                st.subheader("Album Dilution Impact")
                st.markdown('<p class="help-text">Downward trendlines indicate that massive albums hurt individual song popularity.</p>', unsafe_allow_html=True)
                st.plotly_chart(px.scatter(df, x='total_tracks', y='popularity', trendline='ols', template='plotly_dark', color_discrete_sequence=['#ff4b4b']), use_container_width=True)

        # TAB 4: ARTIST DEEP-DIVE (NEW FEATURE)
        with tabs[3]:
            st.subheader("🔍 Individual Artist Profiler")
            st.markdown('<p class="help-text">Select an artist to instantly generate a custom compliance and format report for them.</p>', unsafe_allow_html=True)
            
            selected_artist = st.selectbox("Select an Artist to analyze:", sorted(df_master['artist'].unique()))
            artist_df = df_master[df_master['artist'] == selected_artist]
            
            if not artist_df.empty:
                a_cols = st.columns([1, 2])
                with a_cols[0]:
                    # Show their most recent album cover
                    recent_cover = artist_df['album_cover_url'].iloc[0]
                    if pd.notna(recent_cover):
                        st.image(recent_cover, width=250)
                with a_cols[1]:
                    st.markdown(f"### {selected_artist}")
                    st.metric("Highest Chart Position", f"#{artist_df['position'].min()}")
                    st.metric("Explicit Track Percentage", f"{round((artist_df['is_explicit'].sum() / len(artist_df)) * 100, 1)}%")
                    st.metric("Primary Format", artist_df['album_type'].mode()[0].capitalize())

        # TAB 5: STRATEGY OUTPUT
        with tabs[4]:
            st.subheader("Executive Action Plan")
            
            best_format = df['album_type'].mode()[0].capitalize()
            best_length = df['duration_bucket'].mode()[0]
            safety = "Clean" if exp_share < 50 else "Explicit"
            
            st.markdown(f"""
            <div class="executive-card">
            <h4>🎯 Current Market Hit Formula:</h4>
            Based on the currently selected data, the ideal release profile for the French market is:<br><br>
            • <b>Release Strategy:</b> Focus on {best_format}s.<br>
            • <b>Target Length:</b> Aim for {best_length} tracks.<br>
            • <b>Content Risk:</b> The market favors {safety} content right now.<br>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### 📥 Export Data")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Curated Report (CSV)", data=csv, file_name="atlantic_france_report.csv", mime='text/csv')

else:
    st.error("DATA MISSING: Please ensure 'Atlantic_France.csv' is saved in the same folder.")