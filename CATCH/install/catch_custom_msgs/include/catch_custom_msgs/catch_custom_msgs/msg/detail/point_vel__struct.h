// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from catch_custom_msgs:msg/PointVel.idl
// generated code does not contain a copyright notice

#ifndef CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__STRUCT_H_
#define CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/PointVel in the package catch_custom_msgs.
typedef struct catch_custom_msgs__msg__PointVel
{
  std_msgs__msg__Header header;
  /// Position
  float x;
  float y;
  float z;
  /// Velocity
  float vx;
  float vy;
  float vz;
} catch_custom_msgs__msg__PointVel;

// Struct for a sequence of catch_custom_msgs__msg__PointVel.
typedef struct catch_custom_msgs__msg__PointVel__Sequence
{
  catch_custom_msgs__msg__PointVel * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} catch_custom_msgs__msg__PointVel__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__STRUCT_H_
