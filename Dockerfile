FROM python:3 AS build-python

RUN apt-get update \
    && apt-get install -y libyaml-dev

RUN useradd -m kbst
USER kbst:kbst

COPY --chown=kbst:kbst Pipfile Pipfile.lock /opt/kbst/

WORKDIR /opt/kbst
RUN export PATH=$HOME/.local/bin:$PATH \
    && pip install --user --no-cache-dir pipenv \
    && PIPENV_VENV_IN_PROJECT=true pipenv install

COPY --chown=kbst:kbst src/installer /opt/kbst/installer

FROM python:3-slim

RUN apt-get update \
    && apt-get install -y libyaml-0-2

RUN useradd -m kbst
USER kbst:kbst

ENV PATH=/opt/kbst/.venv/bin:$PATH

COPY --from=build-python --chown=kbst:kbst /opt/kbst /opt/kbst

WORKDIR /opt/kbst/installer
ENTRYPOINT ["python", "cmd.py"]
