import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import sys  
import os 
from myfunctions import createTable, yearTable, yearGraph
import math
from geopy.geocoders import Nominatim
import plotly_express as px


#Verileri toplama işlemi
both = pd.read_csv("Both_sexes.csv")
male = pd.read_csv("male.csv")
female = pd.read_csv("female.csv")

def main():

    st.title("Hi-Kod Adult Mortality Rate Project")

    sidebar = st.sidebar.radio("İşleminizi Seçin: ", ["Genel Analiz", "Kadın-Erkek Karşılaştırma"])

    if sidebar == "Genel Analiz":

        select_box = st.selectbox("Veriler", ["Her iki cins", "Erkek", "Dişi"])

        if select_box == "Her iki cins":
            st.write(both)
            if st.button("Genel Grafiği Görüntüle (Her İki Cins)"):
                both_mean = both[["ParentLocation", "Period", "Adult mortality rate"]].groupby(["ParentLocation", "Period"]).mean().reset_index().rename(columns = {"Adult mortality rate": "mean"})
                fig = plt.figure(figsize = (17, 10))
                sns.barplot(x = "Period", y = "mean", hue = "ParentLocation", data = both_mean)
                plt.xlabel("Yıl", fontsize = 14, fontweight = "bold")
                plt.ylabel("Ortalama", fontsize = 14, fontweight = "bold")
                st.pyplot(fig)

        elif select_box == "Erkek":
            st.write(male)
            if st.button("Genel Grafiği Görüntüle (Erkek)"):
                male_mean = male[["ParentLocation", "Period", "Adult mortality rate"]].groupby(["ParentLocation", "Period"]).mean().reset_index().rename(columns = {"Adult mortality rate": "mean"})
                fig = plt.figure(figsize = (17, 10))
                sns.barplot(x = "Period", y = "mean", hue = "ParentLocation", data = male_mean)
                plt.xlabel("Yıl", fontsize = 14, fontweight = "bold")
                plt.ylabel("Ortalama", fontsize = 14, fontweight = "bold")
                st.pyplot(fig)
        elif select_box == "Dişi":
            st.write(female)
            if st.button("Genel Grafiği Görüntüle (Dişi)"):
                female_mean = female[["ParentLocation", "Period", "Adult mortality rate"]].groupby(["ParentLocation", "Period"]).mean().reset_index().rename(columns = {"Adult mortality rate": "mean"})
                fig = plt.figure(figsize = (17, 10))
                sns.barplot(x = "Period", y = "mean", hue = "ParentLocation", data = female_mean)
                plt.xlabel("Yıl", fontsize = 14, fontweight = "bold")
                plt.ylabel("Ortalama", fontsize = 14, fontweight = "bold")
                st.pyplot(fig)

        radio = st.radio("Bölgesel Veri", ["Afrika", "Amerika", "Avrupa", "Batı Pasifik", "Doğu Akdeniz", "Güneydoğu Asya"])

        if radio == "Afrika":
            if select_box == "Her iki cins":
                createTable("Africa", both)

                #Afrikadaki ülkelerin her birinin ayrı ayrı ölüm oranları
                if st.button("Afrika Ülkelerinin Grafiğini Görüntüle (Her İki Cins)"):
                    both_africa = both[both["ParentLocation"] == "Africa"]
                    country_africa = both_africa["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_africa) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_africa:
                        axs[i][j].scatter(data = both_africa[both_africa["Location"] == c], x = "Period", y = "Adult mortality rate", color = "b", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig)  
                
                #Afrika kıtası üzerinde harita ile grafik oluşturma 
                africa_sum = both[both["ParentLocation"] == "Africa"].groupby(["Location"]).sum().reset_index(). sort_values(by = "Adult mortality rate", ascending = False)
                africa_sum = africa_sum[["Location", "Adult mortality rate"]]
                if st.checkbox("Afrika Haritası v Ölüm Oranları Grafiği"):
                    geolocator = Nominatim(user_agent="myGeolocator")
                    country_africa = africa_sum["Location"].unique()
                    for i in country_africa:
                        def func(i):
                            return geolocator.geocode(i).latitude
                    africa_sum["latitude"] = africa_sum["Location"].apply(func)
                    for i in country_africa:
                        def func2(i):
                            return geolocator.geocode(i).longitude
                    africa_sum["longitude"] = africa_sum["Location"].apply(func2)

                    fig = px.scatter_mapbox(africa_sum, lat = "latitude", lon = "longitude", hover_name="Location", hover_data = ["Adult mortality rate"], color = "Adult mortality rate", size = "Adult mortality rate", size_max = 30, opacity = 0.5, center = {"lat": -14.44, "lon": 22.7}, zoom = 2, height = 800, width = 800)
                    fig.update_layout(mapbox_style = "open-street-map")
                    fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0})
                    fig.update_layout(title_text = "Afrikadaki Yetişkin Ölüm Oranları")
                    st.plotly_chart(fig)

            elif select_box == "Erkek":
                createTable("Africa", male)

                if st.button("Afrika Ülkelerinin Grafiğini Görüntüle (Erkek)"):
                    male_africa = male[male["ParentLocation"] == "Africa"]
                    country_africa_male = male_africa["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_africa_male) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_africa_male:
                        axs[i][j].scatter(data = male_africa[male_africa["Location"] == c], x = "Period", y = "Adult mortality rate", color = "b", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig)  

            elif select_box == "Dişi":
                createTable("Africa", female)

                if st.button("Afrika Ülkelerinin Grafiğini Görüntüle (Dişi)"):
                    female_africa = female[female["ParentLocation"] == "Africa"]
                    country_africa_female = female_africa["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_africa_female) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_africa_female:
                        axs[i][j].scatter(data = female_africa[female_africa["Location"] == c], x = "Period", y = "Adult mortality rate", color = "b", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig)  
        elif radio == "Amerika":
            if select_box == "Her iki cins":
                createTable("Americas", both)
                #Amerikada ülkelerin her birinin ayrı ayrı ölüm oranları
                if st.button("Amerika Ülkelerinin Grafiğini Görüntüle (Her İki Cins)"):
                    both_america = both[both["ParentLocation"] == "Americas"]
                    country_america = both_america["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_america) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_america:
                        axs[i][j].scatter(data = both_america[both_america["Location"] == c], x = "Period", y = "Adult mortality rate", color = "orange", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig)  
                
                #Amerika kıtası üzerinde harita ile grafik oluşturma 
                america_sum = both[both["ParentLocation"] == "Americas"].groupby(["Location"]).sum().reset_index(). sort_values(by = "Adult mortality rate", ascending = False)
                america_sum = america_sum[["Location", "Adult mortality rate"]]
                if st.checkbox("Amerika Haritası v Ölüm Oranları Grafiği"):
                    geolocator = Nominatim(user_agent="myGeolocator")
                    country_america = america_sum["Location"].unique()
                    for i in country_america:
                        def func(i):
                            return geolocator.geocode(i).latitude
                    america_sum["latitude"] = america_sum["Location"].apply(func)
                    for i in country_america:
                        def func2(i):
                            return geolocator.geocode(i).longitude
                    america_sum["longitude"] = america_sum["Location"].apply(func2)

                    fig = px.scatter_mapbox(america_sum, lat = "latitude", lon = "longitude", hover_name="Location", hover_data = ["Adult mortality rate"], color = "Adult mortality rate", size = "Adult mortality rate", size_max = 30, opacity = 0.5, center = {"lat": -1.44, "lon": -52.7}, zoom = 2, height = 800, width = 800)
                    fig.update_layout(mapbox_style = "open-street-map")
                    fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0})
                    fig.update_layout(title_text = "Amerikadaki Yetişkin Ölüm Oranları")
                    st.plotly_chart(fig)

            elif select_box == "Erkek":
                createTable("Americas", male)
                if st.button("Amerika Ülkelerinin Grafiğini Görüntüle (Erkek)"):
                    male_america = male[male["ParentLocation"] == "Americas"]
                    country_america_male = male_america["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_america_male) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_america_male:
                        axs[i][j].scatter(data = male_america[male_america["Location"] == c], x = "Period", y = "Adult mortality rate", color = "orange", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 

            elif select_box == "Dişi":
                createTable("Americas", female)

                if st.button("Amerika Ülkelerinin Grafiğini Görüntüle (Dişi)"):
                    female_america = female[female["ParentLocation"] == "Americas"]
                    country_america_female = female_america["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_america_female) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_america_female:
                        axs[i][j].scatter(data = female_america[female_america["Location"] == c], x = "Period", y = "Adult mortality rate", color = "orange", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 
        elif radio == "Avrupa":
            if select_box == "Her iki cins":
                createTable("Europe", both)
                if st.button("Avrupa Ülkelerinin Grafiğini Görüntüle (Her İki Cins)"):
                    both_europe = both[both["ParentLocation"] == "Europe"]
                    country_europe = both_europe["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_europe) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_europe:
                        axs[i][j].scatter(data = both_europe[both_europe["Location"] == c], x = "Period", y = "Adult mortality rate", color = "r", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 

                #Güneydoğu Asya kıtası üzerinde harita ile grafik oluşturma 
                europe_sum = both[both["ParentLocation"] == "Europe"].groupby(["Location"]).sum().reset_index(). sort_values(by = "Adult mortality rate", ascending = False)
                europe_sum = europe_sum[["Location", "Adult mortality rate"]]
                if st.checkbox("Avrupa Haritası v Ölüm Oranları Grafiği"):
                    geolocator = Nominatim(user_agent="myGeolocator")
                    country_europe = europe_sum["Location"].unique()
                    for i in country_europe:
                        def func(i):
                            return geolocator.geocode(i).latitude
                    europe_sum["latitude"] = europe_sum["Location"].apply(func)
                    for i in country_europe:
                        def func2(i):
                            return geolocator.geocode(i).longitude
                    europe_sum["longitude"] = europe_sum["Location"].apply(func2)

                    fig = px.scatter_mapbox(europe_sum, lat = "latitude", lon = "longitude", hover_name="Location", hover_data = ["Adult mortality rate"], color = "Adult mortality rate", size = "Adult mortality rate", size_max = 30, opacity = 0.5, center = {"lat": 0.44, "lon": 157.7}, zoom = 2, height = 800, width = 800)
                    fig.update_layout(mapbox_style = "open-street-map")
                    fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0})
                    fig.update_layout(title_text = "Avrupadaki Yetişkin Ölüm Oranları")
                    st.plotly_chart(fig)

                
            elif select_box == "Erkek":
                createTable("Europe", male)
                if st.button("Avrupa Ülkelerinin Grafiğini Görüntüle (Erkek)"):
                    male_europe = male[male["ParentLocation"] == "Europe"]
                    country_europe_male = male_europe["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_europe_male) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_europe_male:
                        axs[i][j].scatter(data = male_europe[male_europe["Location"] == c], x = "Period", y = "Adult mortality rate", color = "r", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 
            elif select_box == "Dişi":
                createTable("Europe", female)
                if st.button("Avrupa Ülkelerinin Grafiğini Görüntüle (Dişi)"):
                    female_europe = female[female["ParentLocation"] == "Europe"]
                    country_europe_female = female_europe["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_europe_female) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_europe_female:
                        axs[i][j].scatter(data = female_europe[female_europe["Location"] == c], x = "Period", y = "Adult mortality rate", color = "r", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig)
        elif radio == "Batı Pasifik":
            if select_box == "Her iki cins":
                createTable("Western Pacific", both)
                if st.button("Batı Pasifik Ülkelerinin Grafiğini Görüntüle (Her İki Cins)"):
                    both_west = both[both["ParentLocation"] == "Western Pacific"]
                    country_west = both_west["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_west) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_west:
                        axs[i][j].scatter(data = both_west[both_west["Location"] == c], x = "Period", y = "Adult mortality rate", color = "brown", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 

                #Batı Pasifik kıtası üzerinde harita ile grafik oluşturma 
                west_sum = both[both["ParentLocation"] == "Western Pacific"].groupby(["Location"]).sum().reset_index(). sort_values(by = "Adult mortality rate", ascending = False)
                west_sum = west_sum[["Location", "Adult mortality rate"]]
                if st.checkbox("Batı Pasifik Haritası v Ölüm Oranları Grafiği"):
                    geolocator = Nominatim(user_agent="myGeolocator")
                    country_west = west_sum["Location"].unique()
                    for i in country_west:
                        def func(i):
                            return geolocator.geocode(i).latitude
                    west_sum["latitude"] = west_sum["Location"].apply(func)
                    for i in country_west:
                        def func2(i):
                            return geolocator.geocode(i).longitude
                    west_sum["longitude"] = west_sum["Location"].apply(func2)

                    fig = px.scatter_mapbox(west_sum, lat = "latitude", lon = "longitude", hover_name="Location", hover_data = ["Adult mortality rate"], color = "Adult mortality rate", size = "Adult mortality rate", size_max = 30, opacity = 0.5, center = {"lat": 0.44, "lon": 152.7}, zoom = 2, height = 800, width = 1400)
                    fig.update_layout(mapbox_style = "open-street-map")
                    fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0})
                    fig.update_layout(title_text = "Batı Pasifikteki Yetişkin Ölüm Oranları")
                    st.plotly_chart(fig)

            elif select_box == "Erkek":
                createTable("Western Pacific", male)
                if st.button("Batı Pasifik Ülkelerinin Grafiğini Görüntüle (Erkek)"):
                    male_west = male[male["ParentLocation"] == "Western Pacific"]
                    country_west_male = male_west["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_west_male) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_west_male:
                        axs[i][j].scatter(data = male_west[male_west["Location"] == c], x = "Period", y = "Adult mortality rate", color = "brown", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 
            elif select_box == "Dişi":
                createTable("Western Pacific", female)
                if st.button("Batı Pasifik Ülkelerinin Grafiğini Görüntüle (Dişi)"):
                    female_west = female[female["ParentLocation"] == "Western Pacific"]
                    country_west_female = female_west["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_west_female) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_west_female:
                        axs[i][j].scatter(data = female_west[female_west["Location"] == c], x = "Period", y = "Adult mortality rate", color = "brown", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 
        elif radio == "Doğu Akdeniz":
            if select_box == "Her iki cins":
                createTable("Eastern Mediterranean", both)
                if st.button("Doğu Akdeniz Ülkelerinin Grafiğini Görüntüle (Her İki Cins)"):
                    both_east = both[both["ParentLocation"] == "Eastern Mediterranean"]
                    country_east = both_east["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_east) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_east:
                        axs[i][j].scatter(data = both_east[both_east["Location"] == c], x = "Period", y = "Adult mortality rate", color = "green", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 

                #Doğu Akdeniz kıtası üzerinde harita ile grafik oluşturma 
                east_sum = both[both["ParentLocation"] == "Eastern Mediterranean"].groupby(["Location"]).sum().reset_index(). sort_values(by = "Adult mortality rate", ascending = False)
                east_sum = east_sum[["Location", "Adult mortality rate"]]
                if st.checkbox("Doğu Akdeniz Haritası v Ölüm Oranları Grafiği"):
                    geolocator = Nominatim(user_agent="myGeolocator")
                    country_east = east_sum["Location"].unique()
                    for i in country_east:
                        def func(i):
                            return geolocator.geocode(i).latitude
                    east_sum["latitude"] = east_sum["Location"].apply(func)
                    for i in country_east:
                        def func2(i):
                            return geolocator.geocode(i).longitude
                    east_sum["longitude"] = east_sum["Location"].apply(func2)

                    fig = px.scatter_mapbox(east_sum, lat = "latitude", lon = "longitude", hover_name="Location", hover_data = ["Adult mortality rate"], color = "Adult mortality rate", size = "Adult mortality rate", size_max = 30, opacity = 0.5, center = {"lat": 0.44, "lon": 72.7}, zoom = 2, height = 800, width = 1400)
                    fig.update_layout(mapbox_style = "open-street-map")
                    fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0})
                    fig.update_layout(title_text = "Doğu Akdenizdeki Yetişkin Ölüm Oranları")
                    st.plotly_chart(fig)
            elif select_box == "Erkek":
                createTable("Eastern Mediterranean", male)
                if st.button("Doğu Akdeniz Ülkelerinin Grafiğini Görüntüle (Erkek)"):
                    male_east = male[male["ParentLocation"] == "Eastern Mediterranean"]
                    country_east_male = male_east["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_east_male) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_east_male:
                        axs[i][j].scatter(data = male_east[male_east["Location"] == c], x = "Period", y = "Adult mortality rate", color = "green", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 
            elif select_box == "Dişi":
                createTable("Eastern Mediterranean", female)
                if st.button("Doğu Akdeniz Ülkelerinin Grafiğini Görüntüle (Dişi)"):
                    female_east = female[female["ParentLocation"] == "Eastern Mediterranean"]
                    country_east_female = female_east["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_east_female) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 100))
                    for c in country_east_female:
                        axs[i][j].scatter(data = female_east[female_east["Location"] == c], x = "Period", y = "Adult mortality rate", color = "green", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.7)
                    st.pyplot(fig) 
        elif radio == "Güneydoğu Asya":
            if select_box == "Her iki cins":
                createTable("South-East Asia", both)
                if st.button("Güneydoğu Asya Ülkelerinin Grafiğini Görüntüle (Her İki Cins)"):
                    both_south = both[both["ParentLocation"] == "South-East Asia"]
                    country_south = both_south["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_south) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 60))
                    for c in country_south:
                        axs[i][j].scatter(data = both_south[both_south["Location"] == c], x = "Period", y = "Adult mortality rate", color = "purple", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.3)
                    st.pyplot(fig)

                #Güneydoğu Asya kıtası üzerinde harita ile grafik oluşturma 
                south_sum = both[both["ParentLocation"] == "South-East Asia"].groupby(["Location"]).sum().reset_index(). sort_values(by = "Adult mortality rate", ascending = False)
                south_sum = south_sum[["Location", "Adult mortality rate"]]
                if st.checkbox("Güneydoğu Asya Haritası v Ölüm Oranları Grafiği"):
                    geolocator = Nominatim(user_agent="myGeolocator")
                    country_south = south_sum["Location"].unique()
                    for i in country_south:
                        def func(i):
                            return geolocator.geocode(i).latitude
                    south_sum["latitude"] = south_sum["Location"].apply(func)
                    for i in country_south:
                        def func2(i):
                            return geolocator.geocode(i).longitude
                    south_sum["longitude"] = south_sum["Location"].apply(func2)

                    fig = px.scatter_mapbox(south_sum, lat = "latitude", lon = "longitude", hover_name="Location", hover_data = ["Adult mortality rate"], color = "Adult mortality rate", size = "Adult mortality rate", size_max = 30, opacity = 0.5, center = {"lat": 0.44, "lon": 157.7}, zoom = 2, height = 800, width = 1400)
                    fig.update_layout(mapbox_style = "open-street-map")
                    fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0})
                    fig.update_layout(title_text = "Güneydoğu Asyadaki Yetişkin Ölüm Oranları")
                    st.plotly_chart(fig)

            elif select_box == "Erkek":
                createTable("South-East Asia", male)
                if st.button("Güneydoğu Asya Ülkelerinin Grafiğini Görüntüle (Erkek)"):
                    male_south = male[male["ParentLocation"] == "South-East Asia"]
                    country_south_male = male_south["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_south_male) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 60))
                    for c in country_south_male:
                        axs[i][j].scatter(data = male_south[male_south["Location"] == c], x = "Period", y = "Adult mortality rate", color = "purple", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.3)
                    st.pyplot(fig)

            elif select_box == "Dişi":
                createTable("South-East Asia", female)
                if st.button("Güneydoğu Asya Ülkelerinin Grafiğini Görüntüle (Dişi)"):
                    female_south = female[female["ParentLocation"] == "South-East Asia"]
                    country_south_female = female_south["Location"].unique()
                    i, j = 0, 0
                    PLOTS_PER_ROW = 2
                    fig, axs = plt.subplots(math.ceil(len(country_south_female) / PLOTS_PER_ROW), PLOTS_PER_ROW, figsize = (20, 60))
                    for c in country_south_female:
                        axs[i][j].scatter(data = female_south[female_south["Location"] == c], x = "Period", y = "Adult mortality rate", color = "purple", s = 15)
                        axs[i][j].set_ylabel(" ")
                        axs[i][j].set_title(c)
                        j += 1
                        if j%PLOTS_PER_ROW == 0:
                            i+=1
                            j=0
                    fig.subplots_adjust(hspace=0.3)
                    st.pyplot(fig)

        slider = st.slider("Yıl Seçiniz", 2000, 2016)

        if slider == 2000:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2000, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Africa", year = 2000, table = both)
                elif select_box == "Erkek":
                    yearTable(2000, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Africa", year = 2000, table = male)
                elif select_box == "Dişi":
                    yearTable(2000, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Africa", year = 2000, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2000, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Americas", year = 2000, table = both)
                elif select_box == "Erkek":
                    yearTable(2000, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Americas", year = 2000, table = male)
                elif select_box == "Dişi":
                    yearTable(2000, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Americas", year = 2000, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2000, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Europe", year = 2000, table = both)
                elif select_box == "Erkek":
                    yearTable(2000, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Europe", year = 2000, table = male)
                elif select_box == "Dişi":
                    yearTable(2000, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Europe", year = 2000, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2000, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Western Pacific", year = 2000, table = both)
                elif select_box == "Erkek":
                    yearTable(2000, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Western Pacific", year = 2000, table = male)
                elif select_box == "Dişi":
                    yearTable(2000, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Western Pacific", year = 2000, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2000, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Eastern Mediterranean", year = 2000, table = both)
                elif select_box == "Erkek":
                    yearTable(2000, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Eastern Mediterranean", year = 2000, table = male)
                elif select_box == "Dişi":
                    yearTable(2000, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Eastern Mediterranean", year = 2000, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2000, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "South-East Asia", year = 2000, table = both)
                elif select_box == "Erkek":
                    yearTable(2000, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "South-East Asia", year = 2000, table = male)
                elif select_box == "Dişi":
                    yearTable(2000, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "South-East Asia", year = 2000, table = female)
        elif slider == 2001:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2001, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2001, table = both)
                elif select_box == "Erkek":
                    yearTable(2001, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Africa", year = 2001, table = male)
                elif select_box == "Dişi":
                    yearTable(2001, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı"):
                        yearGraph(location = "Africa", year = 2001, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2001, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2001, table = both)
                elif select_box == "Erkek":
                    yearTable(2001, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2001, table = male)
                elif select_box == "Dişi":
                    yearTable(2001, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2001, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2001, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2001, table = both)
                elif select_box == "Erkek":
                    yearTable(2001, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2001, table = male)
                elif select_box == "Dişi":
                    yearTable(2001, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2001, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2001, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2001, table = both)
                elif select_box == "Erkek":
                    yearTable(2001, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2001, table = male)
                elif select_box == "Dişi":
                    yearTable(2001, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2001, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2001, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2001, table = both)
                elif select_box == "Erkek":
                    yearTable(2001, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2001, table = male)
                elif select_box == "Dişi":
                    yearTable(2001, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2001, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2001, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2001, table = both)
                elif select_box == "Erkek":
                    yearTable(2001, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2001, table = male)
                elif select_box == "Dişi":
                    yearTable(2001, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2001, table = female)
        elif slider == 2002:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2002, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2002, table = both)
                elif select_box == "Erkek":
                    yearTable(2002, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2002, table = male)
                elif select_box == "Dişi":
                    yearTable(2002, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2002, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2002, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2002, table = both)
                elif select_box == "Erkek":
                    yearTable(2002, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2002, table = male)
                elif select_box == "Dişi":
                    yearTable(2002, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2002, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2002, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2002, table = both)
                elif select_box == "Erkek":
                    yearTable(2002, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2002, table = male)
                elif select_box == "Dişi":
                    yearTable(2002, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2002, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2002, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2002, table = both)
                elif select_box == "Erkek":
                    yearTable(2002, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2002, table = male)
                elif select_box == "Dişi":
                    yearTable(2002, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2002, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2002, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2002, table = both)
                elif select_box == "Erkek":
                    yearTable(2002, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2002, table = male)
                elif select_box == "Dişi":
                    yearTable(2002, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2002, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2002, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2002, table = both)
                elif select_box == "Erkek":
                    yearTable(2002, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2002, table = male)
                elif select_box == "Dişi":
                    yearTable(2002, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2002, table = female)
        elif slider == 2003:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2003, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2003, table = both)
                elif select_box == "Erkek":
                    yearTable(2003, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2003, table = male)
                elif select_box == "Dişi":
                    yearTable(2003, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2003, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2003, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2003, table = both)
                elif select_box == "Erkek":
                    yearTable(2003, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2003, table = male)
                elif select_box == "Dişi":
                    yearTable(2003, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2003, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2003, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2003, table = both)
                elif select_box == "Erkek":
                    yearTable(2003, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2003, table = male)
                elif select_box == "Dişi":
                    yearTable(2003, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2003, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2003, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2003, table = both)
                elif select_box == "Erkek":
                    yearTable(2003, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2003, table = male)
                elif select_box == "Dişi":
                    yearTable(2003, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2003, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2003, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2003, table = both)
                elif select_box == "Erkek":
                    yearTable(2003, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2003, table = male)
                elif select_box == "Dişi":
                    yearTable(2003, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2003, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2003, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2003, table = both)
                elif select_box == "Erkek":
                    yearTable(2003, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2003, table = male)
                elif select_box == "Dişi":
                    yearTable(2003, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2003, table = female)
        elif slider == 2004:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2004, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2004, table = both)
                elif select_box == "Erkek":
                    yearTable(2004, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2004, table = male)
                elif select_box == "Dişi":
                    yearTable(2004, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2004, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2004, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2004, table = both)
                elif select_box == "Erkek":
                    yearTable(2004, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2004, table = male)
                elif select_box == "Dişi":
                    yearTable(2004, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2004, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2004, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2004, table = bothf)
                elif select_box == "Erkek":
                    yearTable(2004, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2004, table = male)
                elif select_box == "Dişi":
                    yearTable(2004, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2004, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2004, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2004, table = both)
                elif select_box == "Erkek":
                    yearTable(2004, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2004, table = male)
                elif select_box == "Dişi":
                    yearTable(2004, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2004, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2004, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2004, table = both)
                elif select_box == "Erkek":
                    yearTable(2004, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2004, table = male)
                elif select_box == "Dişi":
                    yearTable(2004, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2004, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2004, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2004, table = both)
                elif select_box == "Erkek":
                    yearTable(2004, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2004, table = male)
                elif select_box == "Dişi":
                    yearTable(2004, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2004, table = female)
        elif slider == 2005:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2005, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2005, table = both)
                elif select_box == "Erkek":
                    yearTable(2005, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2005, table = male)
                elif select_box == "Dişi":
                    yearTable(2005, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2005, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2005, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2005, table = both)
                elif select_box == "Erkek":
                    yearTable(2005, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2005, table = male)
                elif select_box == "Dişi":
                    yearTable(2005, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2005, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2005, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2005, table = both)
                elif select_box == "Erkek":
                    yearTable(2005, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2005, table = male)
                elif select_box == "Dişi":
                    yearTable(2005, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2005, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2005, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2005, table = both)
                elif select_box == "Erkek":
                    yearTable(2005, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2005, table = male)
                elif select_box == "Dişi":
                    yearTable(2005, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2005, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2005, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2005, table = both)
                elif select_box == "Erkek":
                    yearTable(2005, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2005, table = male)
                elif select_box == "Dişi":
                    yearTable(2005, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2005, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2005, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2005, table = both)
                elif select_box == "Erkek":
                    yearTable(2005, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2005, table = male)
                elif select_box == "Dişi":
                    yearTable(2005, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2005, table = female)
        elif slider == 2006:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2006, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2006, table = both)
                elif select_box == "Erkek":
                    yearTable(2006, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2006, table = male)
                elif select_box == "Dişi":
                    yearTable(2006, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2006, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2006, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2006, table = both)
                elif select_box == "Erkek":
                    yearTable(2006, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2006, table = male)
                elif select_box == "Dişi":
                    yearTable(2006, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2006, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2006, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2006, table = both)
                elif select_box == "Erkek":
                    yearTable(2006, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2006, table = male)
                elif select_box == "Dişi":
                    yearTable(2006, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2006, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2006, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2006, table = both)
                elif select_box == "Erkek":
                    yearTable(2006, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2006, table = male)
                elif select_box == "Dişi":
                    yearTable(2006, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2006, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2006, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2006, table = both)
                elif select_box == "Erkek":
                    yearTable(2006, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2006, table = male)
                elif select_box == "Dişi":
                    yearTable(2006, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2006, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2006, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2006, table = both)
                elif select_box == "Erkek":
                    yearTable(2006, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2006, table = male)
                elif select_box == "Dişi":
                    yearTable(2006, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2006, table = female)
                    
        elif slider == 2007:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2007, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2007, table = both)
                elif select_box == "Erkek":
                    yearTable(2007, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2007, table = male)
                elif select_box == "Dişi":
                    yearTable(2007, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2007, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2007, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2007, table = both)
                elif select_box == "Erkek":
                    yearTable(2007, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2007, table = male)
                elif select_box == "Dişi":
                    yearTable(2007, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2007, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2007, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2007, table = both)
                elif select_box == "Erkek":
                    yearTable(2007, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2007, table = male)
                elif select_box == "Dişi":
                    yearTable(2007, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2007, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2007, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2007, table = both)
                elif select_box == "Erkek":
                    yearTable(2007, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2007, table = male)
                elif select_box == "Dişi":
                    yearTable(2007, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2007, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2007, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2007, table = both)
                elif select_box == "Erkek":
                    yearTable(2007, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2007, table = male)
                elif select_box == "Dişi":
                    yearTable(2007, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2007, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2007, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2007, table = both)
                elif select_box == "Erkek":
                    yearTable(2007, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2007, table = male)
                elif select_box == "Dişi":
                    yearTable(2007, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2007, table = female)
        elif slider == 2008:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2008, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2008, table = both)
                elif select_box == "Erkek":
                    yearTable(2008, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2008, table = male)
                elif select_box == "Dişi":
                    yearTable(2008, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2008, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2008, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2008, table = both)
                elif select_box == "Erkek":
                    yearTable(2008, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2008, table = male)
                elif select_box == "Dişi":
                    yearTable(2008, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2008, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2008, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2008, table = both)
                elif select_box == "Erkek":
                    yearTable(2008, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2008, table = male)
                elif select_box == "Dişi":
                    yearTable(2008, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2008, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2008, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2008, table = both)
                elif select_box == "Erkek":
                    yearTable(2008, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2008, table = male)
                elif select_box == "Dişi":
                    yearTable(2008, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2008, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2008, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2008, table = both)
                elif select_box == "Erkek":
                    yearTable(2008, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2008, table = male)
                elif select_box == "Dişi":
                    yearTable(2008, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2008, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2008, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2008, table = both)
                elif select_box == "Erkek":
                    yearTable(2008, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2008, table = male)
                elif select_box == "Dişi":
                    yearTable(2008, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2008, table = female)
        elif slider == 2009:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2009, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2009, table = both)
                elif select_box == "Erkek":
                    yearTable(2009, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2009, table = male)
                elif select_box == "Dişi":
                    yearTable(2009, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2009, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2009, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2009, table = both)
                elif select_box == "Erkek":
                    yearTable(2009, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2009, table = male)
                elif select_box == "Dişi":
                    yearTable(2009, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2009, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2009, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2009, table = both)
                elif select_box == "Erkek":
                    yearTable(2009, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2009, table = male)
                elif select_box == "Dişi":
                    yearTable(2009, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2009, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2009, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2009, table = both)
                elif select_box == "Erkek":
                    yearTable(2009, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2009, table = male)
                elif select_box == "Dişi":
                    yearTable(2009, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2009, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2009, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2009, table = both)
                elif select_box == "Erkek":
                    yearTable(2009, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2009, table = male)
                elif select_box == "Dişi":
                    yearTable(2009, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2009, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2009, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2009, table = both)
                elif select_box == "Erkek":
                    yearTable(2009, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2009, table = male)
                elif select_box == "Dişi":
                    yearTable(2009, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2009, table = female)
        elif slider == 2010:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2010, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2010, table = both)
                elif select_box == "Erkek":
                    yearTable(2010, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2010, table = male)
                elif select_box == "Dişi":
                    yearTable(2010, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2010, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2010, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2010, table = both)
                elif select_box == "Erkek":
                    yearTable(2010, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2010, table = male)
                elif select_box == "Dişi":
                    yearTable(2010, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2010, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2010, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2010, table = both)
                elif select_box == "Erkek":
                    yearTable(2010, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2010, table = male)
                elif select_box == "Dişi":
                    yearTable(2010, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2010, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2010, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2010, table = both)
                elif select_box == "Erkek":
                    yearTable(2010, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2010, table = male)
                elif select_box == "Dişi":
                    yearTable(2010, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2010, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2010, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2010, table = both)
                elif select_box == "Erkek":
                    yearTable(2010, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2010, table = male)
                elif select_box == "Dişi":
                    yearTable(2010, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2010, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2010, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2010, table = both)
                elif select_box == "Erkek":
                    yearTable(2010, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2010, table = male)
                elif select_box == "Dişi":
                    yearTable(2010, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2010, table = female)
        elif slider == 2011:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2011, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2011, table = both)
                elif select_box == "Erkek":
                    yearTable(2011, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2011, table = male)
                elif select_box == "Dişi":
                    yearTable(2011, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2011, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2011, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2011, table = both)
                elif select_box == "Erkek":
                    yearTable(2011, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2011, table = male)
                elif select_box == "Dişi":
                    yearTable(2011, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2011, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2011, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2011, table = both)
                elif select_box == "Erkek":
                    yearTable(2011, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2011, table = male)
                elif select_box == "Dişi":
                    yearTable(2011, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2011, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2011, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2011, table = both)
                elif select_box == "Erkek":
                    yearTable(2011, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2011, table = male)
                elif select_box == "Dişi":
                    yearTable(2011, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2011, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2011, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2011, table = both)
                elif select_box == "Erkek":
                    yearTable(2011, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2011, table = male)
                elif select_box == "Dişi":
                    yearTable(2011, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2011, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2011, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2011, table = both)
                elif select_box == "Erkek":
                    yearTable(2011, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2011, table = male)
                elif select_box == "Dişi":
                    yearTable(2011, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2011, table = female)
        elif slider == 2012:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2012, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2012, table = both)
                elif select_box == "Erkek":
                    yearTable(2012, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2012, table = male)
                elif select_box == "Dişi":
                    yearTable(2012, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2012, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2012, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2012, table = both)
                elif select_box == "Erkek":
                    yearTable(2012, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2012, table = male)
                elif select_box == "Dişi":
                    yearTable(2012, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2012, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2012, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2012, table = both)
                elif select_box == "Erkek":
                    yearTable(2012, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2012, table = male)
                elif select_box == "Dişi":
                    yearTable(2012, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2012, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2012, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2012, table = both)
                elif select_box == "Erkek":
                    yearTable(2012, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2012, table = male)
                elif select_box == "Dişi":
                    yearTable(2012, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2012, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2012, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2012, table = both)
                elif select_box == "Erkek":
                    yearTable(2012, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2012, table = male)
                elif select_box == "Dişi":
                    yearTable(2012, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2012, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2012, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2012, table = both)
                elif select_box == "Erkek":
                    yearTable(2012, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2012, table = male)
                elif select_box == "Dişi":
                    yearTable(2012, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2012, table = female)
        elif slider == 2013:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2013, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2013, table = both)
                elif select_box == "Erkek":
                    yearTable(2013, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2013, table = male)
                elif select_box == "Dişi":
                    yearTable(2013, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2013, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2013, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2013, table = both)
                elif select_box == "Erkek":
                    yearTable(2013, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2013, table = male)
                elif select_box == "Dişi":
                    yearTable(2013, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2013, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2013, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2013, table = both)
                elif select_box == "Erkek":
                    yearTable(2013, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2013, table = male)
                elif select_box == "Dişi":
                    yearTable(2013, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2013, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2013, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2013, table = both)
                elif select_box == "Erkek":
                    yearTable(2013, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2013, table = male)
                elif select_box == "Dişi":
                    yearTable(2013, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2013, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2013, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2013, table = both)
                elif select_box == "Erkek":
                    yearTable(2013, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2013, table = male)
                elif select_box == "Dişi":
                    yearTable(2013, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2013, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2013, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2013, table = both)
                elif select_box == "Erkek":
                    yearTable(2013, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2013, table = male)
                elif select_box == "Dişi":
                    yearTable(2013, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2013, table = female)
        elif slider == 2014:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2014, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2014, table = both)
                elif select_box == "Erkek":
                    yearTable(2014, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2014, table = male)
                elif select_box == "Dişi":
                    yearTable(2014, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2014, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2014, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2014, table = both)
                elif select_box == "Erkek":
                    yearTable(2014, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2014, table = male)
                elif select_box == "Dişi":
                    yearTable(2014, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2014, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2014, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2014, table = both)
                elif select_box == "Erkek":
                    yearTable(2014, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2014, table = male)
                elif select_box == "Dişi":
                    yearTable(2014, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2014, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2014, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2014, table = both)
                elif select_box == "Erkek":
                    yearTable(2014, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2014, table = male)
                elif select_box == "Dişi":
                    yearTable(2014, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2014, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2014, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2014, table = both)
                elif select_box == "Erkek":
                    yearTable(2014, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2014, table = male)
                elif select_box == "Dişi":
                    yearTable(2014, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2014, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2014, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2014, table = both)
                elif select_box == "Erkek":
                    yearTable(2014, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2014, table = male)
                elif select_box == "Dişi":
                    yearTable(2014, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2014, table = female)
        elif slider == 2015:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2015, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2015, table = both)
                elif select_box == "Erkek":
                    yearTable(2015, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2015, table = male)
                elif select_box == "Dişi":
                    yearTable(2015, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2015, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2015, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2015, table = both)
                elif select_box == "Erkek":
                    yearTable(2015, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2015, table = male)
                elif select_box == "Dişi":
                    yearTable(2015, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2015, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2015, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2015, table = both)
                elif select_box == "Erkek":
                    yearTable(2015, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2015, table = male)
                elif select_box == "Dişi":
                    yearTable(2015, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2015, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2015, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2015, table = both)
                elif select_box == "Erkek":
                    yearTable(2015, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2015, table = male)
                elif select_box == "Dişi":
                    yearTable(2015, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2015, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2015, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2015, table = both)
                elif select_box == "Erkek":
                    yearTable(2015, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2015, table = male)
                elif select_box == "Dişi":
                    yearTable(2015, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2015, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2015, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2015, table = both)
                elif select_box == "Erkek":
                    yearTable(2015, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2015, table = male)
                elif select_box == "Dişi":
                    yearTable(2015, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2015, table = female)
        elif slider == 2016:
            if radio == "Afrika":
                if select_box == "Her iki cins":
                    yearTable(2016, both, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2016, table = both)
                elif select_box == "Erkek":
                    yearTable(2016, male, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2016, table = male)
                elif select_box == "Dişi":
                    yearTable(2016, female, "Africa")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Africa", year = 2016, table = female)
            elif radio == "Amerika":
                if select_box == "Her iki cins":
                    yearTable(2016, both, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2016, table = both)
                elif select_box == "Erkek":
                    yearTable(2016, male, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2016, table = male)
                elif select_box == "Dişi":
                    yearTable(2016, female, "Americas")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Americas", year = 2016, table = female)
            elif radio == "Avrupa":
                if select_box == "Her iki cins":
                    yearTable(2016, both, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2016, table = both)
                elif select_box == "Erkek":
                    yearTable(2016, male, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2016, table = male)
                elif select_box == "Dişi":
                    yearTable(2016, female, "Europe")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Europe", year = 2016, table = female)
            elif radio == "Batı Pasifik":
                if select_box == "Her iki cins":
                    yearTable(2016, both, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2016, table = both)
                elif select_box == "Erkek":
                    yearTable(2016, male, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2016, table = male)
                elif select_box == "Dişi":
                    yearTable(2016, female, "Western Pacific")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Western Pacific", year = 2016, table = female)
            elif radio == "Doğu Akdeniz":
                if select_box == "Her iki cins":
                    yearTable(2016, both, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2016, table = both)
                elif select_box == "Erkek":
                    yearTable(2016, male, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2016, table = male)
                elif select_box == "Dişi":
                    yearTable(2016, female, "Eastern Mediterranean")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "Eastern Mediterranean", year = 2016, table = female)
            elif radio == "Güneydoğu Asya":
                if select_box == "Her iki cins":
                    yearTable(2016, both, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2016, table = both)
                elif select_box == "Erkek":
                    yearTable(2016, male, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2016, table = male)
                elif select_box == "Dişi":
                    yearTable(2016, female, "South-East Asia")
                    if st.button("Yıla göre ortalama ölüm oranı "):
                        yearGraph(location = "South-East Asia", year = 2016, table = female)

    elif sidebar == "Kadın-Erkek Karşılaştırma":
        df_concat = pd.concat([female, male])

        st.write(df_concat[["ParentLocation", "Location", "Period", "Sex", "Adult mortality rate"]].sort_values(by="Adult mortality rate", ascending= False))

        st.subheader("Hala Üzerinde Çalışılmaktadır. Teşekkürler c: ")
        st.balloons()

    




if __name__ == "__main__":
    main()
