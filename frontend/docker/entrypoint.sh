#!/usr/bin/env sh

# Replace environment variables in built JS files
sed -i "s#%%VITE_API_BASE_URL%%#${VITE_API_BASE_URL}#g" /usr/share/nginx/html/assets/*.js
sed -i "s#%%VITE_MAX_FILE_SIZE_MB%%#${VITE_MAX_FILE_SIZE_MB}#g" /usr/share/nginx/html/assets/*.js
sed -i "s#%%VITE_POLLING_INTERVAL_MS%%#${VITE_POLLING_INTERVAL_MS}#g" /usr/share/nginx/html/assets/*.js
sed -i "s#%%VITE_USE_MOCKS%%#${VITE_USE_MOCKS}#g" /usr/share/nginx/html/assets/*.js

exec /docker-entrypoint.sh "$@"