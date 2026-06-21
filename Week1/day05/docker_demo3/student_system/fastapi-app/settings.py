import os

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": os.getenv("DB_HOST", "localhost"),
                "port": int(os.getenv("DB_PORT", "3306")),
                "database": os.getenv("DB_NAME", "student_system"),
                "user": os.getenv("DB_USER", "root"),
                "password": os.getenv("DB_PASSWORD", "123456"),
                "minsize": 1,
                "maxsize": 10,
                "charset": "utf8mb4",
                "echo": True
            }
        },
    },
    "apps": {
      "models": {
          "models": ["models"],
          "default_connection": "default",
      }
    },
    "use_tz": True,
    "timezone": "Asia/Shanghai"
}

