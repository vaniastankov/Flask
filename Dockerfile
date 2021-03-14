FROM ubuntu:20.04
MAINTAINER Ivan Stankov 'vania.stankoov@gmail.com'
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Kiev
RUN apt-get update -y
RUN apt-get install -y tzdata
RUN apt-get install -y python3-pip
COPY . /app
WORKDIR /app 
RUN apt-get install -y python3.8
RUN pip3 install -r requirements.txt

RUN apt-get install -y build-essential xorg libssl-dev libxrender-dev wget

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends xvfb libfontconfig libjpeg-turbo8 xfonts-75dpi fontconfig

RUN wget --no-check-certificate https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
RUN dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
RUN rm wkhtmltox_0.12.5-1.bionic_amd64.deb

EXPOSE 5000

ENTRYPOINT ["python3.8"]
CMD ["run.py"]