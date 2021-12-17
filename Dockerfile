FROM python:3.9.9-slim-buster 

COPY . .

RUN mkdir /root/.ssh/

COPY ./id_ed25519 /root/.ssh/id_ed25519

COPY ./id_ed25519.pub /root/.ssh/id_ed25519.pub

RUN chmod 600 /root/.ssh/id_ed25519

RUN chmod 600 /root/.ssh/id_ed25519.pub

COPY  ca-bundle.crt usr/local/share/ca-certificates/my-cert.crt

RUN mkdir /etc/pki

RUN mkdir /etc/pki/tls

RUN mkdir /etc/pki/tls/certs

COPY ./ca-bundle.crt /etc/pki/tls/certs/ca-bundle.crt

RUN cat /usr/local/share/ca-certificates/my-cert.crt >> /etc/ssl/certs/ca-certificates.crt

RUN apt-get update

RUN apt-get -y --allow-unauthenticated install git

RUN ssh-keyscan -t rsa code.viawest.net >> /root/.ssh/known_hosts

RUN  ssh -T git@code.viawest.net

#RUN apt-get -y install software-properties-common

RUN apt-get -y --allow-unauthenticated install software-properties-common libpq-dev python3-dev git

RUN touch /usr/bin/pg_config

RUN export PATH=/usr/bin/pg_config:$PATH

ENV PYTHONPATH=":/opt/netops-lib/"

RUN git clone git@code.viawest.net:network/netops-lib.git /opt/netops-lib/

COPY ./creds.py /opt/netops-lib/netdb/creds.py

RUN pip --trusted-host pypi.org --trusted-host files.pythonhosted.org  install -r requirements.txt

RUN mkdir /var/log/webexbot

RUN touch /var/log/webexbot/webexbot.log

RUN echo $PYTHONPATH

CMD ["python", "./main.py"]

