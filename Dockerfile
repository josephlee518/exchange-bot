# Use Python Default Alpine Docker Repository
FROM python:alpine3.7

# Install tzdata and git (for Change Timezone and Use git for cloning Scripts)
RUN apk add --no-cache tzdata git

# Copy timezone to localtime folder
RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# Specify My Timezone
RUN echo "Asia/Seoul" > /etc/timezone && date

# Change Default PyPI Directory Into Kakao (KOREA) Server
RUN mkdir ~/.pip 
RUN printf "[global]\nindex-url=http://ftp.daumkakao.com/pypi/simple\ntrusted-host=ftp.daumkakao.com\n" > ~/.pip/pip.conf

# Clone Projects from git
RUN git clone https://github.com/josephlee518/exchange-bot

# Install Python Requirements from requirements.txt
RUN pip install -r /exchange-bot/requirements.txt

# RUN Trade.py forever
ENTRYPOINT cd /exchange-bot/scheduler && celery -A scheduler_currency_price worker --loglevel=info