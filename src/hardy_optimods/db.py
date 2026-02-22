from sqlmodel import SQLModel, Field, Session, create_engine, select


class TestTable(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str


engine = create_engine(
    "postgresql+psycopg://username:password@postgres:5432/default_database",
    echo=True,
)

# テーブル作成
SQLModel.metadata.create_all(engine)

# insert + select
with Session(engine) as session:
    session.add(TestTable(id=1, name="test"))
    session.commit()

    result = session.exec(select(TestTable)).all()
    print(result)
