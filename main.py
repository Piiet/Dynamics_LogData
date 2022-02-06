from queue import Empty
import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
import re
import statistics


image = Image.open('DynamicsLogo.png')

st.set_page_config(layout="wide", page_title="AGX LOG DATA", page_icon=image)

folder_path = ""

#set page columns
col1, col2, col3= st.columns([1.2, 2, 2])
Runtime = [] #store runtime data in ms

st.sidebar.warning('please enter "plog" filepath')
sidebar_folder_path = st.sidebar.text_input('Folderpath: ...\plog')


if bool(sidebar_folder_path):
    

#1. ASM folder path 2.autocross folder path. Wenn mehr missionen -> autocross variable machen
 with col1:
    st.header("AGX Log Data")
    st.image(image, width=100)

    options_folder = st.selectbox('Folder: ', ('ASM', 'CAM FUSION', 'CAN INTERFACE', 'LCD', 'PATHPLANNING',
                                               'RACELINE OPTIMIZATION', 'SLAM', 'STANLEY', 'WATCHDOG'))

    #Select Folder 
    if options_folder == "ASM":
        arr_dir = os.listdir(
            sidebar_folder_path + "\\ASM")
    else:
        #Autocross is parentfolder
        arr_dir = os.listdir(
            sidebar_folder_path +  "\\autocross\\" + options_folder)

    #select log file
    options_file = st.selectbox('Log File: ', arr_dir) 
    st.write("Selected: " + options_file)


    #button for INFO / FATAL selection
    message_type = st.radio(
        "Filter Message Type: ",
        ('ALL', 'FATAL')
    )






#Show Log Data Text Coloumn
 with col3:

    lines = [] #for later interation

    if options_folder == "ASM":
        with st.container():
          with open(
             sidebar_folder_path 
            + "\\" + options_folder + "\\" + options_file) as log_file:

             #print log file lines
             for line in log_file:

                # check radio button state
                if message_type == "FATAL":
                    if "FATAL" in line:
                        st.write(line)
                else: 
                        st.write(line)
             
            
             
    else:
        message_count = 0
        with open(
            sidebar_folder_path + "\\autocross\\"
                + options_folder + "\\" + options_file) as log_file:
            for line in log_file:

                message_count += 1
                   
             
             #check radio button state
                if message_type == "FATAL":
                    if "FATAL" in line:
                        m = re.search('Runtime of (.+?)ms', line)
                        if m:
                            found = m.group(1)
                            found = float(found)
                            Runtime.append(found)
                        st.write(line)
                else:
                        #different ms description in differenct log file types SLAM, LCD etc...
                        m = re.search('Runtime of (.+?)ms', line)
                        c = re.search('classification of (.+?)ms', line)
                        s = re.search('Lidar measurement of (.+?)ms', line)
                        if m:
                            found = m.group(1)
                            found = float(found)
                            Runtime.append(found)
                        if c:
                            found = c.group(1)
                            found = float(found)
                            Runtime.append(found)
                        if s:
                            found = s.group(1)
                            found = float(found)
                            Runtime.append(found)

                        st.write(line)

        
#Plot column
 with col2:

    #check if Runtime is empty -> a file without ms statement was selected
    if bool(Runtime):

        #Delete Array Values from 0 to number_input 
        number_input = int(st.number_input('Delete Array Values'))
        for i in range(0,number_input):
         del Runtime[i]

        #print Max ms and Min ms with median
        col1.metric("Max ms: ", value=max(Runtime),
                delta=statistics.median(Runtime), delta_color="inverse")
        col1.metric("Min ms: ", value=min(Runtime), delta=-
                statistics.median(Runtime), delta_color="inverse")


        #Fill panda Dataframe with Runtime array
        df = pd.DataFrame(
        np.array(Runtime,
                 dtype=[("frequenzy", "d")])
        )

        #plot line chart and dataframe
        col2.line_chart(df)
        st.dataframe(df)
    else:
        st.info('No ms data found in log file')

        

