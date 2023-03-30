# digital-ecommerce

[![codecov](https://codecov.io/gh/GaniyevUz/digital-ecommerce/branch/master/graph/badge.svg?token=IPVIFRXEMB)](https://codecov.io/gh/GaniyevUz/digital-ecommerce)

An e-commerce platform with online shop creation, user-friendly dashboard, and a customizable Telegram bot for real-time updates and customer communication.
## TODO - Required

1. [ ] server
2. [x] github
3. [ ] github actions
4. [ ] test (pytest coverage 80% ^)
5. [ ] docker/docker compose
6. [ ] elasticsearch
7. [x] sentry
8. [x] security
9. [x] custom admin

## Don't Required

1. [ ] cache
2. [x] celery
3. [x] redis
4. [ ] rabbitmq
5. [ ] cron

## NOTE - For teammates

- _Don't forget write tests your codes_
- _Test files must be_ `tests/test_*.py`

## Makefile
- ```make mig``` makemigrations & migrate 
- ```make unmig``` delete migrations files 
- ```make admin``` create admin superuser
- ```make data``` collect all datas
