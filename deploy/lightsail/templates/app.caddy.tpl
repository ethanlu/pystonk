__APP_DOMAIN__ {
    encode zstd gzip

    header {
        Referrer-Policy "strict-origin-when-cross-origin"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
    }

    reverse_proxy 127.0.0.1:__APP_PORT__
}
