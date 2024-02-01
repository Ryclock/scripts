#!/bin/bash

image_ids=$(docker images --filter "dangling=true" --format "{{.ID}}")

for image_id in $image_ids; do
    docker rmi "$image_id"
done
