FROM registry.altlinux.org/p10/alt:20250625

RUN apt-get update && apt-get install -y \
    curl \
    git \
    gcc \
    make
ENV PYENV_ROOT=/root/.pyenv
ENV PATH=/root/.pyenv/bin:/root/.pyenv/shims:$PATH

RUN curl https://pyenv.run | bash 
RUN $PYENV_ROOT/bin/pyenv install 3.11.9 && \
$PYENV_ROOT/bin/pyenv global 3.11.9

ENV SRC=/src
ENV WORK=$SRC/work
ENV OUT=$SRC/out

RUN mkdir -p $SRC $WORK $OUT
WORKDIR $SRC

COPY fuzzNormilize.py $SRC/fuzzNormilize.py
COPY measure_cov.py $SRC/measure_cov.py
COPY test_corpus $SRC