#!/bin/bash

./manage.py collectstatic --noinput
gcloud app deploy
gcloud app logs tail -s default
