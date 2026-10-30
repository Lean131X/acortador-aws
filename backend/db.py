import os
import boto3
from dotenv import load_dotenv

load_dotenv()

region = os.getenv("AWS_REGION", "us-east-1")
nombre_tabla = os.getenv("TABLE_NAME", "urls")

# no hay claves aqui, boto3 usa el rol IAM de la EC2
dynamodb = boto3.resource("dynamodb", region_name=region)
tabla = dynamodb.Table(nombre_tabla)