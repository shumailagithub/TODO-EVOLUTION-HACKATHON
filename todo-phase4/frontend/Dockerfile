# Multi-stage build for Next.js frontend application
ARG NEXT_PUBLIC_API_URL=http://localhost:8002

# Stage 1: Build stage
FROM node:18-alpine AS builder

# Set build-time environment variable
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application source code
COPY . .

# Build the Next.js application
RUN npm run build

# Stage 2: Runtime stage
FROM node:18-alpine AS runtime

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY --from=builder /app/package*.json ./

# Install only production dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy built application from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/next.config.js ./next.config.js
COPY --from=builder /app/package.json ./package.json
# Conditionally copy public directory if it exists
RUN if [ -d "/app/public" ]; then cp -r /app/public .; fi

# Switch to non-root user
USER nextjs

# Expose port 3000
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Start the application
CMD ["sh", "-c", "npm start"]