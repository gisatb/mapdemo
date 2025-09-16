"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps, TileLayer
import ipywidgets as widgets


class Map(ipyleaflet.Map):
    """This is the map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class.
    """    

    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        """Initialize the map.

       S Args:
            center (list, optional): Set the center of the map. Defaults to [20, 0].
            zoom (int, optional): Set the zoom level of the map. Defaults to 2.
        """ 
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        # Optional controls flags
        #layer_control = kwargs.pop("layer_control", False)
        # fullscreen_control = kwargs.pop("fullscreen_control", True) 
        if "add_layers_control" not in kwargs:
            layer_control_flag = True
        
        else:
          layer_control_flag = kwargs["add_layers_control"]
        kwargs.pop("add_layers_control", None)  

        super().__init__(center=center, zoom=zoom, **kwargs)

        # Add controls based on flags
        #self.add_layers_control()
        #if layer_control: self.add_layers_control()
        # if fullscreen_control: self.add_fullscreen_control()
        if layer_control_flag:
            self.add_layers_control()
        

        # -------- Utility to remove duplicates -------- #
    def replace_control(self, control_type, new_control):
        for c in list(self.controls):
            if isinstance(c, control_type):
                self.remove_control(c)
        self.add_control(new_control)        



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


    #def add_layers_control(self, position="topright"):
    def add_layers_control(self, position="topright"):
        """Adds a layer control to the map

        Args:
            position (str, optional): The position of the layer control. Defaults to "topright".
        """        
        #self.add_control(ipyleaflet.LayersControl(position=position))
        self.replace_control(ipyleaflet.LayersControl, ipyleaflet.LayersControl(position=position))  

    
    
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

    def add_image(self, url, bounds, name="image", **kwargs):
        """Add a image overlay to the map.

        Args:
            url (str): The URL of the image
            bounds (list): The bounds of the layer
            name (str, optional): The name of the layer. Defaults to "image".
        """
        layer = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name=name, **kwargs)
        self.add(layer)

    def add_raster(self, data, name="raster",zoom_to_layer=True, **kwargs):

        try:
            from localtileserver import TileClient, get_leaflet_tile_layer
        except ImportError:
            raise ImportError("please install the localtileserver package")
        
        client =TileClient(data)
        layer=get_leaflet_tile_layer(client, name=name, **kwargs)
        self.add(layer)

        if zoom_to_layer:
            self.center=client.center()
            self.zoom=client.default_zoom


    def add_zoom_slider(self, description="Zoom level", min=0, max=18, value=4, position="topright"):
        """Addd a zoom slider to the map

        Args:
            description (str, optional): Name of the zoom slider. Defaults to "Zoom level".
            min (int, optional): Min value of zoom slider. Defaults to 0.
            max (int, optional): Max value of the zoom slider. Defaults to 18.
            value (int, optional): value of the zoom slider. Defaults to 10.
            position (str, optional): Position of the zoom slider. Defaults to "topright".
        """
        zoom_slider= widgets.IntSlider(
            description=description, min=min, max=max, value=value
        ) 

        control = ipyleaflet.WidgetControl(widget=zoom_slider, position=position)
        self.add(control)
        widgets.jslink((zoom_slider,"value"),(self,'zoom'))

    def add_widget(self,widget, position="topright"):
        """_summary_

        Args:
            widget (_type_): _description_
            position (str, optional): Position of the widget. Defaults to "topright".
        """
        control =ipyleaflet.WidgetControl(widget=widget, position=position)
        self.add(control)
        
    def add_opacity_slider(self, layer_index=-1, description="Opacity",position="topright",style={"description_width": "inital"},):
        """Add an opacity slider to the map

        Args:
            layer_index (int, optional): The layer to which the opacity slider is added. Defaults to -1.
            description (str, optional): the description of the opacity silder. Defaults to "Opacity".
            position (str, optional): The position of the opacity slider. Defaults to "topright".
        """
        layer=self.layers[layer_index]
        opacity_slider=widgets.FloatSlider(
            description=description, min=0, max=1,value=layer.opacity
        )
        
        def upadate_opacity(change):
           layer.opacity=change["new"]

        opacity_slider.observe(upadate_opacity,"value")   
        
        control =ipyleaflet.WidgetControl(widget=opacity_slider,position=position)
        self.add(control)

    def add_basemap_gui(self,basemaps=None, position="topright"):

        basemap_selector=widgets.Dropdown(
            options=[
                "OpenStreetMap",
                "OpenTopoMap",
                "Esri.WorldImagery",
                "Esri.NatGeoWorldMap",
            ],
            description="Basemap",
        )

        def update_basemap(change):
            self.add_basemap(change["new"])

        basemap_selector.observe(update_basemap,"value")

        control = ipyleaflet.WidgetControl(widget=basemap_selector, position=position)
        self.add(control)

        


