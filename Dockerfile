FROM ubuntu:latest
LABEL authors="Stas"

ENTRYPOINT ["top", "-b"]