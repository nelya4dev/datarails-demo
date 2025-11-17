FROM node:24.10.0-alpine3.21 as build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY public                 ./public
COPY src                    ./src
COPY .env.container         ./.env
COPY components.json        ./components.json
COPY eslint.config.js       ./eslint.config.js
COPY index.html             ./index.html
COPY postcss.config.js      ./postcss.config.js
COPY tailwind.config.js     ./tailwind.config.js
COPY tsconfig.app.json      ./tsconfig.app.json
COPY tsconfig.json          ./tsconfig.json
COPY tsconfig.node.json     ./tsconfig.node.json
COPY vite.config.ts         ./vite.config.ts

RUN npm run build:no-typecheck

FROM nginx:1.27.4-alpine3.21
RUN apk update && apk upgrade && apk add --no-cache sed

COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy built app
COPY --from=build /app/dist /usr/share/nginx/html

# Create non-root user
RUN addgroup -S nginxuser && adduser -S -G nginxuser -u 1000 -s /sbin/nologin nginxuser

# Set permissions
RUN chown -R nginxuser:nginxuser /usr/share/nginx/html && \
    chown -R nginxuser:nginxuser /var/cache/nginx && \
    chown -R nginxuser:nginxuser /var/log/nginx && \
    chown -R nginxuser:nginxuser /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginxuser:nginxuser /var/run/nginx.pid

USER nginxuser

ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
EXPOSE 80