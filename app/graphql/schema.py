import strawberry
from graphql import GraphQLError
from pydantic import ValidationError
from strawberry.schema.config import StrawberryConfig

from app.exceptions import AlmacenNoEncontradoError
from app.graphql.context import GraphQLContext
from app.graphql.types import (
    AlmacenType,
    InventarioItemType,
    InventarioPorSedeType,
    ProductoType,
    RegistroAlmacenInput,
    RegistroAlmacenResult,
    RegistroInventarioInput,
    RegistroInventarioResult,
)
from app.schemas.inventario import RegistroAlmacenRequest, RegistroInventarioRequest
from app.services.inventario_service import InventarioService


@strawberry.type
class Query:
    @strawberry.field(description="Lista todas las sedes de almacén registradas")
    def almacenes(self, info: strawberry.Info[GraphQLContext, None]) -> list[AlmacenType]:
        service = InventarioService(info.context.db)
        return [AlmacenType.from_model(almacen) for almacen in service.listar_almacenes()]

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
    @strawberry.mutation(description="Crea o actualiza una sede de almacén")
    def registrar_almacen(
        self,
        info: strawberry.Info[GraphQLContext, None],
        datos: RegistroAlmacenInput,
    ) -> RegistroAlmacenResult:
        service = InventarioService(info.context.db)
        try:
            request = RegistroAlmacenRequest.model_validate(datos.__dict__)
        except ValidationError as error:
            raise GraphQLError(error.errors()[0]["msg"]) from error

        resultado = service.registrar_almacen(request)

        return RegistroAlmacenResult(
            mensaje=resultado.mensaje,
            almacen=AlmacenType.from_model(resultado.almacen),
        )

    @strawberry.mutation(description="Registra un producto en el inventario de un almacén existente")
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

        try:
            resultado = service.registrar_producto_en_inventario(request)
        except AlmacenNoEncontradoError as error:
            raise GraphQLError(str(error)) from error

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
