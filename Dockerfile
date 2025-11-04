# Build stage
FROM golang:1.25-alpine AS builder

# Install build dependencies
RUN apk add --no-cache git ca-certificates

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the application
ARG VERSION=dev
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-s -w -X main.version=${VERSION}" \
    -o githubrel \
    ./cmd/githubrel

# Runtime stage
FROM alpine:latest

# Install ca-certificates for HTTPS requests
RUN apk --no-cache add ca-certificates

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/githubrel /usr/local/bin/githubrel

# Create non-root user
RUN addgroup -g 1000 githubrel && \
    adduser -D -u 1000 -G githubrel githubrel && \
    chown -R githubrel:githubrel /app

USER githubrel

# Expose MCP server port
EXPOSE 8556

# Set default command to run MCP server
ENTRYPOINT ["githubrel"]
CMD ["mcp"]
