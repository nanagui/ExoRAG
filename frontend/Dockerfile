# syntax=docker/dockerfile:1.7
FROM node:20-alpine

WORKDIR /app
COPY package.json tsconfig.json vite.config.ts index.html .
COPY src ./src
COPY README.md ./README.md
COPY public ./public

RUN npm install && npm run build

EXPOSE 5173
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]
