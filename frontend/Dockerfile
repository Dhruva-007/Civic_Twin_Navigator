# Civic Twin Navigator - Frontend Dockerfile
# Multi-stage build for Google Cloud Run
# Stage 1: Build React app with Vite
# Stage 2: Serve with Nginx

# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first (better layer caching)
COPY package.json package-lock.json ./

# Install all dependencies
RUN npm ci --silent

# Copy ALL source files including .env.production
# .env.production is NOT committed to git (.gitignore blocks it)
# but IS included in the Cloud Build source upload via .gcloudignore.
# Vite reads it automatically during build to inject VITE_* variables.
COPY . .

# Build the React application
# Vite reads .env.production at build time and bakes VITE_* vars into the bundle
RUN npm run build

# Verify build output exists
RUN ls -la dist/

# Stage 2: Serve with Nginx
FROM nginx:alpine AS production

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built React app from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Create non-root user for security
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /usr/share/nginx/html \
    && chown -R appuser:appuser /var/cache/nginx \
    && chown -R appuser:appuser /var/log/nginx \
    && touch /var/run/nginx.pid \
    && chown -R appuser:appuser /var/run/nginx.pid

USER appuser

# Cloud Run uses port 8080
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:8080/health || exit 1

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
