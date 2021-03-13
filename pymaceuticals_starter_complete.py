#!/usr/bin/env python
# coding: utf-8

# ## Observations and Insights 

# 

# In[104]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import re
from scipy import stats
# Study data files
mouse_metadata_path = "data/Mouse_metadata.csv"
study_results_path = "data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single dataset
Complete_Mouse_Data = pd.merge(mouse_metadata,study_results,on="Mouse ID",how = "outer")
# Display the data table for preview
Complete_Mouse_Data
#study_results.head()


# In[24]:


# Checking the number of mice.
No_Mice=len (Complete_Mouse_Data.groupby(["Mouse ID"]).count())
No_Mice


# In[25]:


# Getting the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
DUP = Complete_Mouse_Data.duplicated(subset=["Mouse ID","Timepoint"])
Complete_Mouse_Data["DUP"] =DUP
DUP2 = Complete_Mouse_Data.groupby(["DUP","Mouse ID"]).count()
DUP2
#g989 is duplicate mouse!!


# In[26]:


# Optional: Get all the data for the duplicate mouse ID. 
g989 = Complete_Mouse_Data.loc[Complete_Mouse_Data["Mouse ID"]=="g989"]


# In[27]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.
Complete_Mouse_Data_Clean = Complete_Mouse_Data.drop_duplicates(subset=["Mouse ID","Timepoint"])
Complete_Mouse_Data_Clean

#Complete_Mouse_Data_Clean.loc[Complete_Mouse_Data_Clean["Mouse ID"]=="g989"]


# In[28]:


# Checking the number of mice in the clean DataFrame.

No_Mice=len (Complete_Mouse_Data_Clean.groupby(["Mouse ID"]).count())
No_Mice


# ## Summary Statistics

# In[29]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen
REGIMEN_GROUP = pd.DataFrame({"Regimen":Complete_Mouse_Data_Clean["Drug Regimen"],
                            "Tumor Volume (mm3)":Complete_Mouse_Data_Clean["Tumor Volume (mm3)"]})
DRUGS = REGIMEN_GROUP["Regimen"].unique()
#_Mean

DRUGS 


# This method is the most straighforward, creating multiple series and putting them all together at the end.

REGIMEN_GROUP.head()


# In[30]:


Mean = REGIMEN_GROUP.groupby(["Regimen"]).mean()
Ave = Mean["Tumor Volume (mm3)"]

Median = REGIMEN_GROUP.groupby(["Regimen"]).median()
MED = Median["Tumor Volume (mm3)"]

Variance = REGIMEN_GROUP.groupby(["Regimen"]).var()
VAR = Variance["Tumor Volume (mm3)"]

Standard_Deviation = REGIMEN_GROUP.groupby(["Regimen"]).std()
SD = Standard_Deviation["Tumor Volume (mm3)"]

SEM = REGIMEN_GROUP.groupby(["Regimen"]).sem()
StErr = SEM ["Tumor Volume (mm3)"]
SUMM_ST = pd.DataFrame({
                       "MEAN Tumor Volume (mm3)" :Ave,
                       "Median Tumor Volume (mm3)":MED,
                       "Variance":VAR ,
                       "Standard_Deviation Tumor Volume (mm3)":SD ,
                       "SEM":StErr})
SUMM_ST
#M
#Standard_Deviation


# In[31]:


MEAN_2 = []
#NAME = []
#MEDIAN = 0
#Variance = 0
#sd = 0
#m=int
#MEAN = 
for DRUG in DRUGS:
     m=((REGIMEN_GROUP.loc[REGIMEN_GROUP["Regimen"]==DRUG]).mean())
     DF = m.to_frame()
     DF.rename(columns={0:"average"})
     #MEAN_2.append(DF["average"])
    #MEAN.append()
   # for DRUG in REGIMEN_GROUP["Regimen"]:
        #MEAN.append(REGIMEN_GROUP["Regimen"].mean)
    

type(DF)
#MEAN
#NAME
#MEAN
DF
#SUMM_ST = pd.DataFrame({"Regimen":DRUGS,
                     #  "MEAN" :MEAN})
#SUMM_ST


# In[32]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen

# This method produces everything in a single groupby function


# ## Bar and Pie Charts

# In[33]:


# Generate a bar plot showing the total number of mice for each treatment throughout the course of the study using pandas. 
Complete_Mouse_Data_Clean.head()

MIceBYTreatment = Complete_Mouse_Data_Clean.groupby(["Drug Regimen"]).count()
MIceBYTreatment2 = pd.DataFrame({"Regimen":DRUGS,
    "Mouse Count":MIceBYTreatment["Mouse ID"]})

