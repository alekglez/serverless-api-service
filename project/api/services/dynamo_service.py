# -*- coding: utf-8 -*-

import os
from typing import Any, Dict, Iterable, List, Tuple

import boto3

from project.api.services.base import Service


class DynamoService(Service):
    def __init__(self):
        self.resource = boto3.resource("dynamodb", region_name=os.getenv("REGION"))

    def get_records(self, model: str, filters: List[Tuple], fields: List[str],
                    offset: Any = None, limit: int = 20) -> Iterable:

        args = {
            "TableName": model,
            "Select": "ALL_ATTRIBUTES" if not fields else "SPECIFIC_ATTRIBUTES",
            "ReturnConsumedCapacity": "TOTAL",
            "Limit": limit
        }

        if offset:
            args["ExclusiveStartKey"] = {"id": {"S": offset}}

        if fields:
            args["ProjectionExpression"] = fields

        return self.resource.Table(model).scan(**args)["Items"]

    def get_record(self, model: str, record_id: Any, **kwargs) -> Any:
        return self.resource.Table(model).get_item(
            Key={"id": record_id}
        )["Item"]

    def create_record(self, model: str, record_id: Any, record_values: Dict):
        self.resource.Table(model).put_item(Item=record_values)

    def update_record(self, model: str, record_id: Any, record_values: Dict):
        update_expression = 'SET {}'.format(','.join(f'#{k}=:{k}' for k in record_values))
        expression_attribute_values = {f':{k}': v for k, v in record_values.items()}
        expression_attribute_names = {f'#{k}': k for k in record_values}

        response = self.resource.Table(model).update_item(
            TableName=model,
            Key={'{}'.format("id"): record_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW"
        )

        return response

    def delete_record(self, model: str, record_id: Any):
        self.resource.Table(model).delete_item(Key={"id": record_id})
