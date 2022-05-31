FROM alpine:3.15.0

RUN apk add --no-cache python3

EXPOSE 80
STOPSIGNAL SIGTERM

WORKDIR /www
COPY www/* .
CMD python3 -m http.server 80

