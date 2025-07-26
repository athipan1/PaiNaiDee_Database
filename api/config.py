"""
Database configuration module for PaiNaiDee Database
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConfig:
    """Database configuration class"""

    def __init__(self):
        self.database_url = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/painaidee_db",
        )
        self.echo = os.getenv("DB_ECHO", "false").lower() == "true"

    def get_engine(self):
        """Get SQLAlchemy engine"""
        return create_engine(
            self.database_url,
            echo=self.echo,
            pool_pre_ping=True,  # Enable connection health checks
        )

    def get_session_local(self):
        """Get SessionLocal class"""
        engine = self.get_engine()
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Global configuration instance
db_config = DatabaseConfig()
