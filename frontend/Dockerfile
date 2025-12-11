FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps || npm install

COPY . .

EXPOSE 5173

CMD ["sh", "-c", "npm install --legacy-peer-deps || npm install && npm run dev -- --host 0.0.0.0"]
