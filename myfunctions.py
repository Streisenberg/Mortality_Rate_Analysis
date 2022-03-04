import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import sys  
import os
import math
from geopy.geocoders import Nominatim
import plotly_express as px 

both = pd.read_csv("Both_sexes.csv")
male = pd.read_csv("male.csv")
female = pd.read_csv("female.csv")

#Bu fonksiyon verdiğimiz veriyi bölgesel olarak ayırmayı ve bunları ölüm oranının çokluğundan azlığına göre sıralamayı sağlıyor
def createTable(location, table):
    global new_table
    new_table = table[table["ParentLocation"] == location].sort_values(by = "Adult mortality rate", ascending = False)
    st.write(new_table[["ParentLocation", "Location", "Period", "Sex", "Adult mortality rate"]])

def yearTable(year, table, location):
    year = table[(table["Period"] == year) & (table["ParentLocation"] == location)].sort_values(by = "Adult mortality rate", ascending = False)
    st.write(year[["ParentLocation", "Location", "Period", "Sex", "Adult mortality rate"]])

def yearGraph(year, table, location):
    fig = plt.figure(figsize = (12, 9))
    sns.barplot(y = "Location", x = "Adult mortality rate", linewidth = 2 ,data = table[(table["ParentLocation"] == location) & (table["Period"] == year)].groupby(["Location"]).mean().reset_index().sort_values(by = "Adult mortality rate", ascending = False))
    plt.title("{} Yılındaki Ortalama Ölüm Oranı".format(year))
    plt.xlabel("Ölüm Oranı")
    plt.ylabel("Ülkeler")
    st.pyplot(fig)

def mapping(country, location, lati, longi):
    loc_sum = both[both["ParentLocation"] == location].groupby(["Location"]).sum().reset_index(). sort_values(by = "Adult mortality rate", ascending = False)
    loc_sum = loc_sum[["Location", "Adult mortality rate"]]
    if st.checkbox("{} Haritası v Ölüm Oranları Grafiği".format(country)):
        geolocator = Nominatim(user_agent="myGeolocator")
        country_loc = loc_sum["Location"].unique()
        for i in country_loc:
            def func(i):
                return geolocator.geocode(i).latitude
        loc_sum["latitude"] = loc_sum["Location"].apply(func)
        for i in country_loc:
            def func2(i):
                return geolocator.geocode(i).longitude
        loc_sum["longitude"] = loc_sum["Location"].apply(func2)

        fig = px.scatter_mapbox(loc_sum, lat = "latitude", lon = "longitude", hover_name="Location", hover_data = ["Adult mortality rate"], color = "Adult mortality rate", size = "Adult mortality rate", size_max = 30, opacity = 0.5, center = {"lat": lati, "lon": longi}, zoom = 2, height = 800, width = 800)
        fig.update_layout(mapbox_style = "open-street-map")
        fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(title_text = "{} Yetişkin Ölüm Oranları".format(country))
        st.plotly_chart(fig)

def comparison(country, location):
    radio = st.radio("Seçiminizi Yapın: ", ["{} ortalama ölüm oranı EN YÜKSEK 10 ülke".format(country),"{} ortalama ölüm oranı EN DÜŞÜK 10 ülke".format(country)])
    subset = both[both["ParentLocation"] == location]
    both_location = subset.groupby(["Location"]).mean().reset_index().sort_values(by= "Adult mortality rate", ascending = False)
    if radio == "{} ortalama ölüm oranı EN YÜKSEK 10 ülke".format(country):
        st.write(both_location[["Location", "Adult mortality rate"]].head(10))

        if st.button("Karşılaştırma Grafiği"):
            liste = []
            for i in both_location["Location"].head(10):
                liste.append(i)
            f_m = pd.concat([female, male])
            top5 = f_m[f_m["Location"].isin(liste)]
            top5 = top5[["Location", "Sex", "Adult mortality rate"]].groupby(["Location", "Sex"]).mean().reset_index()
            fig = plt.figure(figsize=(12,9))
            hue_order = ["Male", "Female"]
            sns.barplot(x = "Location", y = "Adult mortality rate", hue = "Sex", hue_order= hue_order, data = top5)
            plt.xticks(rotation = 45)
            st.pyplot(fig)
        
    elif radio == "{} ortalama ölüm oranı EN DÜŞÜK 10 ülke".format(country):
        st.write(both_location[["Location", "Adult mortality rate"]].tail(10))
        if st.button("Karşılaştırma Grafiği"):
            liste = []
            for i in both_location["Location"].tail(10):
                liste.append(i)
            df_concat = pd.concat([female, male])
            bottom5 = df_concat[df_concat["Location"].isin(liste)]
            bottom5 = bottom5[["Location", "Sex", "Adult mortality rate"]].groupby(["Location", "Sex"]).mean().reset_index()
            fig = plt.figure(figsize=(12,9))
            hue_order = ["Male", "Female"]
            sns.barplot(x = "Location", y = "Adult mortality rate", hue = "Sex", hue_order= hue_order, data = bottom5)
            plt.xticks(rotation = 45)
            st.pyplot(fig)


