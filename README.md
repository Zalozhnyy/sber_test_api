# sber_test_api


Развёртывание приложения
========================
### Swagger
документация доступна по адресу `/api/doc`
### Сборка
    docker build -t sber_tz .

### Запуск
    docker run -p 8080:8080 sber_tz

## Сборка prod версии
    docker-compose up --build -d

контейнер nginx ports 8889->80

### Проверка
    postman http://0.0.0.0:8080/
Указываем body json
    `{
    "date": "31.1.2021",
    "periods": 4,
    "amount": 10000,
    "rate": 6
    }`

Тесты
========================
    pytest --cov=app app/tests/

Запускает тесты и показывает покрытие кода

wrk
========================
тесты на локальной машине gunicorn 12 workers + nginx

`./wrk -t12 -c300 -d30s --script=sc.lua http://0.0.0.0:8889/`

    Running 30s test @ http://0.0.0.0:8889/
      12 threads and 300 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    85.65ms   41.70ms 328.15ms   67.57%
        Req/Sec   295.34    149.89     1.17k    95.46%
      106064 requests in 30.09s, 26.70MB read
    Requests/sec:   3524.31
    Transfer/sec:      0.89MB


Входные данные
========================
Формат входных данных указан в `entry_data_schema.json`
