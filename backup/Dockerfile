FROM alpine:latest

RUN apk add --no-cache mysql-client

WORKDIR /app
COPY backup.sh .
RUN chmod +x backup.sh

CMD ["while true; do ./backup.sh; done"]
ENTRYPOINT ["sh", "-c"]