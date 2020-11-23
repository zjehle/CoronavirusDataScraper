FROM python
RUN pip install requests
RUN pip install pandas
RUN pip install beautifulsoup4
COPY . /src
CMD ["python","/src/covid-scraper.py"]
