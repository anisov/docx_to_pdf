FROM python:3.7.4-buster


RUN echo deb http://httpredir.debian.org/debian/ buster main contrib non-free >> /etc/apt/sources.list \
    && echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections \
    && apt-get upgrade \
    && apt-get update \
    && apt-get install -y \
    apt-utils \
    ttf-mscorefonts-installer \
    libreoffice-writer \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/


ADD ./code /code
COPY requirements.txt /code

RUN pip install -r /code/requirements.txt \
	&& mkdir -p /code/logs

EXPOSE 7777

CMD ["python", "-m","code"]
