FROM node:18

WORKDIR /app

# Only copy package files initially for better caching
COPY package*.json ./

# Install dependencies
RUN npm install

# We don't need to copy the rest of the files or build
# since we'll be mounting the volume in development

EXPOSE 3000

# Use npm run dev for development with hot reload
CMD ["npm", "run", "dev"]