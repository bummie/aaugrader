FROM ubuntu:24.04

ARG BINARY_NAME="aaugrader"
ARG RUN_SCRIPT="aaugrader.sh"

RUN dpkg --add-architecture i386

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat libstdc++6:i386 libc6 strace curl binutils

RUN useradd -ms /bin/sh jens

WORKDIR /home/jens

COPY ./grades.txt ./
COPY ./${BINARY_NAME} ./aaugrader
COPY ./run.sh ./
COPY ./${RUN_SCRIPT} ./aaugrader.sh

RUN chown -R jens:jens /home/jens && \
    chmod 750 /home/jens && \
    chown jens:jens /home/jens/grades.txt && \
    chmod 660 /home/jens/grades.txt

EXPOSE 8000

CMD ["./run.sh"]
