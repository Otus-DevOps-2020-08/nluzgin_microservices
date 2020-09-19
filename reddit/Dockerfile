FROM ruby:alpine3.12

ENV APP_HOME /app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
ADD Gemfile* $APP_HOME/

COPY gitlab-ci/reddit-monolith/mongod.conf /etc/mongod.conf
COPY gitlab-ci/reddit-monolith/db_config /db_config
COPY gitlab-ci/reddit-monolith/start.sh /start.sh

RUN apk --no-cache --update add build-base && \
    gem install bundler -v 1.17.2 && \
    bundle install && \
    apk del build-base && \
    chmod 0777 /start.sh && \

ADD . $APP_HOME

#ENV COMMENT_DATABASE_HOST comment_db
#ENV COMMENT_DATABASE comments

CMD ["/start.sh"]
