class AlmacenNoEncontradoError(Exception):
    def __init__(self, sede_id: int):
        self.sede_id = sede_id
        super().__init__(f"No existe un almacén con ID de sede {sede_id}")
