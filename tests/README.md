In order to execute tests install chrome on wsl with commands below in exact order:

    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg

    echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list

    sudo apt update

    sudo apt install -y google-chrome-stable

Check if properly installed with:

    google-chrome --version

Installing Libraries

    You can install all the required libraries using the pip package manager. Use the following command:

    pip install selenium

Additional Requirements

    Python version 3.8 or newer.

Running the Script

    Ensure you meet the requirements listed above.
    Run the script using the command:

    python tests.py

