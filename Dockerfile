FROM node:14-slim AS frontend
COPY ./client /app/client
RUN cd /app/client; \
    npm install; \
    npm run build

FROM python:3.8-slim
RUN pip install poetry;
WORKDIR /app
COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install;
COPY ./main.py logo.jpg /app/
COPY ./api /app/api
COPY --from=frontend /app/client/dist /app/client/dist
CMD ["poetry", "run", "python", "main.py"]
