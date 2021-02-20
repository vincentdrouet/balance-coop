FROM node:14-slim AS frontend
COPY ./client /app/client
RUN  cd /app/client &&\
     npm install &&\
     npm run build

FROM python:3.8-slim AS backend
WORKDIR /app
COPY ./pyproject.toml ./poetry.lock ./main.py /app/
COPY ./api /app/api
RUN  pip install poetry &&\
     poetry build -f wheel

FROM python:3.8-slim
WORKDIR /app
COPY --from=frontend /app/client/dist /app/client/dist
COPY --from=backend /app/dist/balance_coop-*-py3-none-any.whl /tmp
COPY logo.jpg /app/
RUN  pip install /tmp/balance_coop-*-py3-none-any.whl &&\
     rm /tmp/balance_coop-*-py3-none-any.whl
CMD  ["balance-coop"]
