FROM ubuntu:24.04

RUN dpkg --add-architecture i386

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat libstdc++6:i386 libc6

RUN useradd -ms /bin/sh jens

WORKDIR /home/jens

COPY ./grades.txt ./
COPY ./aaugrader ./
COPY ./src/run.sh ./

RUN chown -R jens:jens /home/jens && \
    chmod 750 /home/jens && \
    chown jens:jens /home/jens/grades.txt && \
    chmod 660 /home/jens/grades.txt

EXPOSE 8000

CMD ["./run.sh"]
