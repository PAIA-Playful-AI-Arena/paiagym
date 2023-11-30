# Install xserver-xorg-video-dummy for X server and virtual screen
if [ -z "$(dpkg -l | grep xserver-xorg-video-dummy)" ]
then
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt install -y xserver-xorg-video-dummy
fi

# make sure that :0 has a screen to display
if [ -z "${DISPLAY}" ] || [ $DISPLAY != ":0" ]
then
    if [ ! -z "$(which nvidia-xconfig)" ]
    then
        # using NVIDIA Driver on machine with GPU Driver
        nvidia-xconfig -a --allow-empty-initial-configuration --virtual=1920x1080
    else
        # Download a virtual screen config for machine without GPU (using only CPU)
        if [ -z "$(which wget)" ]
        then
            apt-get update
            apt install -y wget
        fi
        if [ -e "/etc/X11/xorg.conf" ]
        then
            # To backup the old config
            mv /etc/X11/xorg.conf /etc/X11/xorg.conf.backup_before_dummy
            echo "backup /etc/X11/xorg.conf to /etc/X11/xorg.conf.backup_before_dummy"
        fi
        wget -P /etc/X11 http://xpra.org/xorg.conf
    fi
    # start the X server on :0
    X :0 &> /dev/null
    echo "Create Display :0, please execute: export DISPLAY=:0"
else
    echo "Display $DISPLAY already exists"
fi

# make sure that /tmp/.X11-unix socket exists
X11_SOCKET=/tmp/.X11-unix
if [ ! -e $X11_SOCKET ]
then
    echo "$X11_SOCKET does not exists, please install relative applications"
fi