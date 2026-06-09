from fastapi import Depends
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter

from app.database import get_db
from app.graphql.context import GraphQLContext
from app.graphql.schema import schema


async def get_graphql_context(db: Session = Depends(get_db)) -> GraphQLContext:
    return GraphQLContext(db=db)


graphql_router = GraphQLRouter(
    schema,
    context_getter=get_graphql_context,
    graphiql=True,
)
