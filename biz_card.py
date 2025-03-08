import easyocr
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import sqlite3

def image_to_text(path):

  input_img=Image.open(path)

  #converting image to array format
  image_array=np.array(input_img)
  reader=easyocr.Reader(['en'])
  text=reader.readtext(image_array, detail=0)

  return text, input_img

 #from typing import Concatenate
def extracted_text(texts):
  extracted_dic={"NAME":[],"DESIGNATION":[], "COMPANY_NAME":[], "CONTACT_NO":[], "MAIL_ID":[], "WEBSITE":[], "ADDRESS":[], "PINCODE":[]}

  extracted_dic["NAME"].append(texts[0])
  extracted_dic["DESIGNATION"].append(texts[1])

  for i in range(2,len(texts)):
    if texts[i]. startswith("+")or(texts[i].replace("-","").isdigit() and '-' in texts[i]):
      extracted_dic["CONTACT_NO"].append(texts[i])

    elif "@" in texts[i] and ".com" in texts[i]:
      extracted_dic["MAIL_ID"].append(texts[i])
    elif "WWW" in texts[i] or "www" in texts[i] or "Www" in texts[i] or "wWw" in texts[i] or "wwW" in texts[i]:
      small=texts[i].lower()
      extracted_dic["WEBSITE"].append(small)
    elif "TamilNadu" in texts[i] or  "Tamil Nadu" in texts[i] or texts[i].isdigit():
      extracted_dic["PINCODE"].append(texts[i])

    elif re.match(r'^[A-Za-z]',texts[i]):
      extracted_dic["COMPANY_NAME"].append(texts[i])

    else:
      remove_colon=re.sub(r'[,;]','',texts[i])
      extracted_dic["ADDRESS"].append(remove_colon)

  for key,value in extracted_dic.items():
    if len(value)>0:
      Concatenate = " ".join(value)
      extracted_dic[key]=[Concatenate]
    else:
      value="NA"
      extracted_dic[key]=[value]

  return extracted_dic


#streamlit part
st.set_page_config(layout="wide")
st.title("EXTRACTING BUSINESS CARD WITH 'OCR'")

with st.sidebar:
  select=option_menu("Main Menu", ["Home","Upload & Modyfying","Delete"])

text_dict=None
designation_select=None
names_select=None

if select=="Home":
  pass

elif select=="Upload & Modyfying":
  img=st.file_uploader("Upload the image", type=["png","jpeg","jpg"])

  if img is not None:
    st.image(img, width=300)

    text_image, input_img=image_to_text(img)

    text_dict = extracted_text(text_image)

  if text_dict:
    st.success("TEXT IS EXTRACTED SUCCESSFULLY")
  df=pd.DataFrame(text_dict)

