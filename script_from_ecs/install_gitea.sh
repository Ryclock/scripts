#!/usr/bin/env bash

# Check Git(>=2.0)
git_version_minimum=2.0
if ! command -v git &>/dev/null; then
    echo "Git is not installed. Please install Git version ${git_version_minimum} or higher."
    exit 1
fi

git_version=$(git --version | awk '{print $3}')
if [[ ${git_version} < ${git_version_minimum} ]]; then
    echo "Git version ${git_version} is not supported. Please install Git version ${git_version_minimum} or higher."
    exit 1
fi

# Check MySQL
if ! command -v mysql --version &>/dev/null;  then
    echo "MySQL is not installed. Please install MySQL."
    exit 1
else 
    systemctl is-active mysql &>/dev/null || sudo systemctl start mysql
fi

# Install Gitea
echo "Install Gitea ..."
arch=$(uname -m)
case ${arch} in
    "x86_64")
        gitea_file=gitea-main-nightly-linux-amd64
    ;;
    "i386")
        gitea_file=gitea-main-nightly-linux-386
    ;;
    "armv5l")
        gitea_file=gitea-main-nightly-linux-arm-5
    ;;
    "armv6l")
        gitea_file=gitea-main-nightly-linux-arm-6
    ;;
    "aarch64")
        gitea_file=gitea-main-nightly-linux-arm64
    ;;
    *)
        echo "Unsupported: ${arch}"
        # exit 1
    ;;
esac

#! outside
wget -O gitea https://dl.gitea.com/gitea/main/${gitea_file}
chmod +x gitea
sudo mv gitea /usr/local/bin/gitea

id -u git &>/dev/null && sudo adduser --system --shell /bin/bash --gecos 'Git Version Control' --group --disabled-password --home /home/git git
sudo mkdir -p /var/lib/gitea/{custom,data,indexers,public,log}
sudo chown git:git /var/lib/gitea/{data,indexers,log}
sudo chmod 750 /var/lib/gitea/{data,indexers,log}
sudo mkdir /etc/gitea
sudo chown root:git /etc/gitea
sudo chmod 770 /etc/gitea

#! outside
sudo wget -O /etc/systemd/system/gitea.service https://raw.githubusercontent.com/go-gitea/gitea/main/contrib/systemd/gitea.service
sudo sed -i 's/^#\(.*=mysql\.service\)/\1/' /etc/systemd/system/gitea.service

sudo systemctl daemon-reload
sudo systemctl enable gitea
sudo systemctl start gitea

chmod 750 /etc/gitea
chmod 640 /etc/gitea/app.ini