FROM node:18 AS build-frontend

ARG BUILD_MODE=production
ARG LAUNCH_MODE=production
ARG APP_VERSION=dev

ENV MODE=${LAUNCH_MODE}
ENV VITE_APP_VERSION=${APP_VERSION}

WORKDIR /app
ADD ./frontend/package.json ./frontend/pnpm-lock.yaml /app/
RUN npm i -g pnpm && pnpm install
ADD ./frontend /app
RUN pnpm build --mode ${BUILD_MODE}


FROM nginx:1.21

ADD ./deployment/nginx.conf /etc/nginx/conf.d/default.conf
ADD --chmod=+x ./deployment/docker_entrypoint.sh /docker_entrypoint.sh
COPY --from=build-frontend /app/dist /usr/share/nginx/html


# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
# ARG APP_VERSION=dev
# ENV APP_VERSION=${APP_VERSION}
# ENV APP_NAME=keystore
# ENV APP_MODULE=${APP_NAME}.routes.base:app

# COPY ./backend/requirements.txt /app/
# RUN pip install -U -r /app/requirements.txt

# COPY ./backend/alembic.ini /alembic.ini
# COPY ./backend/logging_prod.conf /app/
# COPY ./backend/logging_test.conf /app/
# COPY ./backend/migrations /migrations/

# COPY --from=build-frontend /app/dist /app/static/ui
# COPY ./backend/${APP_NAME} /app/${APP_NAME}
