FROM prestashop/prestashop:1.7.8

# Install OpenSSL
RUN apt-get update && apt-get install -y openssl

# Create directories for certificates and keys
RUN mkdir -p /etc/apache2/private && mkdir -p /etc/apache2/certs

# Generate the SSL certificate and key
RUN openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/apache2/private/selfKey.key -out /etc/apache2/certs/selfCert.crt -subj "/C=US/ST=State/L=City/O=Company/OU=Department/CN=localhost"

# Change ownership of the key and certificate files
RUN chown www-data:www-data /etc/apache2/private/selfKey.key /etc/apache2/certs/selfCert.crt

# Copy custom Apache configuration file
COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf

# Enable SSL and site configuration
RUN a2enmod ssl && a2ensite 000-default.conf

# Start Apache in the foreground
CMD ["apache2-foreground"]
