// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from catch_custom_msgs:msg/PointVel.idl
// generated code does not contain a copyright notice

#ifndef CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "catch_custom_msgs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "catch_custom_msgs/msg/detail/point_vel__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace catch_custom_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_catch_custom_msgs
cdr_serialize(
  const catch_custom_msgs::msg::PointVel & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_catch_custom_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  catch_custom_msgs::msg::PointVel & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_catch_custom_msgs
get_serialized_size(
  const catch_custom_msgs::msg::PointVel & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_catch_custom_msgs
max_serialized_size_PointVel(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace catch_custom_msgs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_catch_custom_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, catch_custom_msgs, msg, PointVel)();

#ifdef __cplusplus
}
#endif

#endif  // CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
