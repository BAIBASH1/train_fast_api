from fastapi import FastAPI

from app.app_components.admin import setup_admin_panel
from app.app_components.instrumentation import setup_instrumentation
from app.app_components.middleware import setup_middleware
from app.app_components.redis_cache import init_cache
from app.app_components.routes import include_routers
from app.app_components.sentry import init_sentry

app = FastAPI()

# Инициализация Sentry
init_sentry()

# Инициализация кэша
init_cache()

# Настройка мидлвари
setup_middleware(app)

# Добавление роутеров
include_routers(app)

# Настройка инструментирования
setup_instrumentation(app)

# Настройка административной панели
setup_admin_panel(app)
