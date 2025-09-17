import folium

class Map(folium.Map):

    def __init__(self, center=[20, 0], zoom= 2, **kwargs):
        super().__init__(location=center, zoom_start=zoom , **kwargs)


    def add_raster(self, data, name="raster", **kwargs):
        """Add raster layer to the map using tileserver 

        Args:
            data (_type_): Raster data
            name (str, optional): Name of the raster layer. Defaults to "raster".
            zoom_to_layer (bool, optional): zoom to the layer which one added. Defaults to True.

        Raises:
            ImportError: package not found
        """
        try:
            from localtileserver import TileClient, get_folium_tile_layer
        except ImportError:
            raise ImportError("please install the localtileserver package")
        
        client =TileClient(data)
        layer=get_folium_tile_layer(client, name=name, **kwargs)
        layer.add_to(self)
