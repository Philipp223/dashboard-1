import streamlit as st
import pandas as pd

excel_path = "Musterdaten-Sellerboard-daily.xlsx"

# --- Daten einlesen ---
df = pd.read_excel(excel_path)
df["order-date"] = pd.to_datetime(df["order-date"], errors="coerce")

# --- Date Range Picker einfügen ---
# Standardwerte: min/max aus den Daten
min_date_total = df["order-date"].min().date()
max_date_total = df["order-date"].max().date()

start_date, end_date = st.date_input(
    "Zeitraum auswählen:",
    value=[min_date_total, max_date_total],
    min_value=min_date_total,
    max_value=max_date_total
)

# --- Daten filtern ---
mask = (df["order-date"] >= pd.to_datetime(start_date)) & (df["order-date"] <= pd.to_datetime(end_date))
df_filtered = df.loc[mask]

# --- Dynamischer Titel ---
if not df_filtered.empty:
    min_date = df_filtered["order-date"].min().date()
    max_date = df_filtered["order-date"].max().date()
    st.write(f"📊 Musterunternehmen Absatz von {min_date} bis {max_date}")

    # --- Tabelle und Chart ---
    st.dataframe(df_filtered.groupby("asin").units.sum())
    st.write(f"📊 Absatz pro KW von {min_date} bis {max_date}")
    st.dataframe(
    df_filtered.pivot_table(
        index="asin",
        columns=pd.Grouper(key="order-date", freq="W"),
        values="units",
        aggfunc="sum",
        fill_value=0
    )
)
    st.write("Units pro ASIN")
    st.bar_chart(df_filtered, x="asin", y="units", color="asin")
    st.write("Units pro Tag")
    st.line_chart(df_filtered.groupby("order-date")["units"].sum().reset_index(),x="order-date", y="units")
    st.write("Sales pro Tag (€)")
    st.line_chart(df_filtered.groupby("order-date")["sales"].sum().reset_index(),x="order-date", y="sales")
else:
    st.warning("⚠️ Keine Daten im gewählten Zeitraum gefunden.")