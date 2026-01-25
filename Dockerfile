FROM registry.altlinux.org/p11/alt:20250625

RUN apt-get update && apt-get install -y \
   python3 \
   python3-module-pip \
   gcc \
   glibc \
  python3-modules-sqlite3 \
  python3-dev
ENV SRC=/src
ENV OUT=/out
RUN mkdir -p $SRC  $OUT
WORKDIR $SRC
COPY Normilize_fuzzer.py $SRC/
COPY XML_fuzzer.py $SRC/
COPY urlize.py $SRC/
COPY ./corpus_urlize $OUT/corpus_urlize
COPY ./corpus_norm $OUT/corpus_norm
COPY ./corpus_xml $OUT/corpus_xml
COPY requirements.txt $SRC
COPY build.sh $SRC/
RUN chmod +x $SRC/build.sh
RUN python3 -m pip install -r requirements.txt
