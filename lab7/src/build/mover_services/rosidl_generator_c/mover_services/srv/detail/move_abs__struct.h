// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mover_services:srv/MoveAbs.idl
// generated code does not contain a copyright notice

#ifndef MOVER_SERVICES__SRV__DETAIL__MOVE_ABS__STRUCT_H_
#define MOVER_SERVICES__SRV__DETAIL__MOVE_ABS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/MoveAbs in the package mover_services.
typedef struct mover_services__srv__MoveAbs_Request
{
  double x;
  double y;
  double z;
} mover_services__srv__MoveAbs_Request;

// Struct for a sequence of mover_services__srv__MoveAbs_Request.
typedef struct mover_services__srv__MoveAbs_Request__Sequence
{
  mover_services__srv__MoveAbs_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mover_services__srv__MoveAbs_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveAbs in the package mover_services.
typedef struct mover_services__srv__MoveAbs_Response
{
  bool success;
  rosidl_runtime_c__String message;
} mover_services__srv__MoveAbs_Response;

// Struct for a sequence of mover_services__srv__MoveAbs_Response.
typedef struct mover_services__srv__MoveAbs_Response__Sequence
{
  mover_services__srv__MoveAbs_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mover_services__srv__MoveAbs_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MOVER_SERVICES__SRV__DETAIL__MOVE_ABS__STRUCT_H_
