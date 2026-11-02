
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Nassau Candy - Shipping Analytics",
    page_icon="🍬",
    layout="wide"
)

# Load dataset
df = pd.read_csv(
    "data/cleaned_dataset.csv",
    parse_dates=["Order Date"]
)

df["Route (State)"] = (
    df["Factory"].astype(str) + " → " +
    df["State/Province"].astype(str)
)

# Dark theme for charts
chart_theme = "plotly_dark"

# Sidebar filters
st.sidebar.title("Filters")

modes = st.sidebar.multiselect(
    "Ship mode",
    sorted(df["Ship Mode"].dropna().unique()),
    default=list(df["Ship Mode"].dropna().unique())
)

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].dropna().unique()),
    default=list(df["Region"].dropna().unique())
)

states = st.sidebar.multiselect(
    "State",
    sorted(df["State/Province"].dropna().unique())
)

d_min = df["Order Date"].min().date()
d_max = df["Order Date"].max().date()

dates = st.sidebar.date_input(
    "Order date range",
    (d_min, d_max),
    min_value=d_min,
    max_value=d_max
)

thr = st.sidebar.slider(
    "Delay threshold (days)", 1, 11, 6
)

# Apply filters
f = df[
    df["Ship Mode"].isin(modes) &
    df["Region"].isin(regions)
].copy()

if states:
    f = f[f["State/Province"].isin(states)]

if len(dates) == 2:
    f = f[
        (f["Order Date"].dt.date >= dates[0]) &
        (f["Order Date"].dt.date <= dates[1])
    ]

f["Delayed"] = f["Lead Time"] > thr

# Dashboard title
st.title("🍬 Shipping Route Efficiency")
st.caption("Nassau Candy Distributor | Shipping Performance Analytics")

if f.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

# KPI metrics
c1, c2, c3 = st.columns(3)

c1.metric("Total Shipments", f"{len(f):,}")
c2.metric("Average Lead Time", f"{f['Lead Time'].mean():.2f} days")
c3.metric("Delay Percentage", f"{f['Delayed'].mean() * 100:.1f}%")

st.divider()

# Four dashboard sections
tab1, tab2, tab3, tab4 = st.tabs([
    "Routes",
    "Ship modes",
    "State drill-down",
    "Map"
])

# --------------------------------------------------
# TAB 1: ROUTE ANALYSIS
# --------------------------------------------------

