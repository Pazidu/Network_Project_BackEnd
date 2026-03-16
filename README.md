**WiFi Network Monitoring Mobile Application**

---

# **Project Description**

Many WiFi network owners do not have clear visibility into the devices connected to their network or the websites those devices access. Without proper monitoring tools, it becomes difficult to detect unknown devices, identify potential security risks, or understand network usage patterns.

This project aims to develop a **mobile-based WiFi network monitoring application** that allows users to monitor connected devices, analyze network activity, and track device usage in real time. The system collects network traffic information and displays it through a user-friendly mobile interface.

---

# **Objectives**

* Detects devices connected to the WiFi network.  
* Display usage information for each device including:  
  * Packet usage  
  * Download activity  
  * Upload activity  
  * Active sessions  
* Provide historical records of devices that have connected to the WiFi network.  
* Display WiFi network details such as:  
  * Network download speed  
  * Network upload speed  
  * Internet Service Provider (ISP)  
  * Network latency (Ping)

---

# 

# 

# **Target Users**

* Home WiFi users who want to monitor devices connected to their network.  
* Small office administrators who need basic network monitoring capabilities.

---

# **Overview**

The WiFi Network Monitoring Mobile Application provides a simple way for users to monitor network activity through their mobile devices. The system detects connected devices and collects network usage information such as packets, downloads, uploads, and sessions.

The backend system processes network data and stores it in a database, while the mobile application retrieves this information through APIs and displays it in a user-friendly format.

Users can view:

* Real-time network activity  
* Device usage statistics  
* Historical device information

This application helps users improve network visibility, identify unknown devices, and understand how their network resources are being used.

---

# **System Architecture**

## **System Workflow**

1. Devices connect to the WiFi network.  
2. The packet sniffer captures network packets from the network interface.  
3. DNS requests and packet information are extracted from captured packets.  
4. Device information such as MAC address, IP address, packet usage, uploads, downloads, and sessions is processed.  
5. The backend server stores the processed data in the database.  
6. The mobile application retrieves the data through API endpoints.  
7. The application displays the information using graphs and device activity lists.

---

# **System Components**

### **1\. Packet Sniffer**

Captures network traffic from the WiFi interface and extracts useful information such as DNS queries and packet statistics.

### **2\. Backend Server**

Processes captured packet data, manages device information, and provides API endpoints for the mobile application.

### **3\. Database**

Stores network activity data including:

* Device MAC address  
* Device IP address  
* Website domains visited  
* Packet usage  
* Upload and download statistics  
* Device connection history

### **4\. Mobile Application**

Provides the user interface where users can:

* View connected devices  
* Monitor network usage  
* View device history  
* Analyze network statistics using graphs

---

# 

# 

# 

# **Technologies Used**

## **Programming Languages**

* Python  
* JavaScript  
* SQL

## **Backend**

* FastAPI (Backend API)  
* Scapy  
* Uvicorn  
* SQLALchemy

## **Frontend**

* React Native  
* React Navigation  
* Lucide React  
* Axios

## 	**Security**

* JWT(python-jose)  
* Password Hashing(passlib with bcrypt)

## **Database**

* SQLite

## 	**Utilities**

* psutil(system info)  
* ping3(latency)  
* Python-dotenv

## **Dev Ops/Tools**

* Node.js (used to run React Native and manage frontend dependencies)  
* Android Studio  
* Postman  
* Git


---

**Installation Instructions**

## **Requirements**

Before running the system install:

* Python 3.10 or higher  
* Node.js  
* Android Studio  
* USB Debugged Android Device or Android Emulator  
* Git

(SQLite does not require installation because it is included with Python.)

---

# **Backend Installation**

* Clone the repository  
  * git clone https://github.com/MohomedImshan/Network\_Project\_BackEnd.git  
* Navigate to the backend folder  
  * cd Network\_Project\_BackEnd  
* Create a virtual environment  
  * python \-m venv venv  
* Activate the environment  
  * venv\\Scripts\\activate  
* Install dependencies  
  * pip install \-r requirements.txt  
* Run the backend server  
  * uvicorn main:app \--reload

---

# **Mobile Application Installation (Frontend)**

* Clone the repository  
  * git clone https://github.com/MohomedImshan/Network\_Project\_App\_Frontend.git  
* Navigate to the folder  
  * cd Network\_Project\_App\_Frontend  
* Install dependencies  
  * npm install  
* Start Metro server  
  * npx react-native start \--reset-cache  
* Run Android application  
  * npx react-native run-android  
* The application will build and install on the connected Android emulator or device.

---

**APK Build (Optional)**

* To generate an APK file:  
  * cd android  
* Run  
  * .\\gradlew assembleRelease  
* APK location:  
  * android/app/build/outputs/apk/debug/app-debug.apk  
* You can share this APK file to install the application on other Android devices.

---

# **Usage Instructions**

1. Start the backend server.  
2. Start the mobile application.  
3. Ensure both the backend server and mobile device are connected to the **same WiFi network**.  
4. Ensure the env has the correct ip address.  
5. Open the mobile application.

The application will display:

* Connected devices  
* Device usage statistics  
* Device visit history  
* WiFi network information  
* **Contributors**

  ### **M.I.M Imshan**

  Team Lead  
  2021/CSC/042  
  Email: [mohomedamccimshan@gmail.com](mailto:mohomedamccimshan@gmail.com)  
  Responsibilities:  
* Backend development  
* System integration  
* Code maintenance

  ### **W.G.P.B Wilagama**

  2021/CSC/042  
  Email: pasidubhagya20@gmail.com  
  Responsibilities:  
* Backend development

  ### **R.P.A Sajana**

  2021/CSC/094  
  Email: ashansajana0623@gmail.com  
  Responsibilities:  
* Frontend development

  ### **K.G.K Imalsha**

  2021/CSC/042  
  Email: kavishkaimalsha@gmail.com  
  Responsibilities:  
* Authentication implementation  
* Security features

---

# **License**

This project is licensed under the **MIT License**.