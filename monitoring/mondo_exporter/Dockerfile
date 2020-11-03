FROM golang:alpine3.12

RUN apk --no-cache --update add build-base git && \
    go get -u github.com/percona/mongodb_exporter && \
    cd ${GOPATH-$HOME/go}/src/github.com/percona/mongodb_exporter && \
    make build && \
    apk del build-base

EXPOSE 9216

CMD ["/bin/mongodb_exporter"]
