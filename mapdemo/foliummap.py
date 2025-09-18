import folium
from ipyleaflet import basemaps

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

    def add_tile_layer(self, url, name, attribution="custom tile",**kwargs):
        """Add a tile layer to the map

        Args:
            url (_type_): url of the layer
            name (_type_): _descrName of the layer added to the layeription_
            attribution (str, optional): _description_. Defaults to "custom tile".
        """        
        layer = folium.TileLayer(tiles=url, name=name, attr=attribution, **kwargs)
        layer.add_to(self)

    def add_basemap(self, name, overlay=True,**kwargs):
        """Adds a basemap to the current map

        Args:
            name (_type_): The name of the basemap as a string, or an object
        """
        if isinstance(name, str):
            try:
                provider = basemaps
                for part in name.split("."):
                    provider = getattr(provider, part)

                url = provider.build_url()
                attribution = provider.attribution

                # Add the provider as a TileLayer
                layer = folium.TileLayer(tiles=url, name=name,attr=attribution, **kwargs)
                layer.add_to(self)
            except Exception as e:
                raise ValueError(f"Basemap '{name}' not found: {e}")        
        else:
            name.add_to(self)


    def to_streamlit(self, width=700, height=500):
        """_summary_

        Returns:
            _type_: _description_
        """
        from streamlit_folium import folium_static
        return folium_static(self, width=width, height=height)
    

    def add_layer_control(self):
        """Add a layer control to the map
        
        """
        folium.LayerControl().add_to(self)
             
