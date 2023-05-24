def maskarray(file: str, xmin: float, xmax: float, ymin: float, ymax: float) -> np.ndarray:
    """
    Masks an xarray dataset based on longitude and latitude ranges and returns the sum of values along the 'time' dimension.
    
    Args:
        file (str): File path to the xarray dataset.
        xmin (float): Minimum longitude value for masking.
        xmax (float): Maximum longitude value for masking.
        ymin (float): Minimum latitude value for masking.
        ymax (float): Maximum latitude value for masking.
    
    Returns:
        np.ndarray: Numpy array containing the sum of values after masking along the 'time' dimension.
    """
    xds_i = xr.open_dataset(file)
    mask_lon_i = (xds_i.lon >= xmin) & (xds_i.lon <= xmax)
    mask_lat_i = (xds_i.lat >= ymin) & (xds_i.lat <= ymax)
    clipped_i = xds_i.where(mask_lon_i & mask_lat_i, drop=True)
    xds_i_sum = clipped_i.sum(skipna=True, dim='time').drop_vars(names='crs', errors='ignore')
    
    nparr = xds_i_sum.to_array().values                     
    return nparr



def arrToRast(np_arr: np.ndarray, res: float, display: bool = True) -> None:
    """
    Creates a raster from a numpy array using arcpy.

    Args:
        np_arr (np.ndarray): Numpy array to be converted to a raster.
        res (float): Resolution of the raster.
        display (bool, optional): Flag to add the output raster to the map display. Defaults to True.

    Returns:
        None
    """
    wgs = arcpy.SpatialReference('WGS 1984')  # create an arcpy spatial reference
    arcpy.env.addOutputsToMap = display
    rast_arr = arcpy.NumPyArrayToRaster(np_arr, ll, res, res, 0)  # convert numpy array to arcpy raster

    arcpy.management.DefineProjection(rast_arr, wgs)  # set the coordinate reference system (CRS) of the new raster

    if 'rain' in str(os.getcwd()).lower():
        nm = '_Rain.tif'
    else:
        nm = '_Drought.tif'
    rast_arr.save(os.path.join(os.getcwd(), mt_i + nm))  # save the raster
    del rast_arr
    
    
def flipyflip(nparr: np.ndarray) -> np.ndarray:
    """
    Flips a numpy array twice.

    Args:
        nparr (np.ndarray): Numpy array to be flipped.

    Returns:
        np.ndarray: Flipped numpy array.
    """
    np_xarr_fl = np.flip(np.flip(nparr, 2), 2)
    return np_xarr_fl