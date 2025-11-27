// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from catch_custom_msgs:msg/PointVel.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "catch_custom_msgs/msg/detail/point_vel__rosidl_typesupport_introspection_c.h"
#include "catch_custom_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "catch_custom_msgs/msg/detail/point_vel__functions.h"
#include "catch_custom_msgs/msg/detail/point_vel__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  catch_custom_msgs__msg__PointVel__init(message_memory);
}

void catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_fini_function(void * message_memory)
{
  catch_custom_msgs__msg__PointVel__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_message_member_array[7] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(catch_custom_msgs__msg__PointVel, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(catch_custom_msgs__msg__PointVel, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(catch_custom_msgs__msg__PointVel, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(catch_custom_msgs__msg__PointVel, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "vx",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(catch_custom_msgs__msg__PointVel, vx),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "vy",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(catch_custom_msgs__msg__PointVel, vy),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "vz",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(catch_custom_msgs__msg__PointVel, vz),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_message_members = {
  "catch_custom_msgs__msg",  // message namespace
  "PointVel",  // message name
  7,  // number of fields
  sizeof(catch_custom_msgs__msg__PointVel),
  catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_message_member_array,  // message members
  catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_init_function,  // function to initialize message memory (memory has to be allocated)
  catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_message_type_support_handle = {
  0,
  &catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_catch_custom_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, catch_custom_msgs, msg, PointVel)() {
  catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_message_type_support_handle.typesupport_identifier) {
    catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &catch_custom_msgs__msg__PointVel__rosidl_typesupport_introspection_c__PointVel_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
