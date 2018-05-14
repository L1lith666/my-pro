import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

pro_bucket = s3.Bucket('pro.wolil.myinstance.com')
build_bucket = s3.Bucket('probuild.wolil.myinstance.com')
pro_zip = StringIO.StringIO()
build_bucket.download_fileobj('probuild.zip', pro_zip)

with zipfile.ZipFile(pro_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        pro_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        pro_bucket.Object(nm).Acl().put(ACL='public-read')
