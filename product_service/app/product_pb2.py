# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: product.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rproduct.proto\x12\x07product\"]\n\x0e\x43\x61tegory_Proto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12(\n\x08products\x18\x03 \x03(\x0b\x32\x16.product.Product_Proto\"\x90\x02\n\rProduct_Proto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x01(\x02\x12\x11\n\tavailable\x18\x04 \x01(\x08\x12\x13\n\x0b\x63\x61tegory_id\x18\x05 \x01(\x05\x12\r\n\x05\x62rand\x18\x06 \x01(\t\x12\x0e\n\x06weight\x18\x07 \x01(\x02\x12\x0b\n\x03sku\x18\x08 \x01(\t\x12)\n\x08\x63\x61tegory\x18\t \x01(\x0b\x32\x17.product.Category_Proto\x12&\n\x07reviews\x18\n \x03(\x0b\x32\x15.product.Review_Proto\x12&\n\x07ratings\x18\x0b \x03(\x0b\x32\x15.product.Rating_Proto\"`\n\x0cReview_Proto\x12\x13\n\x0breview_text\x18\x01 \x01(\t\x12\x12\n\nproduct_id\x18\x02 \x01(\x05\x12\'\n\x07product\x18\x03 \x01(\x0b\x32\x16.product.Product_Proto\"[\n\x0cRating_Proto\x12\x0e\n\x06rating\x18\x01 \x01(\x05\x12\x12\n\nproduct_id\x18\x02 \x01(\x05\x12\'\n\x07product\x18\x03 \x01(\x0b\x32\x16.product.Product_Protob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'product_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CATEGORY_PROTO._serialized_start=26
  _CATEGORY_PROTO._serialized_end=119
  _PRODUCT_PROTO._serialized_start=122
  _PRODUCT_PROTO._serialized_end=394
  _REVIEW_PROTO._serialized_start=396
  _REVIEW_PROTO._serialized_end=492
  _RATING_PROTO._serialized_start=494
  _RATING_PROTO._serialized_end=585
# @@protoc_insertion_point(module_scope)
