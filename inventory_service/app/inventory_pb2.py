# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: inventory.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0finventory.proto\x12\tinventory\"y\n\x0fInventory_Proto\x12\x12\n\nproduct_id\x18\x01 \x01(\x05\x12\x10\n\x08quantity\x18\x02 \x01(\x05\x12\x13\n\x0blocation_id\x18\x03 \x01(\x05\x12+\n\x08location\x18\x04 \x01(\x0b\x32\x19.inventory.Location_Proto\"m\n\x0eLocation_Proto\x12\x15\n\rlocation_name\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\x12\x33\n\x0finventory_items\x18\x03 \x03(\x0b\x32\x1a.inventory.Inventory_Protob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'inventory_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _INVENTORY_PROTO._serialized_start=30
  _INVENTORY_PROTO._serialized_end=151
  _LOCATION_PROTO._serialized_start=153
  _LOCATION_PROTO._serialized_end=262
# @@protoc_insertion_point(module_scope)
