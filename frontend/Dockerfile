# Use Node 18 LTS as base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install a simple HTTP server
RUN npm install -g serve

# Create a simple placeholder HTML file
RUN echo '<html><body><h1>Todo Frontend Placeholder</h1><p>Frontend service is running</p></body></html>' > index.html

# Expose port 3000
EXPOSE 3000

# Serve the placeholder page
CMD ["serve", "-s", ".", "-l", "3000"]