import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:eu-west-1:211335235430:deployProTopic')

    try:

        s3 = boto3.resource('s3')

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
        topic.publish(Subject="Pro deployed", Message="Pro Deployed successfully")
    except:
        topic.publish(Subject="Pro deployment failed!", Message="Pro not deployed successfully")
        raise
    return 'Hello from Lambda'
