# hynfratechbe
Setup
Clone the repository:

bash
git clone https://github.com/your-username/django-vm-manager
cd django-vm-manager
Create a virtual environment and activate it:

bash
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
python manage.py migrate
python manage.py setup_roles
python manage.py populate_servie_plans

