import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

from utils import (
    load_and_clean_data,
    load_model,
    predict_score,
    get_champions,
    get_matches_per_season,
    get_team_stats,
    get_single_team_stats,
    get_top_batters,
    get_top_bowlers,
    get_top_sixes,
    get_top_fours,
    get_top_pom,
    get_orange_cap_per_season,
    get_purple_cap_per_season,
    get_top_keepers,
    get_top_venues,
    get_highest_scoring_venues,
    get_head_to_head
)

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="All About Cric...",
    page_icon="🏏",
    layout="wide"
)

# ==========================================
# GLOBAL CHART THEME
# ==========================================
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams.update({
    'figure.facecolor': '#0f172a',
    'axes.facecolor': '#111827',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'text.color': 'white',
    'axes.titlecolor': '#fbbf24',
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'grid.color': '#334155',
    'grid.alpha': 0.3,
    'font.family': 'sans-serif',
})

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #1e293b 100%);
        color: white;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        position: relative;
        z-index: 2;
    }

    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(90deg, #f97316, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }

    .sub-title {
        text-align: center;
        color: #cbd5e1;
        font-size: 17px;
        font-weight: 400;
        margin-top: 0px;
        margin-bottom: 25px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .section-heading {
        color: #fbbf24;
        font-size: 28px;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    h3 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.25);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-6px);
        border-color: #f97316;
        box-shadow: 0px 8px 30px rgba(249, 115, 22, 0.3);
    }

    .metric-value {
        font-size: 36px;
        font-weight: 800;
        font-family: 'Poppins', sans-serif;
        color: #f97316;
        margin-bottom: 5px;
    }

    .metric-label {
        font-size: 13px;
        color: #e5e7eb;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .info-card {
        background: rgba(249, 115, 22, 0.12);
        border-left: 5px solid #f97316;
        padding: 18px;
        border-radius: 12px;
        color: #f8fafc;
        font-size: 16px;
        line-height: 1.6;
    }

    .prediction-card {
        background: linear-gradient(135deg, #f97316 0%, #fbbf24 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0px 10px 40px rgba(249, 115, 22, 0.4);
        margin-top: 20px;
    }

    .prediction-label {
        color: white;
        font-size: 18px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
        font-family: 'Poppins', sans-serif;
    }

    .prediction-value {
        color: white;
        font-size: 80px;
        font-weight: 800;
        font-family: 'Poppins', sans-serif;
        line-height: 1;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }

    .prediction-range {
        color: white;
        font-size: 16px;
        margin-top: 10px;
        opacity: 0.9;
    }

    label {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        color: #e2e8f0 !important;
    }

    .stTabs [data-baseweb="tab-list"] button {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
    }

    table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .metric-card,
    .section-heading,
    .info-card,
    .prediction-card,
    .stTabs,
    .stDataFrame,
    .stSelectbox,
    table {
        animation: fadeInUp 0.6s ease-out;
    }

    /* ===== FLOATING BACKGROUND ELEMENTS ===== */
    .floating-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }

    .floating-item {
        position: absolute;
        font-size: 32px;
        opacity: 0;
        animation: float linear infinite;
        user-select: none;
    }

    @keyframes float {
        0% {
            transform: translateY(110vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 0.18;
        }
        90% {
            opacity: 0.18;
        }
        100% {
            transform: translateY(-20vh) rotate(720deg);
            opacity: 0;
        }
    }

    /* Force nav-menu background dark on mobile */
    nav[class*="nav-menu"],
    ul[class*="nav-menu"],
    .nav-menu {
        background-color: #1e293b !important;
    }

    /* Each nav item */
    .nav-link {
        background-color: transparent !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# FLOATING BACKGROUND
# ==========================================
st.markdown("""
<div class="floating-bg">
    <span class="floating-item" style="left: 5%; animation-duration: 20s; animation-delay: 0s;">🏏</span>
    <span class="floating-item" style="left: 12%; animation-duration: 24s; animation-delay: 3s;">🥎</span>
    <span class="floating-item" style="left: 20%; animation-duration: 18s; animation-delay: 6s;">🏆</span>
    <span class="floating-item" style="left: 28%; animation-duration: 26s; animation-delay: 1s;">🏏</span>
    <span class="floating-item" style="left: 36%; animation-duration: 22s; animation-delay: 4s;">⭐</span>
    <span class="floating-item" style="left: 44%; animation-duration: 19s; animation-delay: 8s;">🥎</span>
    <span class="floating-item" style="left: 52%; animation-duration: 25s; animation-delay: 2s;">🏏</span>
    <span class="floating-item" style="left: 60%; animation-duration: 21s; animation-delay: 5s;">🏆</span>
    <span class="floating-item" style="left: 68%; animation-duration: 23s; animation-delay: 7s;">🥎</span>
    <span class="floating-item" style="left: 76%; animation-duration: 17s; animation-delay: 9s;">🏏</span>
    <span class="floating-item" style="left: 84%; animation-duration: 27s; animation-delay: 2s;">⭐</span>
    <span class="floating-item" style="left: 92%; animation-duration: 20s; animation-delay: 6s;">🥎</span>
</div>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA & MODEL
# ==========================================
matches, deliveries = load_and_clean_data()
model, metadata = load_model()

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def metric_card(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def section_heading(text):
    st.markdown(f"<div class='section-heading'>{text}</div>",
                unsafe_allow_html=True)

def render_chart(fig):
    st.pyplot(fig)
    plt.close(fig)

def styled_table(df, gradient_col=None, cmap='Oranges', format_dict=None):
    if format_dict:
        styled = df.style.format(format_dict)
    else:
        float_cols = df.select_dtypes(include=['float']).columns
        styled = df.style.format({col: '{:.2f}' for col in float_cols})
    
    styled = styled.set_table_styles([
        {'selector': 'thead th',
         'props': [
             ('background-color', '#f97316'),
             ('color', 'white'),
             ('font-weight', '700'),
             ('font-family', 'Poppins, sans-serif'),
             ('text-transform', 'uppercase'),
             ('font-size', '13px'),
             ('letter-spacing', '0.5px'),
             ('padding', '14px 16px'),
             ('text-align', 'left'),
             ('border', 'none'),
         ]},
        {'selector': 'tbody td',
         'props': [
             ('color', '#f1f5f9'),
             ('font-family', 'Inter, sans-serif'),
             ('font-size', '14px'),
             ('padding', '12px 16px'),
             ('border-bottom', '1px solid rgba(255,255,255,0.05)'),
             ('font-weight', '500'),
         ]},
        {'selector': 'tbody tr:nth-child(even) td',
         'props': [('background-color', 'rgba(255,255,255,0.03)')]},
        {'selector': 'tbody tr:nth-child(odd) td',
         'props': [('background-color', 'rgba(255,255,255,0.06)')]},
        {'selector': 'tbody tr:hover td',
         'props': [('background-color', 'rgba(249,115,22,0.18)')]},
        {'selector': '',
         'props': [
             ('border-collapse', 'collapse'),
             ('width', '100%'),
             ('border-radius', '12px'),
             ('overflow', 'hidden'),
             ('box-shadow', '0px 4px 20px rgba(0,0,0,0.25)'),
             ('margin', '10px 0'),
         ]},
    ]).hide(axis='index')

    if gradient_col and gradient_col in df.columns:
        styled = styled.background_gradient(
            subset=[gradient_col],
            cmap=cmap,
            vmin=df[gradient_col].min(),
            vmax=df[gradient_col].max()
        ).set_properties(
            subset=[gradient_col],
            **{'color': '#1a1a1a', 'font-weight': '700'}
        )

    st.markdown(styled.to_html(), unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown("<h1 class='main-title'>🏏 All About Cric...</h1>",
            unsafe_allow_html=True)
st.markdown("<p class='sub-title'>IPL Statistics Dashboard | 2008 - 2024</p>",
            unsafe_allow_html=True)

# ==========================================
# TOP NAV
# ==========================================
page = option_menu(
    menu_title=None,
    options=["Home", "Season", "Team", "Player", "Venue", "Head-to-Head", "Predictor"],
    icons=["house-fill", "trophy-fill", "people-fill",
           "person-fill", "geo-alt-fill", "shield-fill", "graph-up-arrow"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "5px !important",
            "background-color": "#1e293b !important",
            "border-radius": "14px",
            "margin-bottom": "25px",
            "border": "1px solid rgba(255,255,255,0.1)"
        },
        "icon": {
            "color": "#f97316",
            "font-size": "18px"
        },
        "nav-link": {
            "font-size": "15px",
            "text-align": "center",
            "margin": "2px",
            "color": "#e5e7eb !important",
            "background-color": "transparent !important",
            "--hover-color": "rgba(249,115,22,0.18)",
            "border-radius": "10px",
            "padding": "12px"
        },
        "nav-link-selected": {
            "background-color": "#f97316 !important",
            "color": "white !important",
            "font-weight": "700"
        },
    }
)

# ==========================================
# HOME PAGE
# ==========================================
if page == "Home":
    section_heading("🏠 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1: metric_card("Total Seasons", matches['season'].nunique())
    with col2: metric_card("Total Matches", matches.shape[0])
    with col3: metric_card("Total Teams", matches['team1_std'].nunique())
    with col4: metric_card("Total Players", deliveries['batter'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: metric_card("Total Venues", matches['venue'].nunique())
    with col2: metric_card("Host Cities", matches['city'].nunique())
    with col3: metric_card("Total Deliveries", f"{deliveries.shape[0]:,}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        Welcome to <b>All About Cric...</b> — an interactive IPL analytics platform 
        built using <b>Python, Pandas, Seaborn, Scikit-learn and Streamlit</b>.
        Explore detailed stats and try our <b>AI Score Predictor</b> powered 
        by Linear Regression.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    section_heading("⚡ Quick Insights")

    champions = get_champions(matches)
    team_stats = get_team_stats(matches)
    top_batter = get_top_batters(deliveries, 1)
    top_bowler = get_top_bowlers(deliveries, 1)

    col1, col2, col3, col4 = st.columns(4)
    with col1: metric_card("Most Titles 🏆", champions['Champion'].value_counts().idxmax())
    with col2: metric_card("Best Win % 📈", team_stats.index[0])
    with col3: metric_card("Top Run Scorer 🏏", top_batter.index[0])
    with col4: metric_card("Top Wicket Taker 🎯", top_bowler.index[0])


# ==========================================
# SEASON ANALYSIS
# ==========================================
elif page == "Season":
    section_heading("🏆 Season Analysis")

    champions = get_champions(matches)
    st.subheader("👑 IPL Champions by Season")
    styled_table(champions)

    st.markdown("---")
    st.subheader("🏆 Most Titles Won")
    title_count = champions['Champion'].value_counts()

    col1, col2 = st.columns([1, 2])
    with col1:
        title_df = title_count.reset_index()
        title_df.columns = ['Team', 'Titles']
        styled_table(title_df, gradient_col='Titles', cmap='Oranges')

    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=title_count.index, y=title_count.values,
                    palette='Oranges_r', ax=ax, edgecolor='white')
        ax.set_title('IPL Titles Won by Each Team')
        ax.set_xlabel('Team')
        ax.set_ylabel('Titles')
        for i, v in enumerate(title_count.values):
            ax.text(i, v + 0.05, str(v), ha='center',
                    color='white', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        render_chart(fig)

    st.markdown("---")
    st.subheader("📊 Matches Played Per Season")
    matches_per_season = get_matches_per_season(matches)

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(x=matches_per_season.index,
                y=matches_per_season.values,
                palette='Blues_r', ax=ax, edgecolor='white')
    ax.set_title('Total Matches Per IPL Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Matches')
    for i, v in enumerate(matches_per_season.values):
        ax.text(i, v + 0.2, str(v), ha='center',
                color='white', fontweight='bold', fontsize=9)
    plt.xticks(rotation=45)
    plt.tight_layout()
    render_chart(fig)


# ==========================================
# TEAM ANALYSIS
# ==========================================
elif page == "Team":
    section_heading("👥 Team Analysis")

    team_stats = get_team_stats(matches)
    st.subheader("📊 Team Performance Summary")
    team_stats_display = team_stats.reset_index().rename(columns={'index': 'Team'})
    styled_table(team_stats_display, gradient_col='Win %', cmap='Oranges')

    st.markdown("---")
    st.subheader("📈 Win Percentage of Each Team")

    win_df = team_stats.reset_index().rename(columns={'index': 'Team'})
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=win_df, x='Team', y='Win %',
                palette='coolwarm', ax=ax, edgecolor='white')
    ax.axhline(50, color='#ef4444', linestyle='--', alpha=0.8, label='50% Mark')
    ax.set_title('Team Win Percentage')
    ax.set_xlabel('Team')
    ax.set_ylabel('Win %')
    ax.legend()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    render_chart(fig)

    st.markdown("---")
    st.subheader("🔍 Deep Dive Into a Single Team")

    all_teams = sorted(matches['team1_std'].dropna().unique())
    selected_team = st.selectbox("Select a team", all_teams)

    total, wins, losses, win_pct = get_single_team_stats(matches, selected_team)

    col1, col2, col3, col4 = st.columns(4)
    with col1: metric_card("Matches Played", total)
    with col2: metric_card("Wins", wins)
    with col3: metric_card("Losses", losses)
    with col4: metric_card("Win %", f"{win_pct:.2f}%")

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie([wins, losses],
           labels=['Wins', 'Losses'],
           colors=['#22c55e', '#ef4444'],
           autopct='%1.1f%%',
           startangle=90,
           explode=(0.05, 0.05),
           shadow=True,
           textprops={'color': 'white', 'fontsize': 13, 'fontweight': 'bold'})
    ax.set_title(f'{selected_team} - Win/Loss Split')
    plt.tight_layout()
    render_chart(fig)


# ==========================================
# PLAYER ANALYSIS
# ==========================================
elif page == "Player":
    section_heading("🏏 Player Analysis")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🟠 Batters", "🟣 Bowlers",
        "💥 Boundaries", "🏆 Season Caps", "🧤 Wicketkeepers"
    ])

    with tab1:
        st.subheader("🏏 Top 10 Run Scorers")
        top_batters = get_top_batters(deliveries).reset_index()
        top_batters.columns = ['Player', 'Runs']

        col1, col2 = st.columns([1, 2])
        with col1:
            styled_table(top_batters, gradient_col='Runs', cmap='Oranges')
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=top_batters, x='Runs', y='Player',
                        palette='Oranges_r', ax=ax, edgecolor='white')
            ax.set_title('Top 10 Run Scorers in IPL History')
            ax.set_xlabel('Total Runs')
            ax.set_ylabel('')
            plt.tight_layout()
            render_chart(fig)

    with tab2:
        st.subheader("🎯 Top 10 Wicket Takers")
        top_bowlers = get_top_bowlers(deliveries).reset_index()
        top_bowlers.columns = ['Bowler', 'Wickets']

        col1, col2 = st.columns([1, 2])
        with col1:
            styled_table(top_bowlers, gradient_col='Wickets', cmap='Purples')
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=top_bowlers, x='Wickets', y='Bowler',
                        palette='Purples_r', ax=ax, edgecolor='white')
            ax.set_title('Top 10 Wicket Takers in IPL History')
            ax.set_xlabel('Total Wickets')
            ax.set_ylabel('')
            plt.tight_layout()
            render_chart(fig)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💥 Top 10 Six Hitters")
            top_sixes = get_top_sixes(deliveries).reset_index()
            top_sixes.columns = ['Player', 'Sixes']
            styled_table(top_sixes, gradient_col='Sixes', cmap='Reds')

        with col2:
            st.subheader("🎯 Top 10 Four Hitters")
            top_fours = get_top_fours(deliveries).reset_index()
            top_fours.columns = ['Player', 'Fours']
            styled_table(top_fours, gradient_col='Fours', cmap='Blues')

    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🟠 Orange Cap Holders")
            orange_cap = get_orange_cap_per_season(matches, deliveries)
            styled_table(orange_cap, gradient_col='Runs', cmap='Oranges')
        with col2:
            st.subheader("🟣 Purple Cap Holders")
            purple_cap = get_purple_cap_per_season(matches, deliveries)
            styled_table(purple_cap, gradient_col='Wickets', cmap='Purples')

        st.markdown("---")

        st.subheader("📈 Orange Cap Runs Trend")
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=orange_cap, x='Season', y='Runs',
                     marker='o', color='#f97316',
                     linewidth=2.5, markersize=9, ax=ax)
        for _, row in orange_cap.iterrows():
            ax.annotate(row['Player'], (row['Season'], row['Runs']),
                        textcoords="offset points", xytext=(0, 10),
                        ha='center', fontsize=8, color='white')
        ax.set_title('Orange Cap - Runs Per Season')
        ax.set_xlabel('Season')
        ax.set_ylabel('Runs')
        plt.xticks(rotation=45)
        plt.tight_layout()
        render_chart(fig)

        st.subheader("📈 Purple Cap Wickets Trend")
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=purple_cap, x='Season', y='Wickets',
                     marker='o', color='#a855f7',
                     linewidth=2.5, markersize=9, ax=ax)
        for _, row in purple_cap.iterrows():
            ax.annotate(row['Player'], (row['Season'], row['Wickets']),
                        textcoords="offset points", xytext=(0, 10),
                        ha='center', fontsize=8, color='white')
        ax.set_title('Purple Cap - Wickets Per Season')
        ax.set_xlabel('Season')
        ax.set_ylabel('Wickets')
        plt.xticks(rotation=45)
        plt.tight_layout()
        render_chart(fig)

    with tab5:
        st.subheader("🧤 Top 10 Wicketkeepers")
        top_keepers = get_top_keepers(deliveries).reset_index()
        top_keepers.columns = ['Wicketkeeper', 'Dismissals']

        col1, col2 = st.columns([1, 2])
        with col1:
            styled_table(top_keepers, gradient_col='Dismissals', cmap='RdPu')
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=top_keepers, x='Dismissals',
                        y='Wicketkeeper',
                        palette='RdPu_r', ax=ax, edgecolor='white')
            ax.set_title('Top 10 Wicketkeepers by Dismissals')
            ax.set_ylabel('')
            plt.tight_layout()
            render_chart(fig)

    st.markdown("---")
    st.subheader("⭐ Most Player of the Match Awards")
    top_pom = get_top_pom(matches).reset_index()
    top_pom.columns = ['Player', 'Awards']

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=top_pom, x='Player', y='Awards',
                palette='YlOrBr_r', ax=ax, edgecolor='white')
    ax.set_title('Most Player of the Match Awards')
    ax.set_ylabel('Awards')
    ax.set_xlabel('')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    render_chart(fig)


# ==========================================
# VENUE ANALYSIS
# ==========================================
elif page == "Venue":
    section_heading("🏟️ Venue Analysis")

    st.subheader("🏟️ Top 10 Venues by Matches Hosted")
    top_venues = get_top_venues(matches).reset_index()
    top_venues.columns = ['Venue', 'Matches']

    col1, col2 = st.columns([1, 2])
    with col1:
        styled_table(top_venues, gradient_col='Matches', cmap='Greens')
    with col2:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=top_venues, x='Matches', y='Venue',
                    palette='Greens_r', ax=ax, edgecolor='white')
        ax.set_title('Top 10 IPL Venues by Matches Hosted')
        ax.set_ylabel('')
        for i, v in enumerate(top_venues['Matches']):
            ax.text(v + 0.5, i, str(v), va='center',
                    color='white', fontweight='bold')
        plt.tight_layout()
        render_chart(fig)

    st.markdown("---")

    st.subheader("🔥 Highest Scoring Venues")
    venue_avg = get_highest_scoring_venues(matches, deliveries).reset_index()
    venue_avg.columns = ['Venue', 'Avg Score']

    col1, col2 = st.columns([1, 2])
    with col1:
        styled_table(venue_avg, gradient_col='Avg Score', cmap='Oranges')
    with col2:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=venue_avg, x='Avg Score', y='Venue',
                    palette='Oranges_r', ax=ax, edgecolor='white')
        ax.set_title('Highest Scoring Venues - Avg 1st Innings Score')
        ax.set_ylabel('')
        for i, v in enumerate(venue_avg['Avg Score']):
            ax.text(v + 0.3, i, f'{v:.1f}', va='center',
                    color='white', fontweight='bold')
        plt.tight_layout()
        render_chart(fig)


# ==========================================
# HEAD-TO-HEAD
# ==========================================
elif page == "Head-to-Head":
    section_heading("⚔️ Head-to-Head Analysis")

    all_teams = sorted(matches['team1_std'].dropna().unique())

    col1, col2 = st.columns(2)
    with col1:
        team_a = st.selectbox("Select Team A", all_teams, index=0)
    with col2:
        team_b = st.selectbox("Select Team B", all_teams, index=1)

    if team_a == team_b:
        st.warning("⚠️ Please select two different teams.")
    else:
        total, a_wins, b_wins, no_result = get_head_to_head(matches, team_a, team_b)

        if total == 0:
            st.info(f"{team_a} and {team_b} have never played each other.")
        else:
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            with col1: metric_card("Total Matches", total)
            with col2: metric_card(f"{team_a} Wins", a_wins)
            with col3: metric_card(f"{team_b} Wins", b_wins)
            with col4: metric_card("No Result", no_result)

            st.markdown("---")
            st.subheader(f"📊 {team_a} vs {team_b} - Win Share")

            labels = [team_a, team_b]
            values = [a_wins, b_wins]
            colors = ['#3b82f6', '#f97316']

            if no_result > 0:
                labels.append("No Result")
                values.append(no_result)
                colors.append('#64748b')

            fig, ax = plt.subplots(figsize=(7, 7))
            ax.pie(values, labels=labels, colors=colors,
                   autopct='%1.1f%%', startangle=90,
                   explode=[0.05] * len(values), shadow=True,
                   textprops={'color': 'white', 'fontsize': 13, 'fontweight': 'bold'})
            ax.set_title(f'{team_a} vs {team_b}')
            plt.tight_layout()
            render_chart(fig)


# ==========================================
# PREDICTOR PAGE
# ==========================================
elif page == "Predictor":
    section_heading("🤖 First Innings Score Predictor")

    st.markdown("""
    <div class="info-card">
        Enter the live match situation below and our <b>Linear Regression Model</b> 
        will predict the final 1st innings score. Trained on 85,000+ deliveries 
        from IPL 2008–2024.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    teams = metadata['teams']
    venues = metadata['venues']

    col1, col2, col3 = st.columns(3)
    with col1:
        batting_team = st.selectbox("🏏 Batting Team", teams)
    with col2:
        bowling_team = st.selectbox("🎯 Bowling Team",
                                    [t for t in teams if t != batting_team])
    with col3:
        venue = st.selectbox("🏟️ Venue", venues)

    st.markdown("---")
    st.markdown("### 📊 Current Match Situation")

    col1, col2, col3 = st.columns(3)
    with col1:
        current_runs = st.number_input("Current Runs", min_value=0, max_value=300, value=80, step=1)
    with col2:
        current_wickets = st.number_input("Wickets Fallen", min_value=0, max_value=9, value=2, step=1,
                                 help="Innings ends at 10 wickets")
    with col3:
        over_options = []
        for over in range(5, 20):
            for ball in range(0, 6):
                over_options.append(f"{over}.{ball}")
        
        overs_str = st.selectbox("Overs Completed", over_options, index=30)
        
        parts = overs_str.split('.')
        total_balls = int(parts[0]) * 6 + int(parts[1])
        overs_decimal = round(total_balls / 6, 2)

    col1, col2 = st.columns(2)
    with col1:
        runs_last_5 = st.number_input(
        "Runs in Last 5 Overs",
        min_value=0,
        max_value=current_runs,
        value=min(40, current_runs),
        step=1,
        help=f"Cannot exceed current runs ({current_runs})"
    )
    with col2:
        wickets_last_5 = st.number_input(
        "Wickets in Last 5 Overs",
        min_value=0,
        max_value=current_wickets,
        value=min(2, current_wickets),
        step=1,
        help=f"Cannot exceed wickets fallen ({current_wickets})"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    validation_passed = True
    if runs_last_5 > current_runs:
        st.warning("⚠️ Runs in last 5 overs cannot exceed current total runs!")
        validation_passed = False
    if wickets_last_5 > current_wickets:
        st.warning("⚠️ Wickets in last 5 overs cannot exceed total wickets fallen!")
        validation_passed = False
    if batting_team == bowling_team:
        st.error("Batting team and bowling team must be different!")
        validation_passed = False

    if st.button("🔮 Predict Final Score", use_container_width=True, disabled=not validation_passed):
        predicted = predict_score(
            model, batting_team, bowling_team, venue,
            current_runs, current_wickets, overs_decimal,
            runs_last_5, wickets_last_5
        )

        lower = max(predicted - 10, current_runs)
        upper = predicted + 10
        
        st.markdown(f"""
        <div class="prediction-card">
            <div class="prediction-label">Predicted Final Score</div>
            <div class="prediction-value">{predicted}</div>
            <div class="prediction-range">Likely Range: {lower} - {upper} runs</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        crr = round(current_runs / overs_decimal, 2)
        overs_left = round(20 - overs_decimal, 2)
        runs_needed = predicted - current_runs
        rrr_needed = round(runs_needed / overs_left, 2) if overs_left > 0 else 0
        
        with col1: metric_card("Current RR", f"{crr}")
        with col2: metric_card("Overs Left", f"{overs_left}")
        with col3: metric_card("Runs to Add", f"{runs_needed}")
        with col4: metric_card("Required RR", f"{rrr_needed}")


# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#94a3b8;'>"
    "IPL Analytics Dashboard | All About Cric... 🏏</p>",
    unsafe_allow_html=True
)