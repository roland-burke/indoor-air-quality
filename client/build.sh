#!/bin/bash
export NODE_OPTIONS=--openssl-legacy-provider
npm run build
cp -r dist/* backend/static/
echo "done"