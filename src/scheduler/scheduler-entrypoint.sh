#!/bin/sh

celery -A scheduler beat -l info --detach &

celery -A scheduler worker -l info