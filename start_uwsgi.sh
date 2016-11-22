sudo mkdir /tmp/uwsgi

source chat_env/bin/activate

sudo apt-get install python-pip
#pip install --upgrade pip
sudo pip install uwsgi

echo "updating requirements..."
pip install -r requirements.txt

#echo "starting mongo"
#exec service mongodb start &
#echo "mongo should be started already"

echo "EXPORT PYTHONPATH"
export PYTHONPATH=${PYTHONPATH}:/code/pychatty/

echo "starting uwsgi"
exec uwsgi --ini uwsgi.ini --pidfile /tmp/pychatty.pid &
#exec uwsgi --socket 0.0.0.0:8181 --protocol=http -w pychatty &


deactivate
