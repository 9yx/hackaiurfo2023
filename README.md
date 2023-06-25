Цифровой прорыв 2023 Екатеринбург(УФО) (23.06.2023-25.06.2023)

Датасет:
https://universe.roboflow.com/firstisfirst

Ссылка на модель:
https://disk.yandex.ru/d/a60MSoM5EfnQog

Модель(`best.pb` файл) положить в `models`

Видео в `videos`

После запуска выбрать видео из `videos`

При окончании видео (либо нажатии кнопки q) создается json

Результирующий `json` разбрать из папки `temp`

![image](https://github.com/9yx/hackaiurfo2023/assets/546223/7ce5b1a8-6b85-42ad-b72c-aaf5d21aa962)

Пример json файла: https://disk.yandex.ru/d/ul-uI1vMVsVfPw

```json
[
  {
    "id_object": 1,
    "class_object": "crane",
    "id_event": "f1f250b3-77dd-4143-a290-9bfaae1ba55f",
    "start": 0.0,
    "end": 358.2,
    "class_event": "присутствие"
  },
    {
    "id_object": 4,
    "class_object": "crane",
    "id_event": "bf0c86d7-067d-430c-be55-a0a289ac8e63",
    "start": 0.0,
    "end": 35.0,
    "class_event": "простой"
  },
]
```

```
id_object - идентификатор из трекинга
class_object - класс объекта
id_event - идентификатор эвента
start - секунда начала события от начала видео
end - секунда окончания события от начала видео
class_event - тип события (присутствие - наличие объекта в видео, простой - простой объекта в видео)
```
