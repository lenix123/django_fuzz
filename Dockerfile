FROM registry.altlinux.org/p11/alt:20250625

RUN apt-get update && apt-get install -y \
   python3 \
   python3-module-pip \
   gcc \
   glibc \
  python3-modules-sqlite3


ENV SRC=/src
ENV WORK=$SRC/work
ENV OUT=$SRC/out

RUN mkdir -p $SRC $WORK $OUT
WORKDIR $SRC

COPY fuzzNormilize.py $SRC/fuzzNormilize.py
COPY fuzzXML.py $SRC/fuzzXML.py
COPY ./corpus_norm $SRC/corpus_norm
COPY ./corpus_xml $SRC/corpus_xml
COPY requirements.txt $SRC
RUN python3 -m pip install -r requirements.txt
