FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y mongodb-server ruby-full ruby-dev build-essential git
RUN gem install bundler

COPY reddit /reddit
COPY gitlab-ci/reddit-monolith/mongod.conf /etc/mongod.conf
COPY gitlab-ci/reddit-monolith/db_config /reddit/db_config
COPY gitlab-ci/reddit-monolith/start.sh /start.sh

RUN cd /reddit && bundle install
RUN chmod 0777 /start.sh

CMD ["/start.sh"]
