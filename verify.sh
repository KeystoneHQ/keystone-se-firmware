#!/bin/bash
docker build -t firmware .
docker run -it -v ./artifacts:/app/artifacts firmware