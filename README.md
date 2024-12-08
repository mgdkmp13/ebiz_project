# README - Warhammer Merchandise Replica Project

## Project Overview

This project aims to replicate the Warhammer Merchandise website and embed it within a PrestaShop-based system, leveraging modern technologies to create a robust e-commerce solution.

### Main Features

- **Containerized PrestaShop**: Configured to use a MySQL database within a Docker environment.
- **Web Scraper**: Extracts product and category data from the original Warhammer website.
- **API Connector**: Formats and imports scraped data into the PrestaShop system.
- **Automated Testing**: Ensures system reliability and functionality using Selenium.
- **Backup Mechanisms**: Enables version-controlled backups of the project state.
- **SSL Support**: Includes OpenSSL-generated certificates for secure HTTPS connections.

---

## Tech Stack

- **PrestaShop**: Version 1.7.8 with Apache
- **MySQL**: Database for PrestaShop
- **Docker**: For containerized deployment
- **PHPMyAdmin**: Database management
- **Python**: For scripting and automation
- **Selenium**: For automated testing
- **PrestaPy**: API connector for PrestaShop
- **OpenSSL**: SSL certificate generation

---

## Authors

- **Magdalena Krampa** - 193195  
- **Adam Białek** - 193677  
- **Kacper Witczak** - 193609  
- **Iwo Czartowski** - 193066  

Team "Atomówki" - 5th Semester, Computer Science, Gdańsk University of Technology

---

## Installation and Usage

### Prerequisites

1. Install Docker (Linux) or Docker Engine (Windows/MacOS).  
2. If using Windows, install WSL.

### Steps to Run Locally

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/mgdkmp13/ebiz_project.git
   cd ebiz_project

2. **Run Docker Containers**
   chmod 777 ./run.sh
   ./run.sh --build

3. **Access the Website**
    - **Main Page**: [https://localhost:8443](https://localhost:8443)  
    - **Admin Panel**: [https://localhost:8443/admin123](https://localhost:8443)  
        - **Email**: admin@prestashop.com  
        - **Password**: admin123  

4. **Run the Web Scraper**
    See [Scrapper/README.md](Scrapper/README.md) for details.

5. **Run Automated Tests**
    See [tests/README.md](tests/README.md) for details.
    
6. **Database backup**
    python ./dbdump/dbdump.sh
7. **Api uploader**
    python ./PrestaShopApiConnector/main.py