#converting image to bytes
  if img is not None:
    Image_bytes=io.BytesIO()
    input_img.save(Image_bytes, format="PNG")
    image_data=Image_bytes.getvalue()

  #Creating Dictionary
    data={"IMAGE":[image_data]}
    df_1=pd.DataFrame(data)
    concat_df=pd.concat([df,df_1],axis=1)
    st.dataframe(concat_df)

  button_1=st.button("Save", use_container_width=True)
  if button_1:
    mydb=sqlite3.connect("bizxardx.db")
    cursor=mydb.cursor()
    #Table Creation
    create_table_query='''CREATE TABLE IF NOT EXISTS bizcard_details(name varchar(225),
                                                                      designation varchar(225),
                                                                      company_name varchar(225),
                                                                      contact_no varchar(225),
                                                                      mail_id varchar(225),
                                                                      website text,
                                                                      address varchar(225),
                                                                      pincode varchar(225),
                                                                      image text)'''

    cursor.execute(create_table_query)
    mydb.commit()

    #Insert Query
    insert_query='''INSERT INTO bizcard_details(name, designation, company_name, contact_no, mail_id, website, address, pincode, image)
                                                  values(?,?,?,?,?,?,?,?,?)'''
    datas=concat_df.values.tolist()[0]
    cursor.execute(insert_query, datas)
    mydb.commit()
    st.success("SAVED SUCCESSFULLY")

  method=st.radio("Select the Method",["None","Preview","Modify"])
  if method=="None":
    st.write("")
  if method=="Preview":
    mydb=sqlite3.connect("bizxardx.db")
    cursor=mydb.cursor()
    #Select Query
    select_query="SELECT * FROM bizcard_details"
    cursor.execute(select_query)
    table=cursor.fetchall()
    mydb.commit()
    table_df=pd.DataFrame(table, columns=("NAME","DESIGNATION","COMANY_NAME","CONTACT_NO","MAIL_ID","WEBSITE", "ADDRESS","PINCODE","IMAGE"))
    st.dataframe(table_df)

  elif method=="Modify":
    mydb=sqlite3.connect("bizxardx.db")
    cursor=mydb.cursor()
    #Select Query
    select_query="SELECT * FROM bizcard_details"
    cursor.execute(select_query)
    table=cursor.fetchall()
    mydb.commit()
    table_df=pd.DataFrame(table, columns=("NAME","DESIGNATION","COMANY_NAME","CONTACT_NO","MAIL_ID","WEBSITE", "ADDRESS","PINCODE","IMAGE"))
    col1,col2=st.columns(2)
    with col1:
      selected_name=st.selectbox("Select the Name", table_df["NAME"])

    df_3=table_df[table_df["NAME"]==selected_name]
    st.dataframe(df_3)
    df_4=df_3.copy()

    col1,col2=st.columns(2)
    with col1:
      mod_name=st.text_input("Name", df_3["NAME"].unique()[0])
      mod_desig=st.text_input("Designation", df_3["DESIGNATION"].unique()[0])
      mod_comp=st.text_input("Company_name", df_3["COMANY_NAME"].unique()[0])
      mod_cont=st.text_input("Contact_no", df_3["CONTACT_NO"].unique()[0])
      mod_mail=st.text_input("Mail_ID", df_3["MAIL_ID"].unique()[0])

      df_4["NAME"]=mod_name
      df_4["NAME"]=mod_name
      df_4["NAME"]=mod_name
      df_4["NAME"]=mod_name
      df_4["NAME"]=mod_name

    with col2:
      mod_webs=st.text_input("Website", df_3["WEBSITE"].unique()[0])
      mod_addr=st.text_input("Address", df_3["ADDRESS"].unique()[0])
      mod_pin=st.text_input("Pincode", df_3["PINCODE"].unique()[0])
      mod_img=st.text_input("Image", df_3["IMAGE"].unique()[0])

      df_4["WEBSITE"]=mod_webs
      df_4["ADDRESS"]=mod_addr
      df_4["PINCODE"]=mod_pin
      df_4["IMAGE"]=mod_img

    st.dataframe(df_4)
    col1,col2=st.columns(2)

    with col1:
      button_3=st.button("Modify", use_container_width=True)

    if button_3:
      mydb=sqlite3.connect("bizxardx.db")
      cursor=mydb.cursor()

      cursor.execute(f"DELETE FROM bizcard_details WHERE NAME = '{selected_name}'")
      mydb.commit()

      #Insert Query
      insert_query='''INSERT INTO bizcard_details(name, designation, company_name, contact_no, mail_id, website, address, pincode, image)
                                                    values(?,?,?,?,?,?,?,?,?)'''
      datas=concat_df.values.tolist()[0]
      cursor.execute(insert_query, datas)
      mydb.commit()
      st.success("MODIFIED SUCCESSFULLY")


elif select=="Delete":
  mydb=sqlite3.connect("bizxardx.db")
  cursor=mydb.cursor()
  col1,col2=st.columns(2)

  with col1:
    select_query="SELECT NAME FROM bizcard_details"
    cursor.execute(select_query)
    table1=cursor.fetchall()
    mydb.commit()
    names=[]
    for i in table1:
      names.append(i[0])

      names_select=st.selectbox("Select the Name", names)

  with col2:
    select_query=f"SELECT DESIGNATION FROM bizcard_details WHERE NAME ='{names_select}'"
    cursor.execute(select_query)
    table2=cursor.fetchall()
    mydb.commit()
    designation=[]
    for a in table2:
      designation.append(a[0])

      designation_select=st.selectbox("Select the Designation", options=designation)

if names_select and designation_select:
  col1,col2,col3=st.columns(3)

  with col1:
    st.write(f"Selected Name : {names_select}")
    st.write("")
    st.write("")
    st.write("")
    st.write(f"SELECTED DESIGNATION : {designation_select}")

  with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    remove=st.button("DELETE", use_container_width=True)

    if remove:
      cursor.execute(f"DELETE FROM bizcard_details WHERE NAME ='{names_select}' AND DESIGNATION = '{designation_select}'")
      mydb.commit()

      st.warning("DELETED")
