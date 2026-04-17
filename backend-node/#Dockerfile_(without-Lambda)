# backend/Dockerfile

# 1️⃣ Node
FROM node:18

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install Node.js (for backend)
RUN apt-get update && apt-get install -y curl gnupg build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs

# 4️⃣ Copy backend files
COPY package*.json ./
COPY . .

# 5️⃣ Install Node.js dependencies
RUN npm install

# 7️⃣ Expose port
EXPOSE 3000

# 8️⃣ Start Node.js server
CMD ["node", "server.js"]