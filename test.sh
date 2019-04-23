#!/usr/bin/env bash

token=YOUR_TOKEN
repo=username/your-repo

upload_url=$(curl -s -H "Authorization: token $token"  \
     -d '{"tag_name": "test", "target_commitish":"master","name":"release-0.0.1","body":"this is a test release"}'  \
     "https://api.github.com/repos/$repo/releases" | jq -r '.upload_url')

upload_url="${upload_url%\{*}"

echo "uploading asset to release to url : $upload_url"

curl -s -H "Authorization: token $token"  \
        -H "Content-Type: application/zip" \
        --data-binary @test.zip  \
        "$upload_url?name=test.zip&label=some-binary.zip"
