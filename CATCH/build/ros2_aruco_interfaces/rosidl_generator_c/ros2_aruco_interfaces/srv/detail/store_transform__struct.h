// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from ros2_aruco_interfaces:srv/StoreTransform.idl
// generated code does not contain a copyright notice

#ifndef ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__STRUCT_H_
#define ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'parent_frame'
// Member 'child_frame'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/StoreTransform in the package ros2_aruco_interfaces.
typedef struct ros2_aruco_interfaces__srv__StoreTransform_Request
{
  rosidl_runtime_c__String parent_frame;
  rosidl_runtime_c__String child_frame;
} ros2_aruco_interfaces__srv__StoreTransform_Request;

// Struct for a sequence of ros2_aruco_interfaces__srv__StoreTransform_Request.
typedef struct ros2_aruco_interfaces__srv__StoreTransform_Request__Sequence
{
  ros2_aruco_interfaces__srv__StoreTransform_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ros2_aruco_interfaces__srv__StoreTransform_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/StoreTransform in the package ros2_aruco_interfaces.
typedef struct ros2_aruco_interfaces__srv__StoreTransform_Response
{
  bool success;
  rosidl_runtime_c__String message;
} ros2_aruco_interfaces__srv__StoreTransform_Response;

// Struct for a sequence of ros2_aruco_interfaces__srv__StoreTransform_Response.
typedef struct ros2_aruco_interfaces__srv__StoreTransform_Response__Sequence
{
  ros2_aruco_interfaces__srv__StoreTransform_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ros2_aruco_interfaces__srv__StoreTransform_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__STRUCT_H_
