FROM timegatime/py_mssql_pyodbc

# RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt install tzdata

RUN apt update
RUN pip3 install --upgrade pip

RUN apt-get install python3-pip -y
RUN apt-get install cron -y
RUN apt-get install git -y



#Mandatory for cron
RUN apt-get install nano -y
RUN export EDITOR=nano

WORKDIR /gasolineras
RUN mkdir gasolineras 
WORKDIR /home/gasolineras
COPY ./requirements.txt .
COPY ./main.py .
RUN pip3 install -r requirements.txt
RUN pip3 install pyodbc





RUN crontab -l | { cat; echo "0 8 * * * cd /home/gasolineras && /usr/local/bin/python3 /home/gasolineras/main.py"; } | crontab -
