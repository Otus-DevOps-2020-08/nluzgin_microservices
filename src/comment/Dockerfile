FROM ruby:alpine3.12

#RUN apt-get update -qq && apt-get install -y build-essential

ENV APP_HOME /app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ADD Gemfile* $APP_HOME/
RUN apk --no-cache --update add build-base && \
    gem install bundler -v 1.17.2 && \
    bundle install && \
    apk del build-base

ADD . $APP_HOME

ENV COMMENT_DATABASE_HOST comment_db
ENV COMMENT_DATABASE comments

CMD ["puma"]
