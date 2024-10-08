# Setup


## Installing dependencies
You need to install the following packages on your host machine to enable virtualization and manage VMs:


### On Ubuntu/Debian-based systems:
```
sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager
```

### On Fedora/RHEL-based systems:
```
sudo dnf install -y @virtualization
sudo systemctl start libvirtd
sudo systemctl enable libvirtd
```
Ensure that the libvirt daemon is running:

```
sudo systemctl start libvirtd
sudo systemctl enable libvirtd
```


## Setup Django APP

```

git clone https://github.com/antonymwangig/hynfratechbe.git

cd hynfratechbe

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py setup_roles
python manage.py populate_servie_plans

```