MICE_BAR = MIceBYTreatment2.plot(kind = "bar", title = "Number of Mice on Drugs")
MICE_BAR.set_ylabel("Mouse Count")
#MIceBYTreatment2.plot.bar( rot = 0)
#MIceBYTreatment2.plot(figsize=(200,200))


# In[34]:


# Generate a bar plot showing the total number of mice for each treatment throughout the course of the study using pyplot.
X_Axis = MIceBYTreatment2["Regimen"]
Y_Axis = MIceBYTreatment2["Mouse Count"]
plt.bar(X_Axis,Y_Axis,color = 'r')
plt.xticks(rotation ="vertical")
plt.xlabel("Regimen")
plt.ylabel("Number of Mice")
plt.title("Number of Mice vs Regimen")


# In[35]:


# Generate a pie plot showing the distribution of female versus male mice using pandas

Complete_Mouse_Data_Clean.head()




# In[ ]:





# In[36]:


Complete_Mouse_Data_Clean.head()
SEX = ["Male", "Female"]
Femmice = len(Complete_Mouse_Data_Clean.loc[Complete_Mouse_Data_Clean["Sex"]=="Female"])
Femmice

Mamice = len(Complete_Mouse_Data_Clean.loc[Complete_Mouse_Data_Clean["Sex"]=="Male"])
Mamice
#MIceBYGender = Complete_Mouse_Data_Clean.groupby(["Mouse ID","Sex"]).mean()
#MIceBYTreatment2 = pd.DataFrame({"Regimen":DRUGS,
   # "Mouse Count":MIceBYTreatment["Mouse ID"]})
#MIceBYGender

TotMice = Femmice + Mamice
percent_Male = (Mamice/TotMice)*100
percent_feMale = (Femmice/TotMice)*100
pecent = [percent_Male,percent_feMale]

Gendered_Data = pd.DataFrame({"SEX": SEX,
                             "% Mice":pecent})

Gendered_Data2 = Gendered_Data.set_index("SEX")


# In[37]:


Gendered_Data2


# In[38]:


PIE = Gendered_Data2.plot.pie(y="% Mice")


# In[39]:


# Generate a pie plot showing the distribution of female versus male mice using pyplot
LA = 'Male', 'Female'
size = Gendered_Data2["% Mice"]
fig1, ax1 = plt.subplots()

ax1.pie(size,labels = LA, autopct = '%1.1f%%')
plt.title("Male vs Female mice in study")
ax1.axis('equal')
plt.show()


#plt.pie(Gendered_Data2["% Mice"],labels = LA)
#plt.title("Male vs Female Mice")
#


# In[40]:


Mean = REGIMEN_GROUP.groupby(["Regimen"]).mean()
Ave = Mean["Tumor Volume (mm3)"]

Median = REGIMEN_GROUP.groupby(["Regimen"]).median()
MED = Median["Tumor Volume (mm3)"]

Variance = REGIMEN_GROUP.groupby(["Regimen"]).var()
VAR = Variance["Tumor Volume (mm3)"]

Standard_Deviation = REGIMEN_GROUP.groupby(["Regimen"]).std()
SD = Standard_Deviation["Tumor Volume (mm3)"]

SEM = REGIMEN_GROUP.groupby(["Regimen"]).sem()
StErr = SEM ["Tumor Volume (mm3)"]
SUMM_ST = pd.DataFrame({
                       "MEAN Tumor Volume (mm3)" :Ave,
                       "Median Tumor Volume (mm3)":MED,
                       "Variance":VAR ,
                       "Standard_Deviation Tumor Volume (mm3)":SD ,
                       "SEM":StErr})
SUMM_ST
#M
#Standard_Deviation


# In[41]:


Complete_Mouse_Data_Clean


# ## Quartiles, Outliers and Boxplots

# In[42]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:

#Regimens  = "Capomulin", "Ramicane", "Infubinol", "Ceftamin"


#for Regimen in Regimens:
    
    #if Complete_Mouse_Data_Clean["Drug Regimen"] == Regimen
Tumor_Vol = Complete_Mouse_Data_Clean.groupby(["Drug Regimen","Mouse ID"]).min()
Tumor_Vol_Fin =  Tumor_Vol["Tumor Volume (mm3)"]

Tumor_Vol2 = Complete_Mouse_Data_Clean.groupby(["Drug Regimen","Mouse ID"]).max()
Time_point_Fin =Tumor_Vol2["Timepoint"]

Time_point_Fin

Mouse_Drug_Tumour = pd.DataFrame({"Final Time":Time_point_Fin,
                                 "Final Tumor Size":Tumor_Vol_Fin})
Mouse_Drug_Tumour
# Capomulin, Ramicane, Infubinol, and Ceftamin
DFCapomulin = Mouse_Drug_Tumour.loc[Mouse_Drug_Tumour["Drug Regimen"]=="Capomulin"]


