# Use a lightweight web server to serve static files
FROM nginx:alpine

# Set the working directory inside the container
WORKDIR /usr/share/nginx/html

# Copy the frontend files into the container
#COPY Webpage-html-3/frontend/ .
COPY . .

# Expose the port on which the web server runs
EXPOSE 5000

# Default command to start Nginx
CMD ["nginx", "-g", "daemon off;"]
