FROM node:20-alpine AS frontend-build
WORKDIR /build/frontend/mini-app
COPY frontend/mini-app/package*.json ./
RUN npm ci
COPY frontend/mini-app/ ./
RUN npm run build

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080
WORKDIR /app
RUN addgroup --system deutschiq && adduser --system --ingroup deutschiq deutschiq
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/ ./backend/
COPY --from=frontend-build /build/frontend/mini-app/dist ./frontend/mini-app/dist
USER deutschiq
WORKDIR /app/backend
EXPOSE 8080
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
