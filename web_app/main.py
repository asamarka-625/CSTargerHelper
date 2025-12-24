# Внешние зависимости
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
# Внутренние модули
from web_app.src.core import cfg, engine, setup_database
from web_app.src.admin import (UserAdmin, MapAdmin, CategoryAdmin, CardAdmin, CardImageAdmin,
                               authentication_backend)


async def startup():
    cfg.logger.info("Запускаем приложение...")
    await setup_database()


async def shutdown():
    cfg.logger.info("Останавливаем приложение...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup логика
    await startup()
    yield
    # Shutdown логика
    await shutdown()


app = FastAPI(lifespan=lifespan)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Админка
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(MapAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(CardAdmin)
admin.add_view(CardImageAdmin)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', port=8000, reload=False)