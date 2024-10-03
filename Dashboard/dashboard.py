import pandas as pd
import matplotlib as plt
import seaborn as sns
import streamlit as st


sns.set(style='dark')

def create_season_df(df):
    season_df = df.groupby(by="season")['count_total'].sum().reset_index()
    return season_df

def create_weather_df(df):
    weather_df = df.groupby(by="weather_situation")['count_total'].sum().reset_index()
    return weather_df

def create_monthly_df(df):
    df['month'] = df['dateday'].dt.to_period('M')
    monthly_df = df.groupby(by='month')['count_total'].sum()
    return monthly_df

def create_holiday_df(df):
    holiday_df = df.groupby(by="holiday")['count_total'].mean().reset_index()
    return holiday_df

def temp_group(temp):
    if temp<0.34:
        return "Low"
    elif 0.34<= temp <= 0.65:
        return "Medium"
    else:
        return "High"

def create_temp_df(df):
    df['temp_category'] = df['temp'].apply(temp_group)
    temp_df = df.groupby('temp_category')['count_total'].sum()
    return temp_df


day_df = pd.read_csv('/Dashboard/day_main.csv')
day_df['dateday'] = pd.to_datetime(day_df['dateday'])
day_df.sort_values(by="dateday", inplace=True)


min_date = day_df["dateday"].min()
max_date = day_df["dateday"].max()
with st.sidebar:
    st.image(cwd + "\\Dashboard\\rental3.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = day_df[(day_df["dateday"] >= str(start_date)) & 
                (day_df["dateday"] <= str(end_date))]

season_df = create_season_df(main_df)
weather_df = create_weather_df(main_df)
monthly_df = create_monthly_df(main_df)
temp_df = create_temp_df(main_df)
holiday_df = create_holiday_df(main_df)

st.header('Proyek Analisis Data Bike 🚲:sparkles:')

st.subheader('Total Rental Bikes Berdasarkan Cuaca')
fig, ax = plt.subplots()
colors = ["#0561f5", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="weather_situation", y="count_total", data=weather_df.sort_values(by='count_total', ascending=False),ci=None, palette=colors)
ax.set_ylabel("Total Rental Bikes")
ax.set_xlabel("Weather Condition")
ax.set_title("Total Rental Bikes in Various Weather")
for i, value in enumerate(weather_df.sort_values(by='count_total', ascending=False)['count_total']):
    plt.text(i, value + 10, f'{value}', ha='center', va='bottom')
st.pyplot(fig)

st.subheader('Total Rental Bikes Berdasarkan Hari Libur')
fig, ax = plt.subplots()
sns.barplot(x="holiday", y="count_total", data=holiday_df.sort_values(by='holiday', ascending=False),ci=None, palette=colors)
ax.set_ylabel("Average Rental Bikes")
ax.set_xlabel("Holiday")
ax.set_title("Average Rental Bikes in Holiday")
for i, value in enumerate(holiday_df.sort_values(by='count_total', ascending=False)['count_total']):
    plt.text(i, value + 10, f'{value}', ha='center', va='bottom')
st.pyplot(fig)
with st.expander('Keterangan'):
    st.write(
        """
        0 = Non-holiday
        1 = Holiday
        """
    )

st.subheader('Perkembangan Rental Sepeda')
fig, ax = plt.subplots()
plt.plot(monthly_df.index.astype(str), monthly_df.values, color='red', marker='o')
ax.tick_params(axis='x', rotation=60)
ax.set_xlabel("Year-Month")
ax.set_ylabel("Total Rental Bikes")
ax.set_title("Development of Rental Bikes")
st.pyplot(fig)