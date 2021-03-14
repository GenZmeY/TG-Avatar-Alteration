# TG-Avatar-Alteration
Service that automatically changes your telegram avatar during the day.

# Description
The service is a small python3 script (and config for it) that changes the avatar and systemd timer that is configured to run this script every minute.

For the initial session setup, a bash wrapper for the python script is used. 

# Requirements
**Any OS from the list:**
- RHEL7;
- RHEL8;
- CentOS7;
- CentOS8.

# Install
1. [Download the rpm package](https://github.com/GenZmeY/TG-Avatar-Alteration/releases) for your operating system or build it yourself;
2. Copy it to the target system;
3. Install the package:  
`yum install <rpm_filename> # RHEL7/CentOS7`   
or  
`dnf install <rpm_filename> # RHEL8/CentOS8`  

# Build (manual)
1. Install build dependencies:  
`yum install git rpm-build # RHEL7/CentOS7`  
or  
`dnf install git rpm-build # RHEL8/CentOS8`  
2. Download sources:  
`git clone https://github.com/GenZmeY/TG-Avatar-Alteration ~/rpmbuild`
3. Build packages:  
`rpmbuild ~/rpmbuild/SPECS/tg-avatar-alteration.spec`
4. The source package will be here:  
`~/rpmbuild/SRPMS/`  
The installation package will be here:  
`~/rpmbuild/RPMS/noarch/`  

# Setup & Usage
0. Open config `/etc/tg-avatar-alteration/config.py` and edit it:
1. Get **API_ID** and **API_HASH** [here](https://my.telegram.org/apps), add them to config.
2. Change **PHONE** to your phone number (you will receive a confirmation code to this number during the initial session setup).
3. Change **TIMEZONE** to your [timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
4. Change **IMG_DIR** to the directory where your avatars will be located.
5. In the **IMG_EXT** parameter, specify the extension for your avatar files.
6. Put 1440 images (one picture for every minute) to the directory you previously specified in **IMG_DIR**. Images must have names in the range 0000 - 1339 (eg 0000.png, 0001.png, etc). 0000 corresponds to the first minute of the day, 0001 corresponds to the second minute of the day, and so on.
7. If you need to adjust the display time, you can use the **OFFSET** parameter in the config. It is added to the file index. For example, if you want the image 0060 to be displayed instead of 0000 in the first minute of the day, you need to set OFFSET="60".
8. Run the `tg-avatar-alteration` command to establish a session.
9. Start a timer that will change your avatar every minute:  
`sudo systemctl start tg-avatar-alteration.timer`
10. If you need the timer to work after a reboot, enable the timer:  
`sudo systemctl enable tg-avatar-alteration.timer`

# Now you can turn your avatar into something like this:
![](example.gif)

# License
[GNU GPLv3](LICENSE)