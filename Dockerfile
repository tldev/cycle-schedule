# Use the official lightweight Nginx image
FROM nginx:alpine

# Copy the application source code to the Nginx web root directory
COPY ./src /usr/share/nginx/html

# Copy the custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 to the outside world
EXPOSE 80