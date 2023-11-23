FROM python:3.11-alpine3.18 AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock /project/
COPY src/ /project/src

# install dependencies and project into the local packages directory
WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable


FROM python:3.11-alpine3.18

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.11/lib /project/pkgs
# retrieve executables
COPY --from=builder /project/__pypackages__/3.11/bin/* /bin/

WORKDIR /project/

# set command/entrypoint
CMD ["python","-m","app.bot"]
