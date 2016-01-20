#!/bin/bash

if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

echo "Move to the jasper directory"
cd $(dirname "$0")

echo "Installing VBoxLinuxAdditions"

# Find a way to mount the ISO automatically
# ./runasroot.sh 
# ./runasroot.sudo sh 
# ./runasroot
# su -
# ./VBoxLinuxAdditions.run 
# ./VBoxLinuxAdditions.run 
# lightdm restart
# service lightdm restart
# pwd

echo "Install python audio tools"
echo "Updating packages repository"
apt-get update -y
echo "Upgrading the pending applications"
apt-get upgrade --yes
apt-get install vim git-core python-dev python-pip bison libasound2-dev libportaudio-dev python-pyaudio --yes

# Try to record the sound to a file
#arecord temp.wav
#aplay =D hw:1,0 temp.wav 
#aplay -D hw:1,0 temp.wav 
#aplay -D temp.wav 
#aplay  temp.wav 
#ll
#alsa force-reload
#arecord temp.wav
#aplay  temp.wav 

echo "Configure alsa sound manager"
#vim /etc/modprobe.d/alsa-base.conf 
#alsa force-reload
#vim /etc/modprobe.d/alsa-base.conf 
#alsa force-reload
#arecord temp.wav
#aplay  temp.wav 
#ll
#vim /etc/modprobe.d/alsa-base.conf 
#alsa force-reload
#arecord temp.wav
#aplay  temp.wav 
#touch ~/.bash_profile
#vim ~/.bash_profile 
#vim ~/.bashrc

#echo "Get the code from github"
#git clone https://github.com/jasperproject/jasper-client.git jasper

echo "Install requirements for python"
pip install --upgrade setuptools
pip install -r client/requirements.txt

echo "Updating packages repository"
apt-get update -y

echo "Install pocketsphinx, subversion, pyaudio and related tools"
apt-get install pocketsphinx --yes
apt-get update -y 
apt-get install subversion autoconf libtool automake gfortran g++ python-pocketsphinx libpocketsphinx1 gstreamer0.10-pocketsphinx python-pyaudio --yes
apt-get install subversion autoconf libtool automake gfortran g++ --yes

echo "Installing cmuclmtk "
svn co https://svn.code.sf.net/p/cmusphinx/code/trunk/cmuclmtk/
cd cmuclmtk/
./autogen.sh && sudo make && sudo make install
cd ..

echo "Let the OS install experimental and non-free packages"
su -c "echo 'deb http://ftp.debian.org/debian experimental main contrib non-free' > /etc/apt/sources.list.d/experimental.list"
echo "Updating packages repository"
apt-get update

echo "Install phonetisaurus"
apt-get -t experimental install phonetisaurus m2m-aligner mitlm -y
su -c "echo 'deb http://ftp.debian.org/debian experimental main contrib non-free' > /etc/apt/sources.list.d/experimental.list"
apt-get update
apt-get -t experimental install phonetisaurus m2m-aligner mitlm -y
wget http://phonetisaurus.googlecode.com/files/g014b2b.tgz
tar -xvf g014b2b.tgz
wget http://phonetisaurus.googlecode.com/files/g014b2b.tgz
wget https://www.dropbox.com/s/kfht75czdwucni1/g014b2b.tgz?dl=0

echo "Install voices"
tar -xvf g014b2b.tgz*
cd g014b2b/
./compile-fst.sh
fstcompile
cd ..

echo "Install openfst"
wget http://distfiles.macports.org/openfst/openfst-1.3.3.tar.gz
wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.3.3.tar.gz
tar -xvf openfst-1.3.3.tar.gz
cd openfst-1.3.3/
./configure --enable-compact-fsts --enable-const-fsts --enable-far --enable-lookahead-fsts --enable-pdt
make install
cd ..

cd g014b2b/
./compile-fst.sh
cd ..
mv ~/g014b2b ~/phonetisaurus

echo "Install julius"
apt-get update
apt-get install build-essential zlib1g-dev flex libasound2-dev libesd0-dev libsndfile1-dev -y
wget http://sourceforge.jp/projects/julius/downloads/60273/julius-4.3.1.tar.gz/
#mv Downloads/julius-4.3.1.tar.gz .
tar -xvf julius-4.3.1.tar.gz 
mv julius-4.3.1 julius
cd julius
./configure --enable-words-int
make
make install
cd ..

echo "Install festival, espeak, festvox-don"
echo "Updating packages repository"
apt-get update
apt-get install espeak -y

apt-get update
apt-get install festival festvox-don -y

echo "Updating packages repository"
apt-get update
apt-get install festival festvox-don flite libttspico-utils python-pymad -y
#pip install --upgrade gTTS

echo "Updating packages repository"
apt-get update
apt-get install python-pymad -y

echo "Upgrade python library gTTS and pyvona"
pip install --upgrade gTTS
pip install --upgrade pyvona

apt-get update
apt-get install build-essential zlib1g-dev flex libasound2-dev libesd0-dev libsndfile1-dev --yes

echo "Configure and install julius"
cd julius
./configure --enable-words-int
make
make install
cd ..
locate julius | grep hmmdefflite =lv
flite -lv
cd ..

echo "Tune the audio mixer to get some sound"


echo "Install supervisord"
apt-get install supervisor -y

echo "setup the run program"
service supervisor restart
cp jasper.conf /etc/supervisor/conf.d/

echo "refresh supervisor"
supervisorctl reread
supervisorctl update

echo "Boot jasper"
#/home/pi/jasper/jasper.py --local --debug --diagnose
#history >> historyinstallation.txt
