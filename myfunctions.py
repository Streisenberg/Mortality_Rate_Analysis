import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import sys  
import os 

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
