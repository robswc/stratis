FROM node:18-alpine AS base

# Install git
RUN apk add --no-cache git

# Clone from GitHub
ADD https://api.github.com/repos/robswc/stratis-ui latest_commit
RUN git clone https://github.com/robswc/stratis-ui.git /app

# Set working directory
WORKDIR /app

# Install dependencies
RUN npm install

# Build NextJS app
RUN npm run build

# Expose port 3000
EXPOSE 3000

ARG NEXT_PUBLIC_BACKEND_URL
ARG NEXT_PUBLIC_BACKEND_PORT

# Run NextJS app
CMD ["npm", "run", "start"]



