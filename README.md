<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*-lYKsAKOdvXMe4lkSnpRFA.png" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">📈 Dockerized ML-Powered Sales Forecasting API</h1>
</p>
<p align="center"> <em>Developed with the software and tools below.</em>
</p>
<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Machine%20Learning-007ACC?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Machine Learning">
<img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
<img src="https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white" alt="NodeJS">
<img src="https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB" alt="Express.js">
<img src="https://img.shields.io/badge/NODEMON-%231e211e.svg?style=for-the-badge&logo=nodemon&logoColor=bbdec2" alt="Nodemon">
<img src="https://img.shields.io/badge/PM2-2B037A?style=for-the-badge&logo=pm2&logoColor=white" alt="PM2">
<img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

# 📈 ML-Powered Sales Forecasting API

This is a high-performance, containerized microservices architecture designed for predictive business intelligence. The system integrates a robust Node.js API Gateway with a specialized Python-based Machine Learning service to deliver accurate 12-month sales forecasts.

A high-performance **FastAPI** (Python) service that provides 12-month sales forecasts using Machine Learning. This service is designed to be "Always On," allowing a **Node.js** backend or a frontend application to fetch predictions instantly via REST API.

---

## 🚀 Features

- Predict sales for a specific product for the next N days.
- Node.js API calls Python ML model seamlessly.
- Uses historical sales data from Excel or database.
- Machine Learning model built with **Python, Pandas, and Scikit-learn**.
- Supports multiple products and returns prediction in JSON format.
- Easy to integrate into existing backend systems.
- Can be extended to support real-time sales forecasting pipelines.

---

## 🛠 Tech Stack

- **Backend:** Node.js, Express.js
- **Machine Learning:** Python, Scikit-learn, Pandas, Regression Models
- **Database:** MySQL / PostgreSQL / MongoDB (optional)
- **Deployment & DevOps:** Docker, CI/CD pipelines (GitHub Actions / GitLab CI)
- **Data Input:** Excel, CSV, or database queries

---

## 🛠️ Installation & Setup

### Prerequisites
* **Python 3.8+**
* **pip3** (Python Package Manager)
* **Node.js** (for integration)

### Install Dependencies
Run the following command to install the required Python libraries for AI processing and the web server:

```bash
pip3 install fastapi uvicorn pandas numpy scikit-learn python-dateutil openpyxl
```


---

## ⚡ Installation

 Clone the repo:
```bash
git clone https://github.com/muzahidswe/dockerized-ml-sales-forecasting-api.git
cd dockerized-ml-sales-forecasting-api
```
## 🚀 Running the Prediction Server
To start the service and keep it running for Node.js requests, navigate to the backend folder and run:

#### 1️⃣ Python Script
```bash
python3 predict.py
or
pm2 start "python3 predict.py" --name python-ai
```
#### 2️⃣ Node.js API
```bash
node backend/server.js
or
nodemon backend/server.js
```
### 📡 API Access Points
```bash
Base URL: http://127.0.0.1:8000
```
Traing Endpoint: GET /train

```bash
Example: http://127.0.0.1:8000/train/
```
Prediction Endpoint: GET /predict/{outlet_id}
```bash
Example: http://127.0.0.1:8000/predict/1001
```

### Start the Python API
pm2 start "python3 predict.py" --name sales-ai-service

### Ensure it starts on system reboot

Port Conflict: If port 8000 is used by another app, change the port in the last line of predict.py.