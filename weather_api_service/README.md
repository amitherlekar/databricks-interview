# cloud_solutions_admin_service
Cloud Solutions Admin Service

This application has a dependency on SQL Lite.
To set this application in your local machine, follow the instructures
1. Clone the repository
```
git clone https://github.com/nikhilbharadwaj-db/cloud_solutions_admin_service/
```
2. Create a new virtual environment
```
python3 -m venv venv
```
3. Activate virtual environment
```
source venv/bin/activate
```
4. Pip install all the requirements
```
pip install -r requirements.txt
```
5. Run the application
```
FLASK_RUN_PORT=5900 flask run
```
6. Invoke `http://127.0.0.1:5900/` on chrome to verify the launch. 
