from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = "mysql"
    db_port: int = 3306
    db_user: str = "inventario_user"
    db_password: str = "inventario_pass"
    db_name: str = "inventario_db"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
