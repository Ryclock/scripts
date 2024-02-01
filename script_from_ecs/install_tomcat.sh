#!/usr/bin/env bash

user=""
ip=""
dir=""

# Install JDK
echo 'Installing JDK ...'
jdk_verision=20.0.1
jdk_pkg=jdk-${jdk_verision}

arch=${uname -m}
case ${arch} in
    "x86_64")
        jdk_file=openjdk_${jdk_verision}_linux-x64_bin.tar.gz
    ;;
    "aarch64")
        jdk_file=openjdk_${jdk_verision}_linux-arch64_bin.tar.gz
    ;;
    *)
        echo "! ${arch} is not support"
        exit 1
    ;;
esac

[ ! -f ${jdk_file} ] && scp "${user}"@"${ip}":"${dir}"/${jdk_file} ./
[ -f ${jdk_file} ] && tar -zxf ${jdk_file}
[ -d ${jdk_pkg} ] && cp -a ${jdk_pkg} /usr/local/java

cat <<EOF >>/etc/profile
export JAVE_HOME=/usr/local/java
export PATH=\${JAVA_HOME}/bin;\${PATH}
EOF

source /etc/profile
java -version

# Install Tomcat
echo 'Installing Tomcat ...'
tomcat_version=8.0.50
tomcat_file=apache-tomcat-${tomcat_version}.tar.gz
tomcat_pkg=apache-tomcat-${tomcat_version}
tomcat_dir=/usr/local/tomcat

[ ! -f ${tomcat_file} ] && scp "${user}"@"${ip}":"${dir}"/${tomcat_file} ./
[ -f ${tomcat_file} ] && tar -zxf ${tomcat_file}
[ -d ${tomcat_pkg} ] && cp -a ${tomcat_pkg} /usr/local/java

${tomcat_dir}/bin/startup.sh