with tab1:

    st.header("Shipping Route Performance")

    r = (
        f.groupby("Route (State)")
        .agg(
            Shipments=("Lead Time", "size"),
            Avg_Lead_Time=("Lead Time", "mean")
        )
        .query("Shipments >= 20")
        .reset_index()
    )

    fastest = r.sort_values("Avg_Lead_Time").head(10)
    slowest = r.sort_values("Avg_Lead_Time", ascending=False).head(10)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 Fastest 10 Routes")

        fig = px.bar(
            fastest.sort_values("Avg_Lead_Time", ascending=True),
            x="Avg_Lead_Time",
            y="Route (State)",
            orientation="h",
            color="Avg_Lead_Time",
            color_continuous_scale="Greens",
            hover_data=["Shipments"],
            title="Fastest Shipping Routes",
            template=chart_theme
        )

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("⚠️ Slowest 10 Routes")

        fig = px.bar(
            slowest.sort_values("Avg_Lead_Time"),
            x="Avg_Lead_Time",
            y="Route (State)",
            orientation="h",
            color="Avg_Lead_Time",
            color_continuous_scale="Reds",
            hover_data=["Shipments"],
            title="Slowest Shipping Routes",
            template=chart_theme
        )

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Route Performance Details")

    st.dataframe(
        r.sort_values("Avg_Lead_Time"),
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# TAB 2: SHIPPING MODE ANALYSIS
# --------------------------------------------------

with tab2:

    st.header("Shipping Mode Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Lead Time Distribution")

        fig = px.box(
            f,
            x="Ship Mode",
            y="Lead Time",
            color="Ship Mode",
            title="Lead Time by Shipping Mode",
            template=chart_theme
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Average Lead Time")

        mode_avg = (
            f.groupby("Ship Mode")
            .agg(
                Avg_Lead_Time=("Lead Time", "mean"),
                Shipments=("Lead Time", "size")
            )
            .reset_index()
        )

        fig = px.bar(
            mode_avg,
            x="Ship Mode",
            y="Avg_Lead_Time",
            color="Ship Mode",
            text_auto=".2f",
            title="Average Lead Time by Ship Mode",
            template=chart_theme
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Shipping Mode Summary")

    st.dataframe(
        mode_avg,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# TAB 3: STATE DRILL-DOWN
# --------------------------------------------------

with tab3:

    st.header("State-wise Performance Analysis")

    state_summary = (
        f.groupby("State/Province")
        .agg(
            Shipments=("Lead Time", "size"),
            Avg_Lead_Time=("Lead Time", "mean"),
            Delay_Pct=("Delayed", "mean")
        )
        .reset_index()
    )

    state_summary["Delay_Pct"] *= 100

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Average Lead Time by State")

        fig = px.bar(
            state_summary.sort_values("Avg_Lead_Time"),
            x="Avg_Lead_Time",
            y="State/Province",
            orientation="h",
            color="Avg_Lead_Time",
            color_continuous_scale="RdYlGn_r",
            title="State-wise Average Lead Time",
            template=chart_theme
        )

        fig.update_layout(height=650)
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Shipment Volume by State")

        fig = px.bar(
            state_summary.sort_values("Shipments", ascending=False).head(15),
            x="Shipments",
            y="State/Province",
            orientation="h",
            color="Shipments",
            title="Top 15 States by Shipment Volume",
            template=chart_theme
        )

        fig.update_layout(height=650)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Explore Individual State")

    selected_state = st.selectbox(
        "Select a state",
        sorted(f["State/Province"].dropna().unique())
    )

    state_data = f[
        f["State/Province"] == selected_state
    ]

    st.write(f"Shipment details for {selected_state}")

    st.dataframe(
        state_data[
            ["Order ID", "Factory", "Ship Mode",
             "Order Date", "Lead Time"]
        ],
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# TAB 4: GEOGRAPHICAL MAP
# --------------------------------------------------

STATE_ABBR = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ',
    'Arkansas':'AR','California':'CA','Colorado':'CO',
    'Connecticut':'CT','Delaware':'DE',
    'District of Columbia':'DC','Florida':'FL',
    'Georgia':'GA','Hawaii':'HI','Idaho':'ID',
    'Illinois':'IL','Indiana':'IN','Iowa':'IA',
    'Kansas':'KS','Kentucky':'KY','Louisiana':'LA',
    'Maine':'ME','Maryland':'MD','Massachusetts':'MA',
    'Michigan':'MI','Minnesota':'MN','Mississippi':'MS',
    'Missouri':'MO','Montana':'MT','Nebraska':'NE',
    'Nevada':'NV','New Hampshire':'NH',
    'New Jersey':'NJ','New Mexico':'NM',
    'New York':'NY','North Carolina':'NC',
    'North Dakota':'ND','Ohio':'OH','Oklahoma':'OK',
    'Oregon':'OR','Pennsylvania':'PA',
    'Rhode Island':'RI','South Carolina':'SC',
    'South Dakota':'SD','Tennessee':'TN','Texas':'TX',
    'Utah':'UT','Vermont':'VT','Virginia':'VA',
    'Washington':'WA','West Virginia':'WV',
    'Wisconsin':'WI','Wyoming':'WY'
}

with tab4:

    st.header("Geographical Shipping Analysis")

    m = f.copy()

    m["abbr"] = m["State/Province"].map(STATE_ABBR)

    m = m.dropna(subset=["abbr"])

    sg = (
        m.groupby("abbr")
        .agg(
            Shipments=("Lead Time", "size"),
            Avg_Lead_Time=("Lead Time", "mean"),
            Delay_Pct=("Delayed", "mean")
        )
        .reset_index()
    )

    sg["Delay_Pct"] *= 100

    metric = st.selectbox(
        "Select Map Metric",
        ["Avg_Lead_Time", "Delay_Pct", "Shipments"]
    )

    fig = px.choropleth(
        sg,
        locations="abbr",
        locationmode="USA-states",
        scope="usa",
        color=metric,
        color_continuous_scale="RdYlGn_r",
        hover_data=[
            "Shipments",
            "Avg_Lead_Time",
            "Delay_Pct"
        ],
        title=f"US State-wise {metric}",
        template=chart_theme
    )

    fig.update_layout(height=650)

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Green = lower values; Red = higher values. "
        "Canadian provinces are not displayed."
    )

    st.subheader("Slowest States")

    st.dataframe(
        sg[sg["Shipments"] >= 50]
        .sort_values("Avg_Lead_Time", ascending=False)
        .head(10),
        use_container_width=True,
        hide_index=True
    )

