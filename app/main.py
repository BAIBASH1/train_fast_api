from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.app_components.admin import setup_admin_panel
from app.app_components.instrumentation import setup_instrumentation
from app.app_components.middleware import setup_middleware
from app.app_components.redis_cache import init_cache
from app.app_components.routes import include_routers
from app.app_components.sentry import init_sentry
from app.app_components.versioning import init_versioned_fastapi

app = FastAPI()

# Инициализация Sentry
init_sentry()

# Инициализация кэша
init_cache()

# Добавление роутеров
include_routers(app)

# Настройка мидлвари
setup_middleware(app)

# версионирование
app = init_versioned_fastapi(app)

app.mount(path="/static", app=StaticFiles(directory="app/static"), name="static")

# Настройка метрик
setup_instrumentation(app)

# Настройка административной панели
setup_admin_panel(app)
