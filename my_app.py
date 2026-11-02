import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")
df = pd.read_csv("data/cleaned_dataset.csv", parse_dates=["Order Date"])

df["Route (State)"] = df["Factory"] + " → " + df["State/Province"]

# sidebar filters
st.sidebar.title("Filters")
modes = st.sidebar.multiselect("Ship mode", df["Ship Mode"].unique(), default=list(df["Ship Mode"].unique()))
regions = st.sidebar.multiselect("Region", df["Region"].unique(), default=list(df["Region"].unique()))
states = st.sidebar.multiselect("State (leave empty for all)", sorted(df["State/Province"].unique()))
d_min, d_max = df["Order Date"].min().date(), df["Order Date"].max().date()
dates = st.sidebar.date_input("Order date range", (d_min, d_max), min_value=d_min, max_value=d_max)
thr = st.sidebar.slider("Delay threshold (days)", 1, 11, 6)

f = df[df["Ship Mode"].isin(modes) & df["Region"].isin(regions)].copy()
if states:
    f = f[f["State/Province"].isin(states)]
if len(dates) == 2:
    f = f[(f["Order Date"].dt.date >= dates[0]) & (f["Order Date"].dt.date <= dates[1])]
f["Delayed"] = f["Lead Time"] > thr

st.title("Shipping Route Efficiency")
c1, c2, c3 = st.columns(3)
c1.metric("Shipments", len(f))
c2.metric("Avg lead time", round(f["Lead Time"].mean(), 2))
c3.metric("Delay %", round(f["Delayed"].mean() * 100, 1))

tab1, tab2, tab3, tab4 = st.tabs(["Routes", "Ship modes", "State drill-down", "Map"])

with tab1:
    r = (f.groupby("Route (State)").agg(Shipments=("Lead Time", "size"),
         Avg_Lead_Time=("Lead Time", "mean")).query("Shipments >= 20")
         .sort_values("Avg_Lead_Time").reset_index())
    st.subheader("Fastest 10"); st.dataframe(r.head(10))
    st.subheader("Slowest 10"); st.dataframe(r.tail(10))

with tab2:
    st.plotly_chart(px.box(f, x="Ship Mode", y="Lead Time"))

with tab3:
    s = st.selectbox("State", sorted(f["State/Province"].unique()))
    st.dataframe(f[f["State/Province"] == s][["Order ID", "Factory", "Ship Mode", "Order Date", "Lead Time"]])

STATE_ABBR = {
 'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT',
 'Delaware':'DE','District of Columbia':'DC','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL',
 'Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD',
 'Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT',
 'Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY',
 'North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA',
 'Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT',
 'Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

with tab4:
    m = f.copy()
    m["abbr"] = m["State/Province"].map(STATE_ABBR)
    m = m.dropna(subset=["abbr"])
    sg = m.groupby("abbr").agg(Shipments=("Lead Time", "size"),
                               Avg_Lead_Time=("Lead Time", "mean"),
                               Delay_Pct=("Delayed", "mean")).reset_index()
    sg["Delay_Pct"] = sg["Delay_Pct"] * 100
    metric = st.selectbox("Map metric", ["Avg_Lead_Time", "Delay_Pct", "Shipments"])
    fig = px.choropleth(sg, locations="abbr", locationmode="USA-states", scope="usa",
                        color=metric, color_continuous_scale="RdYlGn_r",
                        hover_data=["Shipments", "Avg_Lead_Time", "Delay_Pct"])
    st.plotly_chart(fig)
    st.caption("Green = faster, red = slower. Canadian provinces are not shown.")
    st.subheader("Slowest states (min. 50 shipments)")
    st.dataframe(sg[sg["Shipments"] >= 50].sort_values("Avg_Lead_Time", ascending=False).head(10))
