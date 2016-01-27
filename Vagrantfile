# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.define "tracker-project-vm" do |vm_define|
  end

  config.vm.hostname = "tracker-project.local"

  config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.vm.synced_folder ".", "/home/vagrant/tracker_project/"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.name = "tracker-project-vm"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y build-essential python python-dev python-virtualenv postgresql postgresql-server-dev-all postgis postgresql-9.3-postgis-2.1 rabbitmq-server

    sudo -u postgres psql --command="CREATE USER tracker_project WITH PASSWORD 'tracker_project';"
    sudo -u postgres psql --command="CREATE DATABASE tracker_project WITH OWNER tracker_project;"
    sudo -u postgres psql --command="GRANT ALL PRIVILEGES ON DATABASE tracker_project TO tracker_project;"
    sudo -u postgres psql --command="CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" tracker_project
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    virtualenv --without-pip tracker_project_venv
    source tracker_project_venv/bin/activate
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

    pip install -r tracker_project/requirements.txt

    cd tracker_project/tracker_project/

    nodeenv --python-virtualenv
    npm install --global bower

    python manage.py migrate
    python manage.py bower_install
    python manage.py loaddata data.json
  SHELL
end
