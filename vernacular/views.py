from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from typing import List, Dict, Callable, Tuple

SlotValidationResult = Tuple[bool, bool, str, Dict]

def validate_finite_values_entity(values: List[Dict], supported_values: List[str] = None,
                                invalid_trigger: str = None, key: str = None,
                                support_multiple: bool = True, pick_first: bool = False, **kwargs) -> SlotValidationResult:

    filled = False
    partially_filled = False
    trigger = True
    parameters = {}
    key_modifier = True

    invalid_count = 0
    total = len(values)

    if not total == 0:
        for val_dict in values:
            if (val_dict["entity_type"] in kwargs['type']) and (val_dict["value"] in supported_values):
                if pick_first and key_modifier:
                    parameters[key] = val_dict["value"].upper()
                    key_modifier = False
                elif support_multiple and key_modifier:
                    if key in parameters:
                        parameters[key].append(val_dict["value"].upper())
                    else:
                        parameters[key] = []
                        parameters[key].append(val_dict["value"].upper())

            else:
                invalid_count+=1
        
        if invalid_count == 0:
            filled = True
            trigger = False
        else:
            parameters = {}
            partially_filled = True
            trigger = True

    trig = invalid_trigger if trigger else ""
    return (filled, partially_filled, trig, parameters)

def validate_numeric_entity(values: List[Dict], invalid_trigger: str = None, key: str = None,
                            support_multiple: bool = True, pick_first: bool = False, constraint=None, var_name=None,
                            **kwargs) -> SlotValidationResult:
    filled = False
    partially_filled = False
    trigger = True
    parameters = {}
    key_modifier = True

    invalid_count = 0
    total = len(values)
    if (constraint is None) or (constraint == ""):
        constraint = "True"

    if not total == 0:
        for val_dict in values:
            exec("%s = %d" % (var_name,val_dict["value"]))
            if (val_dict["entity_type"] in kwargs['type']) and eval(constraint):#(val_dict["value"] in supported_values):
                if pick_first and key_modifier:
                    parameters[key] = val_dict["value"]
                    key_modifier = False
                elif support_multiple and key_modifier:
                    if key in parameters:
                        parameters[key].append(val_dict["value"])
                    else:
                        parameters[key] = []
                        parameters[key].append(val_dict["value"])

            else:
                invalid_count+=1
        
        if invalid_count == 0:
            filled = True
            trigger = False
        else:
            partially_filled = True
            trigger = True

    trig = invalid_trigger if trigger else ""
    return (filled, partially_filled, trig, parameters)

class finitevalues(APIView):

    def post(self, request):
        try:
            data = request.data
            response = validate_finite_values_entity(**data)
            return Response(response, status.HTTP_201_CREATED)
        
        except Exception as exe:
            print(exe)
            content = {
                "message":"ERROR"
            }
            return Response(content, status.HTTP_500_INTERNAL_SERVER_ERROR)

class numeric(APIView):

    def post(self, request):
        try:
            data = request.data
            response = validate_numeric_entity(**data)
            return Response(response, status.HTTP_201_CREATED)
        except Exception as exe:
            print(exe)
            content = {
                "message":"ERROR"
            }
            return Response(content, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
