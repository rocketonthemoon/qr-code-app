# 1. Dependencies stage
FROM node:22-alpine AS deps
RUN apk update && \
  apk upgrade --no-cache && \
  apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

# 2. Builder stage
FROM node:22-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

RUN npm run build

# 3. Runner stage (Standard Alpine with full shell and upgraded packages)
FROM node:22-alpine AS runner
WORKDIR /app

# Upgrade all base OS packages to patch any Alpine CVEs
RUN apk update && \
  apk upgrade --no-cache

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Create a dedicated non-root user and group
RUN useradd -r -s /bin/false appuser && chown -R appuser:appuser /app

# Copy standalone build artifacts with proper ownership
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/healthcheck.js ./healthcheck.js

# Switch to the non-root user
USER appuser

EXPOSE 3000

# Exec-format health check using the local healthcheck.js file
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD ["node", "healthcheck.js"]

# Run the standalone Next.js server directly
CMD ["node", "server.js"]