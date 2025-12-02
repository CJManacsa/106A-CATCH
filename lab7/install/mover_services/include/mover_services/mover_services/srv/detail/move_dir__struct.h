// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mover_services:srv/MoveDir.idl
// generated code does not contain a copyright notice

#ifndef MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__STRUCT_H_
#define MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'direction'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveDir in the package mover_services.
typedef struct mover_services__srv__MoveDir_Request
{
  /// "up", "down", "left", "right", "forward", "backward"
  rosidl_runtime_c__String direction;
  /// meters
  double distance;
} mover_services__srv__MoveDir_Request;

// Struct for a sequence of mover_services__srv__MoveDir_Request.
typedef struct mover_services__srv__MoveDir_Request__Sequence
{
  mover_services__srv__MoveDir_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mover_services__srv__MoveDir_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveDir in the package mover_services.
typedef struct mover_services__srv__MoveDir_Response
{
  bool success;
  rosidl_runtime_c__String message;
} mover_services__srv__MoveDir_Response;

// Struct for a sequence of mover_services__srv__MoveDir_Response.
typedef struct mover_services__srv__MoveDir_Response__Sequence
{
  mover_services__srv__MoveDir_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mover_services__srv__MoveDir_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__STRUCT_H_
