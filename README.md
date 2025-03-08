# BizCardX-Extracting-Business-Card-Data-with-OCR


BizCardX: Extracting Business Card Data with OCR :

The "BizCard" project aims to simplify the process of extracting and managing information from business cards. With this application, users can upload an image of a business card, extract relevant details using Optical Character Recognition (OCR), and display the extracted data. Additionally, users have the option to store the extracted information in a MySQL database for easy access and management. The project utilizes various libraries such as pandas, numpy, streamlit, easyocr, PIL, cv2, and re to achieve its functionalities.

1 extract data from business card image and text image. 2 Analyse extracted data. 3 Store in the database.

Libraries/Modules used for the project :

Pandas - (To Create a DataFrame with the scraped data) mysql.connector - (To store and retrieve the data) Streamlit - (To Create Graphical user Interface) EasyOCR - (To extract text from images)

Workflow :

Imported the necessary libraries for the project, including pandas, streamlit, easyocr, PIL, base64, cv2, and re.

Set up the required configurations and established a connection with the MySQL database.

Created a dictionary to store the extracted data, including fields such as name, designation, mobile number, company name, email ID, website, area, city, state, Pincode, and image.

Developed the user interface using Streamlit. Created different pages for the application: "HOME," "DISPLAY," and "MODIFY."

In the "HOME" page, displays a welcome message and provides instructions for the user to upload an image of a business card using the sidebar.

In the "DISPLAY" page, check if an image has been uploaded. The image is preprocessed using OpenCV and used OCR to extract the text. Extracted specific information from the OCR results, such as name, designation, mobile number, email ID, website, area, city, state, and pincode.

Extracted information was stored in the dictionary created earlier.

Created a DataFrame using pandas to organize the extracted data.

Displays the extracted data in an interactive table using the AgGrid library, which allows the users to view and modify the information if needed.

Provided a button labeled "UPLOAD TO DB" to allow users to upload the extracted data to the MySQL database.

In the "MODIFY" page, users were given the option to update or delete information from the database by providing select box to choose between "UPDATE" and "DELETE."

If "UPDATE" is selected, the existing information for a specific person from the database is retrieved. The retrieved information is displayed and users were allowed to update the desired fields. On submission, the corresponding records were updated in the "businesscard" table.

If "DELETE" is selected, the existing information for a specific person from the database were retrieved. The retrieved information was displayed and provided a button labeled "DELETE" to remove the record from the database.

With this project workflow, users can effortlessly extract information from business cards, view and modify the extracted data, and store it in a MySQL database for efficient management and future reference.

Project Overview:

Install the required packages: You will need to install Python, Streamlit, easyOCR, and a database management system like SQLite or MySQL.

Design the user interface: Create a simple and intuitive user interface using Streamlit that guides users through the process of uploading the business card image and extracting its information. You can use widgets like file uploader, buttons, and text boxes to make the interface more interactive.

Implement the image processing and OCR: Use easyOCR to extract the relevant information from the uploaded business card image. You can use image processing techniques like resizing, cropping, and thresholding to enhance the image quality before passing it to the OCR engine.

Display the extracted information: Once the information has been extracted, display it in a clean and organized manner in the Streamlit GUI. You can use widgets like tables, text boxes, and labels to present the information.

Implement database integration: Use a database management system like SQLite or MySQL to store the extracted information along with the uploaded business card image. You can use SQL queries to create tables, insert data, and retrieve data from the database, Update the data and Allow the user to delete the data through the streamlit UI

Test the application: Test the application thoroughly to ensure that it works as expected. You can run the application on your local machine by running the command streamlit run app.py in the terminal, where app.py is the name of your Streamlit application file.

Improve the application: Continuously improve the application by adding new features, optimizing the code, and fixing bugs. You can also add user authentication and authorization to make the application more secure.
