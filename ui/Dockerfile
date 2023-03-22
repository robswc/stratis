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

# Add args
#ARG BACKEND_URL
#ENV BACKEND_URL=${BACKEND_URL}

#RUN echo "BACKEND_URL: ${BACKEND_URL}"

ARG MAX_OLD_SPACE_SIZE=1024

# Build NextJS app
RUN npm run build --max-old-space-size=${MAX_OLD_SPACE_SIZE}

# Expose port 3000
EXPOSE 3000

# Run NextJS app
CMD ["npm", "run", "start"]



