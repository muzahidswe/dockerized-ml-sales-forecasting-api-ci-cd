# backend/Dockerfile

# 1️⃣ Base image - Python (for ML)
FROM python:3.11-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Copy backend files
COPY . .

# 5️⃣  Expose port
EXPOSE 8000

# 6️⃣ Start Node.js server
CMD ["python", "predict.py"]