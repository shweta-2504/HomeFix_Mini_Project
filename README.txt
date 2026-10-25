HOMEFIX — MINI PROJECT
Frontend: HTML, CSS, JavaScript
Backend: Python Flask
Database: MySQL
Editor: Visual Studio Code on Windows

FEATURES
1. Appliance Selection: choose AC, Refrigerator, Washing Machine, Fan, Microwave or Water Heater.
2. Problem/Symptom Detection: type the problem or use quick symptom buttons.
3. Troubleshooting Engine: searches stored MySQL rules and returns possible causes.
4. Solution & Safety Guide: provides simple steps and safety warnings.
5. Repair History & Technician Suggestion: stores recent checks and gives a technician safety checklist.

REQUIREMENTS
- Python 3.10 or newer
- MySQL Server and MySQL Workbench (or another MySQL client)
- Visual Studio Code
- Internet is needed only to load the optional Google font; the app itself runs locally.

WINDOWS SETUP
1. Extract the HomeFix_Mini_Project ZIP to a folder.
2. Install Python and MySQL Server if not already installed.
3. Open MySQL Workbench and connect to your local server.
4. Open database.sql in Workbench and execute the full script. It creates homefix_db and sample troubleshooting rules.
5. Open the extracted folder in VS Code.
6. Open Terminal > New Terminal.
7. Create a virtual environment:
   py -m venv .venv
8. Activate it in PowerShell:
   .venv\Scripts\Activate.ps1
   If PowerShell blocks activation, use Command Prompt terminal and run:
   .venv\Scripts\activate.bat
9. Install packages:
   pip install -r requirements.txt
10. Set your MySQL password before starting, if your MySQL root user has a password.
    PowerShell:
      $env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
    Command Prompt:
      set DB_PASSWORD=YOUR_MYSQL_PASSWORD
    If your MySQL username is not root, set DB_USER similarly.
11. Run:
      python app.py
12. Open this address in your browser:
      http://127.0.0.1:5000

TROUBLESHOOTING
- "Access denied": set DB_USER and DB_PASSWORD to your actual MySQL credentials.
- "Unknown database homefix_db": run database.sql in MySQL Workbench.
- "Can't connect to MySQL": start MySQL Server from Windows Services or MySQL Workbench.
- Do not double-click index.html. Run app.py and open http://127.0.0.1:5000 so the Python API works.

SAFETY / PROJECT SCOPE
This is an educational prototype, not a certified repair service. It only gives basic user-level checks. It does not recommend opening appliances, touching wiring, bypassing safety locks, or doing dangerous repairs. If there is smoke, sparking, burning smell, or a serious leak, stay away and seek qualified help.
