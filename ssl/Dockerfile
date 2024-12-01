FROM prestashop/prestashop:1.7.8

# Create directories
COPY ./certGen.sh /usr/local/bin/certGen.sh

# Make the script executable
RUN chmod +x /usr/local/bin/certGen.sh

# Run the SSL certificate generation script
RUN /usr/local/bin/certGen.sh

# Copy custom Apache configuration file
COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf

# Enable SSL and site configuration
RUN a2enmod ssl && a2ensite 000-default.conf

# Start Apache in the foreground
CMD ["apache2-foreground"]
