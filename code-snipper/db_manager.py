import sqlite3
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    TIMESTAMP,
    create_engine,
)
import sqlalchemy.engine.url as url
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    relationship,
    sessionmaker
)


class Base(DeclarativeBase):
    created_ts = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    updated_ts = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")


# Association table for many-to-many relationship between snippets and tags
snippet_tag_table = Table(
    "snippet_tags",
    Base.metadata,
    Column("snippet_id", Integer, ForeignKey("snippets.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Folder(Base):
    __tablename__ = "folders"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    snippets = relationship("Snippet", back_populates="folder")

    def __repr__(self):
        return f"Folder(id={self.id!r}, name={self.name!r})"


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return f"Tag(id={self.id!r}, name={self.name!r})"


class Snippet(Base):
    __tablename__ = "snippets"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    folder_id = Column(Integer, ForeignKey("folders.id"))
    folder = relationship("Folder", back_populates="snippets")

    def __repr__(self):
        return f"Snippet(id={self.id!r}, name={self.name!r})"


class Fragment(Base):
    __tablename__ = "fragments"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    language = Column(String(127))
    snippet_id = Column(Integer, ForeignKey("snippets.id"))

    def __repr__(self):
        return f"Fragment(id={self.id!r}, content={self.content!r})"


class DBManager:
    def __init__(self, db_name):
        self.engine = create_engine(f"sqlite:///{db_name}")
        Base.metadata.create_all(self.engine)
        self.__Session = sessionmaker(bind=self.engine)
        self.session = self.__Session()

    def init_db(self):
        pass
        # Initialize the database schema here
        # self.connection.execute(
        #     """CREATE TABLE IF NOT EXISTS folders (
        #                             id INTEGER PRIMARY KEY,
        #                             name VARCHAR(255) NOT NULL,
        #                             created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        #                             updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
        # )

        # self.connection.execute(
        #     """CREATE TABLE IF NOT EXISTS tags (
        #                             id INTEGER PRIMARY KEY,
        #                             name VARCHAR(255) NOT NULL,
        #                             created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        #                             updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
        # )

        # self.connection.execute(
        #     """CREATE TABLE IF NOT EXISTS snippets (
        #                             id INTEGER PRIMARY KEY,
        #                             name VARCHAR(255) NOT NULL,
        #                             folder_id INTEGER,
        #                             created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        #                             updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        #                             FOREIGN KEY (folder_id) REFERENCES folders (id))"""
        # )

        # self.connection.execute(
        #     """CREATE TABLE IF NOT EXISTS fragments (
        #                             id INTEGER PRIMARY KEY,
        #                             content VARCHAR(255) NOT NULL,
        #                             snippet_id INTEGER,
        #                             created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        #                             updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        #                             FOREIGN KEY (snippet_id) REFERENCES snippets (id))"""
        # )

        # self.connection.execute(
        #     """CREATE TABLE IF NOT EXISTS snippet_tags (
        #                             snippet_id INTEGER,
        #                             tag_id INTEGER,
        #                             created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        #                             updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        #                             FOREIGN KEY (snippet_id) REFERENCES snippets (id),
        #                             FOREIGN KEY (tag_id) REFERENCES tags (id),
        #                             PRIMARY KEY (snippet_id, tag_id))"""
        # )

    def commit(self):
        # self.connection.commit()
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        # self.connection.close()
        self.engine.dispose()
