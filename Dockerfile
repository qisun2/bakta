FROM mambaorg/micromamba:0.25.1


COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml

RUN micromamba install -y -n base -f /tmp/environment.yml && \
   micromamba clean --all --yes

COPY --chown=$MAMBA_USER:$MAMBA_USER . /tmp/source/

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN python3 -m pip install --no-cache /tmp/source/ && \
   rm -fr /tmp/source
