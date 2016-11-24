# prepare log output folder
sudo mkdir /tmp/uwsgi

# prepare virtualenv
sudo mkdir v_env
source v_env/bin/activate

# prepare project requirements tools
sudo apt-get install python-pip
#pip install --upgrade pip
sudo pip install uwsgi

# prepare project requirements
echo "updating requirements..."
pip install -r requirements.txt

# prepare mongo service
#echo "starting mongo"
#exec service mongodb start &
#echo "mongo should be started already"

# hot-fix of import problem
echo "EXPORT PYTHONPATH"
export PYTHONPATH=${PYTHONPATH}:/code/pychatty/

# start service itself
echo "starting uwsgi"
exec uwsgi --ini uwsgi.ini --pidfile /tmp/pychatty.pid &
#exec uwsgi --socket 0.0.0.0:8181 --protocol=http -w pychatty &

# exit virtualenv
deactivate
