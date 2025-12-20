// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from catch_custom_msgs:msg/PointVel.idl
// generated code does not contain a copyright notice

#ifndef CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__TRAITS_HPP_
#define CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "catch_custom_msgs/msg/detail/point_vel__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace catch_custom_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const PointVel & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << ", ";
  }

  // member: vx
  {
    out << "vx: ";
    rosidl_generator_traits::value_to_yaml(msg.vx, out);
    out << ", ";
  }

  // member: vy
  {
    out << "vy: ";
    rosidl_generator_traits::value_to_yaml(msg.vy, out);
    out << ", ";
  }

  // member: vz
  {
    out << "vz: ";
    rosidl_generator_traits::value_to_yaml(msg.vz, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PointVel & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }

  // member: vx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vx: ";
    rosidl_generator_traits::value_to_yaml(msg.vx, out);
    out << "\n";
  }

  // member: vy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vy: ";
    rosidl_generator_traits::value_to_yaml(msg.vy, out);
    out << "\n";
  }

  // member: vz
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vz: ";
    rosidl_generator_traits::value_to_yaml(msg.vz, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PointVel & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace catch_custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use catch_custom_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const catch_custom_msgs::msg::PointVel & msg,
  std::ostream & out, size_t indentation = 0)
{
  catch_custom_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use catch_custom_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const catch_custom_msgs::msg::PointVel & msg)
{
  return catch_custom_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<catch_custom_msgs::msg::PointVel>()
{
  return "catch_custom_msgs::msg::PointVel";
}

template<>
inline const char * name<catch_custom_msgs::msg::PointVel>()
{
  return "catch_custom_msgs/msg/PointVel";
}

template<>
struct has_fixed_size<catch_custom_msgs::msg::PointVel>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<catch_custom_msgs::msg::PointVel>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<catch_custom_msgs::msg::PointVel>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__TRAITS_HPP_
