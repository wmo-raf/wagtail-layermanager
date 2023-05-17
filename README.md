# GeoMapViewer Manager

Wagtail based Geospatial data Manager and backend CMS for [geomapviewer-ui](https://github.com/wmo-raf/geomapviewer-ui)

# Background

National Meteorological and Hydrological Services (NMHSs) usually use, produce and disseminate data and information that
is Geo-referenced. This can range from forecast model outputs, earth observation data, stations observation datasets,
periodic bulletins and advisories and so on. Usually these are shared on their websites and social medias in static
formats, mostly PNGs.

This project is an initiative by the [WMO RAF](https://github.com/wmo-raf), as part of the Digital Transformation
Package for the NMHSs in Africa, to provide an interactive system for managing and publishing Geo-referenced (GIS)
datasets.

As the NMHSs produce and share their products in static formats, they can also use packages like this, to make their
data interactive.

# Features

All the raster and vector datasets uploaded must have time associated with each file. For netCDF files with time
dimension, time is automatically extracted from the file. For Geotiff, each uploaded file is manually assigned time.

Data management and visualization

- Uploading and visualization of gridded data
    - netCDF
    - Geotiff
- Uploading and visualization of vector data
    - Shapefiles
    - Geojson
- Raster Tile serving of raster data using [django-large-image](https://github.com/girder/django-large-image).
  All `django-large-image`features are available
- Vector tile serving using PostGIS MVT Tiles

MapViewer Management

- Management of layers visualized on the [geomapviewer-ui](https://github.com/wmo-raf/geomapviewer-ui)
    - Control on visibility (public or private) of layers on the MapViewer

# Installation

### Prerequisite

Before installing this package, you should make sure you have GDAL installed in your system.

`TIP:` Installing GDAL can be notoriously difficult. You can use pre-built Python wheels with the GDAL binary bundled,
provided by [KitWare](https://github.com/Kitware), for easy installation in production linux environments.

To install GDAL using KitWare GDAL wheel, use:

```shell
  pip install --find-links https://girder.github.io/large_image_wheels GDAL
```

Other required packages that you will need to install, if not installed already in your Wagtail Project

- psycopg2 - for postgres/postgis database connection
- wagtail_adminsortable - is also required, but the latest pip version is not compatible with the latest Wagtail
  versions. You can install the updated version that is compatible from Github using:

```shell
pip install https://github.com/Lh4cKg/wagtail-admin-sortable/archive/baa0d1f13a6bca4cc60e0d7dcd0522ecafcf5d67.zip
```

### Installation

You can install the package using pip:

```shell
pip install wagtail-geomanager
```

The following packages will be automatically installed when installing `wagtail-geomanager`, if not already installed.

- wagtail>=4.2.2
- django_extensions>=3.2.1
- django-countries>=7.5.1
- wagtail_color_panel>=1.4.1
- django_json_widget>=1.1.1
- django_nextjs>= 2.2.2
- django-allauth>=0.54.0
- django-large-image>=0.9.0
- large-image-source-gdal>=1.20.6
- large-image-source-pil>=1.20.6
- large-image-source-tiff>=1.20.6
- django-filter>=22.1
- geopandas>=0.12.2
- cftime>=1.6.2
- netCDF4>=1.6.3
- rasterio>=1.3.6
- rio-cogeo>=3.5.1
- xarray>=2023.3.0
- rioxarray>=0.14.0
- shapely>=2.0.1
- djangorestframework-simplejwt>=5.2.2
- wagtail-humanitarian-icons>=1.0.3
- matplotlib>=3.7.1

# Usage

Make sure the following are all added to your `INSTALLED_APPS` in your Wagtail `settings`

````python
INSTALLED_APPS = [
    ...

    "geomanager",
    "django_large_image",
    'django_json_widget',
    'django_nextjs',
    "django_filters",
    "wagtail_color_panel",
    "wagtail_adminsortable",
    "wagtailhumanitarianicons",
    "django_countries",
    "django_extensions",
    "allauth",
    "allauth.account",
  
    "wagtail.contrib.modeladmin",
    "rest_framework",
    "django.contrib.gis",

    ...
]

````

Run migrations

```shell
python manage.py migrate geomanager
```

Add the following to your project's `urls.py`

```python
urlpatterns = [
    ...
    path("", include("geomanager.urls")),
    ...
]
```


# Including the Map Viewer
This package is the backend component to the frontend [geomapviewer-ui](https://github.com/wmo-raf/geomapviewer-ui).


# Documentation

TODO