# Start by getting the last (greatest) timepoint for each mouse


# Merge this group df with the original dataframe to get the tumor volume at the last timepoint


# In[43]:


#DFCapomulin data, will merge 4 df for comp ask for 4 regimes...
DFCapomulin = Complete_Mouse_Data_Clean.loc[Complete_Mouse_Data_Clean["Drug Regimen"]=="Capomulin"]
DFCapomulin
CapomulinTumor_Vol2= DFCapomulin.groupby(["Drug Regimen","Mouse ID"]).min()
CapomulinTumor_Vol_Fin2 =  CapomulinTumor_Vol2["Tumor Volume (mm3)"]

CapomulinTumor_Vol3 = DFCapomulin.groupby(["Drug Regimen","Mouse ID"]).max()
CapomulinTime_point_Fin3 =CapomulinTumor_Vol3["Timepoint"]

CapomulinTime_point_Fin3

Mouse_Drug_Capomulin = pd.DataFrame({"Final Time":CapomulinTime_point_Fin3,
                                 "Final Tumor Size":CapomulinTumor_Vol_Fin2})



# Capomulin, Ramicane, Infubinol, and Ceftamin
#DFCapomulin = Mouse_Drug_Tumour.loc[Mouse_Drug_Tumour["Drug Regimen"]=="Capomulin"]


# In[44]:


DFRamicane = Complete_Mouse_Data_Clean.loc[Complete_Mouse_Data_Clean["Drug Regimen"]=="Ramicane"]
DFRamicane
RamicaneTumor_Vol2= DFRamicane.groupby(["Drug Regimen","Mouse ID"]).min()
RamicaneTumor_Vol_Fin2 =  RamicaneTumor_Vol2["Tumor Volume (mm3)"]

RamicaneTumor_Vol3 = DFRamicane.groupby(["Drug Regimen","Mouse ID"]).max()
RamicaneTime_point_Fin3 =RamicaneTumor_Vol3["Timepoint"]



Mouse_Drug_Ramicane = pd.DataFrame({"Final Time":RamicaneTime_point_Fin3,
                                 "Final Tumor Size":RamicaneTumor_Vol_Fin2})

# Capomulin, Ramicane, Infubinol, and Ceftamin


# In[45]:


DFInfubinol = Complete_Mouse_Data_Clean.loc[Complete_Mouse_Data_Clean["Drug Regimen"]=="Infubinol"]
DFInfubinol
InfubinolTumor_Vol2= DFInfubinol.groupby(["Drug Regimen","Mouse ID"]).min()
InfubinolTumor_Vol_Fin2 =  InfubinolTumor_Vol2["Tumor Volume (mm3)"]

InfubinolTumor_Vol3 = DFInfubinol.groupby(["Drug Regimen","Mouse ID"]).max()
InfubinolTime_point_Fin3 =InfubinolTumor_Vol3["Timepoint"]



Mouse_Drug_Infubinol = pd.DataFrame({"Final Time":InfubinolTime_point_Fin3,
                                 "Final Tumor Size":InfubinolTumor_Vol_Fin2})
#Mouse_Drug_Infubinol Mouse_Drug_Ramicane Mouse_Drug_Capomulin
# Capomulin, Ramicane, Infubinol, and Ceftamin


# In[ ]:





# In[46]:


#Ceftamin
DFCeftamin = Complete_Mouse_Data_Clean.loc[Complete_Mouse_Data_Clean["Drug Regimen"]=="Ceftamin"]
DFCeftamin
CeftaminTumor_Vol2= DFCeftamin.groupby(["Drug Regimen","Mouse ID"]).min()
CeftaminTumor_Vol_Fin2 =  CeftaminTumor_Vol2["Tumor Volume (mm3)"]

CeftaminTumor_Vol3 = DFCeftamin.groupby(["Drug Regimen","Mouse ID"]).max()
CeftaminTime_point_Fin3 =CeftaminTumor_Vol3["Timepoint"]

CeftaminTime_point_Fin3

Mouse_Drug_Ceftamin = pd.DataFrame({"Final Time":CeftaminTime_point_Fin3,
                                 "Final Tumor Size":CeftaminTumor_Vol_Fin2})
#Mouse_Drug_Infubinol Mouse_Drug_Ramicane Mouse_Drug_Capomulin Mouse_Drug_Ceftamin


# In[ ]:





# In[47]:


#Mouse_Drug_Infubinol Mouse_Drug_Ramicane Mouse_Drug_Capomulin Mouse_Drug_Ceftamin

frames = [Mouse_Drug_Infubinol, Mouse_Drug_Ramicane, Mouse_Drug_Capomulin, Mouse_Drug_Ceftamin]

Merged = pd.concat(frames)
Merged


# In[48]:


