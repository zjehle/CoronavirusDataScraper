FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

MAINTAINER Ivan Ermilov <ivan.s.ermilov@gmail.com>

COPY covid-scraper.py /opt/hadoop/applications/covid-scraper.py

ADD run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]