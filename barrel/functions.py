import netCDF4 as nc
import boto3 as boto
import gzip as gzip
from io import BytesIO

class Functions:
	def __init__(self):
		print("RainBarrel initialized...")

	@staticmethod
	def collect_from_bucket(year, month, day, latitude, longitude):
		from botocore.handlers import disable_signing
		s3_resource = boto.resource('s3')
		s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

		zip_obj = s3_resource.Object(bucket_name="noaa-ghe-pds", key=f"rain_rate/{year}/{month}/{day}/NPR.GEO.GHE.v1.S{year}{month}{day}0615.nc.gz")
		buffer = BytesIO(zip_obj.get()["Body"].read())
		
		dataset_new = nc.Dataset('empty.nc', 'w')

		with gzip.open(buffer, 'rb') as f:
		    dataset_new = nc.Dataset('rainfall_dataset', memory=f.read())

		rainfall_array = dataset_new['rain'][0:4800, 0:10020]

		# Ensure that latitude and longitude are within available range
		if (latitude < -65 or latitude > 65):
			print("Latitude out of available range.")
			return -1

		if (longitude < -180 or longitude > 180):
			print("Latitude out of valid range.")
			return -1

		# Both are now validated! Next, correct lat. and long. to begin at zero
		lat_corrected = latitude + 65
		long_corrected = longitude + 180

		# Convert coordinates into indexes (reminder - latitude is y, longitude is x)
		lat_index = int(lat_corrected / 0.02708333)
		long_index = int(long_corrected / 0.03592814)

		print("Lat index " + str(lat_index))

		# Located correct "pixel"
		measurement = rainfall_array[lat_index][long_index]
		return measurement
