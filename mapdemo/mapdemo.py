"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps, TileLayer


class Map(ipyleaflet.Map):
    """This is the map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class.
    """    

    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        """Initialize the map.

        Args:
            center (list, optional): Set the center of the map. Defaults to [20, 0].
            zoom (int, optional): Set the zoom level of the map. Defaults to 2.
        """        
        super().__init__(center=center, zoom=zoom, **kwargs)
        

    def add_tile_layer(self, url, name, **kwargs):
        """Add a layer to the map

        Args:
            url (_type_): url of the layer
            name (_type_): Name of the layer added to the layer
        """        
        layer = ipyleaflet.Tilelayer(url=url, name=name, **kwargs)
        self.add(layer)


    def add_basemap(self, name,**kwargs):
        """Adds a basemap to the current map

        Args:
            name (str or object): The name of the basemap as a string, or an object

        Raises:
            ValueError: Basemap not found
        """
        #if isinstance(name, str):
        #   url=eval(f"basemaps.{name}").build_url()
        #   self.add_tile(url, name)
        #else:
        #   self.add(name)
        if isinstance(name, str):
            try:
                provider = basemaps
                for part in name.split("."):
                    provider = getattr(provider, part)

                url = provider.build_url()
                attribution = provider.attribution

                # Add the provider as a TileLayer
                layer = TileLayer(url=url, name=name,attribution=attribution, **kwargs)
                self.add(layer)
            except Exception as e:
                raise ValueError(f"Basemap '{name}' not found: {e}")        
        else:
            self.add(name)


    def add_layers_control(self, position="topright"):
        """Adds a layer control to the map

        Args:
            position (str, optional): The position of the layer control. Defaults to "topright".
        """        
        self.add_control(ipyleaflet.LayersControl(position=position))  

    
    def add_geojson(self, data, name="geojson", **kwargs):
        """Adds a GeoJSON layer to the map

        Args:
            data (str, dict): GeoJSON Data as a string or a dictionary
            name (str, optional): The name of the layer. Defaults to "geojson".
        """
        import json

        if isinstance(data, str):
            with open(data) as f:
                data = json.load(f)

        if "style" not in kwargs:
            kwargs['style'] = {'color':'blue','weight':1,'fillOpacity':0}

        if "hover_style"  not in kwargs:
            kwargs["hover_style"] =  {'fillColor': 'blue', 'fillOpacity': 0.5} 

        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add(layer)

    
    def add_shp(self, data, name="shp", **kwargs):
        """Adds a shapefile to the map

        Args:
            data (shp): Shapefile data as a shp
            name (str, optional): THe name of shapefile . Defaults to "shp".
        """        
        import shapely#shapefile
        import json 

        if isinstance(data, str):
            with shapely.Reader(data) as shp:
                data = shp.__geo_interface__

        #if "style" not in kwargs:
           # kwargs['style'] = {'color':'blue','weight':1,'fillOpacity':0}

       # if "hover_style"  not in kwargs:
           # kwargs["hover_style"] =  {'fillColor': 'blue', 'fillOpacity': 0.5} 

        #layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        #self.add(layer)
        self.add_geojson(data, name, **kwargs)
