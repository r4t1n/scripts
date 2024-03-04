#!/bin/bash

default_cdn="us"

if [ $# -eq 0 ]; then
    echo "Usage: $0 [--cdn <CDN>] <NVIDIA Driver Version> [installer arguments]"
    exit 1
fi

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --cdn)
            cdn="$2"
            shift
            shift
            ;;
        *)
            version="$1"
            shift
            break
            ;;
    esac
done

if [ -z "$cdn" ]; then
    cdn="$default_cdn"
fi

url="https://${cdn}.download.nvidia.com/XFree86/Linux-x86_64/${version}/NVIDIA-Linux-x86_64-${version}.run"
wget "$url"

chmod +x NVIDIA-Linux-x86_64-${version}.run
./NVIDIA-Linux-x86_64-${version}.run "$@"
