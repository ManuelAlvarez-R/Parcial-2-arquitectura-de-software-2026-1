import strawberry
from graphql import GraphQLError
from pydantic import ValidationError
from strawberry.schema.config import StrawberryConfig

from app.exceptions import AlmacenNoEncontradoError
from app.graphql.context import GraphQLContext
from app.graphql.types import (
    InventarioItemType,
    InventarioPorSedeType,
    ProductoType,
    RegistroInventarioInput,
    RegistroInventarioResult,
    AlmacenType,
)
from app.schemas.inventario import RegistroInventarioRequest
from app.services.inventario_service import InventarioService


@strawberry.type
class Query:
    @strawberry.field(description="Obtiene productos y cantidades de una sede de almacén")
    def inventario_por_sede(
        self, info: strawberry.Info[GraphQLContext, None], sede_id: int
    ) -> InventarioPorSedeType:
        service = InventarioService(info.context.db)
        try:
            resultado = service.obtener_inventario_por_sede(sede_id)
        except AlmacenNoEncontradoError as error:
            raise GraphQLError(str(error)) from error

        return InventarioPorSedeType(
            almacen=AlmacenType.from_model(resultado.almacen),
            items=[
                InventarioItemType(
                    producto=ProductoType.from_model(item.producto),
                    cantidad=item.cantidad,
                )
                for item in resultado.items
            ],
        )


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Registra un producto en el inventario de un almacén")
    def registrar_producto(
        self,
        info: strawberry.Info[GraphQLContext, None],
        datos: RegistroInventarioInput,
    ) -> RegistroInventarioResult:
        service = InventarioService(info.context.db)
        try:
            request = RegistroInventarioRequest.model_validate(datos.__dict__)
        except ValidationError as error:
            raise GraphQLError(error.errors()[0]["msg"]) from error

        resultado = service.registrar_producto_en_inventario(request)

        return RegistroInventarioResult(
            mensaje=resultado.mensaje,
            producto=ProductoType.from_model(resultado.producto),
            almacen=AlmacenType.from_model(resultado.almacen),
            cantidad=resultado.cantidad,
        )


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=True),
)