# Put treatments into a list for for loop (and later for plot labels)

#,0.5,
# Create empty list to fill with tumor vol data (for plotting)
#Mouse_Drug_Infubinol Mouse_Drug_Ramicane Mouse_Drug_Capomulin Mouse_Drug_Ceftamin


Mouse_Drug_RamicaneUpperQ = (Mouse_Drug_Ramicane["Final Tumor Size"].quantile([0.75]))
Mouse_Drug_RamicaneUpperQ
Mouse_Drug_RamicaneLowerQ = (Mouse_Drug_Infubinol["Final Tumor Size"].quantile([0.25]))
Mouse_Drug_RamicaneLowerQ

Mouse_Drug_RamicaneIQR = Mouse_Drug_RamicaneUpperQ - Mouse_Drug_RamicaneUpperQ
Mouse_Drug_RamicaneUpper_bound = UpperQ + (1.5*IQR)
Mouse_Drug_RamicaneLower_bound = LowerQ - (1.5*IQR)
#Mouse_Drug_InfubinolLower_bound

# Calculate the IQR and quantitatively determine if there are any potential outliers. 
#Mouse_Drug_Infubinol_SummData = pd.DataFrame({"UpperQ":Mouse_Drug_InfubinolUpperQ,
                                             #"LowerQ":Mouse_Drug_InfubinolLowerQ,
                                             #"IQR":Mouse_Drug_InfubinolIQR,
                                            # "Upper_bound":Mouse_Drug_InfubinolUpper_bound,
                                            #"Lower_bound":Mouse_Drug_InfubinolLower_bound})
#Mouse_Drug_Infubinol_SummData    
    # Locate the rows which contain mice on each drug and get the tumor volumes
    
    
    # add subset 
    
    
    # Determine outliers using upper and lower bounds
Mouse_Drug_RamicaneLower_bound


# In[49]:


#Mouse_Drug_Infubinol Mouse_Drug_Ramicane Mouse_Drug_Capomulin Mouse_Drug_Ceftamin
(Mouse_Drug_Infubinol.boxplot(column =["Final Tumor Size"]))


# In[50]:


(Mouse_Drug_Ramicane.boxplot(column =["Final Tumor Size"]))


# In[51]:


(Mouse_Drug_Capomulin.boxplot(column =["Final Tumor Size"]))


# In[52]:


(Mouse_Drug_Ceftamin.boxplot(column =["Final Tumor Size"]))


# In[53]:


# Generate a box plot of the final tumor volume of each mouse across four regimens of interest


# ## Line and Scatter Plots

# In[54]:


# Generate a line plot of time point versus tumor volume for a mouse treated with Capomulin

DFCapomulin.head()

s185 = DFCapomulin.loc[DFCapomulin["Mouse ID"]=="s185"]
s185


# In[55]:


X=s185["Timepoint"]
Y=s185["Tumor Volume (mm3)"]

plt.plot(X,Y,color = "Purple")
plt.xlabel("Timepoint")
plt.ylabel("Tumor Volume (mm3)")
plt.title("Capomulin Time vs Tumour Size for mouse s185")


# In[102]:


# Generate a scatter plot of mouse weight versus average tumor volume for the Capomulin regimen
WEIGHTS=DFCapomulin.groupby(["Weight (g)"]).sum()
Total_Volume = WEIGHTS["Tumor Volume (mm3)"]

Number = DFCapomulin.groupby(["Weight (g)"]).count()
Total_Count = Number["Mouse ID"]

Weight = WEIGHTS=DFCapomulin.groupby(["Weight (g)"]).nunique()
Weight
Mean_Volume =pd.DataFrame({"Average Tumour":(Total_Volume/Total_Count)})
Mean_Volume["Weight"] = (15,17,19,20,21,22,23,24,25)
Mean_Volume


# In[103]:


xs = Mean_Volume["Weight"]
ys = Mean_Volume["Average Tumour"]


plt.scatter(xs,ys,marker = "o",color = "red")
plt.xlabel("Weight (g)")
plt.ylabel("Tumor Volume (mm3)")
plt.title("Weight vs Tumour Size")


# ## Correlation and Regression

# In[108]:


# Calculate the correlation coefficient and linear regression model 
# for mouse weight and average tumor volume for the Capomulin regimen
slope, intercept, r_value, p_value, std_err = stats.linregress(xs,ys)
regress_values = xs*slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
plt.scatter(xs,ys,marker = "o",color = "red")
plt.plot(xs,regress_values, color = "blue")
plt.annotate(line_eq,(24,44),fontsize = 12,color = "blue")
plt.xlabel("Weight (g)")
plt.ylabel("Tumor Volume (mm3)")
plt.title("Weight vs Tumour Size")
plt.show()


# In[ ]:




