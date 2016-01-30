# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.define "tracker-project-vm" do |vm_define|
  end

  config.vm.hostname = "tracker-project.local"

  config.vm.network "forwarded_port", guest: 80, host: 8000
  config.vm.network "forwarded_port", guest: 8000, host: 8001
  config.vm.network "forwarded_port", guest: 9000, host: 9000

  config.vm.synced_folder ".", "/home/vagrant/tracker_project/"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.name = "tracker-project-vm"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y supervisor nginx git build-essential python python-dev python-virtualenv postgresql postgresql-server-dev-all postgis postgresql-9.3-postgis-2.1 redis-server

    sudo -u postgres psql --command="CREATE USER tracker_project WITH PASSWORD 'tracker_project';"
    sudo -u postgres psql --command="CREATE DATABASE tracker_project WITH OWNER tracker_project;"
    sudo -u postgres psql --command="GRANT ALL PRIVILEGES ON DATABASE tracker_project TO tracker_project;"
    sudo -u postgres psql --command="CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" tracker_project
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    virtualenv --no-pip tracker_project_venv
    source tracker_project_venv/bin/activate
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

    pip install -r tracker_project/requirements.txt

    cd tracker_project/tracker_project/

    nodeenv --python-virtualenv
    npm install --global bower

    python manage.py migrate
    python manage.py bower_install
    python manage.py loaddata auth.json
    python manage.py collectstatic --noinput
  SHELL

  config.vm.provision "shell", inline: <<-SHELL
    echo '
      upstream tracker_project_upstream {
          server 127.0.0.1:8000 fail_timeout=0;
      }

      upstream tracker_project_ws_upstream {
          server 127.0.0.1:9000 fail_timeout=0;
      }

      map $http_upgrade $connection_upgrade {
          default upgrade;
          ''      close;
      }

      server {
          listen 80;
          server_name localhost;

          client_max_body_size 4G;

          access_log /home/vagrant/tracker_project/nginx_access.log;
          error_log /home/vagrant/tracker_project/nginx_error.log;

          location /static/ {
              alias /home/vagrant/tracker_project/tracker_project/static/;
          }

          location / {
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header Host $http_host;
              proxy_redirect off;
              if (!-f $request_filename) {
                  proxy_pass http://tracker_project_upstream;
                  break;
              }
          }

          location /notifications {
              proxy_pass http://tracker_project_ws_upstream;
              proxy_set_header Host $host:9000;
              proxy_redirect off;
              proxy_buffering off;
              proxy_http_version 1.1;
              proxy_set_header Upgrade $http_upgrade;
              proxy_set_header Connection "upgrade";
          }
      }
    ' > /etc/nginx/conf.d/tracker_project.conf

    /usr/sbin/service nginx restart

    echo '
      [program:tracker_project_uwsgi]
      user = vagrant
      command = /home/vagrant/tracker_project_venv/bin/uwsgi --chdir=/home/vagrant/tracker_project/tracker_project --module=tracker_project.wsgi:application --env DJANGO_SETTINGS_MODULE=tracker_project.settings --master --pidfile=/home/vagrant/tracker_project/tracker_project-master.pid --http=127.0.0.1:8000 --processes=5 --uid=1000 --gid=1000 --harakiri=20 --max-requests=5000 --vacuum --home=/home/vagrant/tracker_project_venv/
      autostart = true
      autorestart = true
      stderr_logfile = /home/vagrant/tracker_project/uwsgi_stderr.log
      stdout_logfile = /home/vagrant/tracker_project/uwsgi_stdout.log
      stopsignal = INT
    ' > /etc/supervisor/conf.d/tracker_project_uwsgi.conf

    echo '
      [program:tracker_project_runwsserver]
      user = vagrant
      directory = /home/vagrant/tracker_project/tracker_project
      command = /home/vagrant/tracker_project_venv/bin/python /home/vagrant/tracker_project/tracker_project/manage.py runwsserver
      autostart = true
      autorestart = true
      stderr_logfile = /home/vagrant/tracker_project/runwsserver_stderr.log
      stdout_logfile = /home/vagrant/tracker_project/runwsserver_stdout.log
      stopsignal = INT
    ' > /etc/supervisor/conf.d/tracker_project_runwsserver.conf

    /usr/bin/supervisorctl reload
  SHELL
end
