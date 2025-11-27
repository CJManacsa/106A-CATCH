// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from ros2_aruco_interfaces:srv/StoreTransform.idl
// generated code does not contain a copyright notice

#ifndef ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__TRAITS_HPP_
#define ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "ros2_aruco_interfaces/srv/detail/store_transform__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace ros2_aruco_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const StoreTransform_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: parent_frame
  {
    out << "parent_frame: ";
    rosidl_generator_traits::value_to_yaml(msg.parent_frame, out);
    out << ", ";
  }

  // member: child_frame
  {
    out << "child_frame: ";
    rosidl_generator_traits::value_to_yaml(msg.child_frame, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const StoreTransform_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: parent_frame
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "parent_frame: ";
    rosidl_generator_traits::value_to_yaml(msg.parent_frame, out);
    out << "\n";
  }

  // member: child_frame
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "child_frame: ";
    rosidl_generator_traits::value_to_yaml(msg.child_frame, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const StoreTransform_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace ros2_aruco_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use ros2_aruco_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const ros2_aruco_interfaces::srv::StoreTransform_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  ros2_aruco_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use ros2_aruco_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const ros2_aruco_interfaces::srv::StoreTransform_Request & msg)
{
  return ros2_aruco_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<ros2_aruco_interfaces::srv::StoreTransform_Request>()
{
  return "ros2_aruco_interfaces::srv::StoreTransform_Request";
}

template<>
inline const char * name<ros2_aruco_interfaces::srv::StoreTransform_Request>()
{
  return "ros2_aruco_interfaces/srv/StoreTransform_Request";
}

template<>
struct has_fixed_size<ros2_aruco_interfaces::srv::StoreTransform_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<ros2_aruco_interfaces::srv::StoreTransform_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<ros2_aruco_interfaces::srv::StoreTransform_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace ros2_aruco_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const StoreTransform_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const StoreTransform_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const StoreTransform_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace ros2_aruco_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use ros2_aruco_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const ros2_aruco_interfaces::srv::StoreTransform_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  ros2_aruco_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use ros2_aruco_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const ros2_aruco_interfaces::srv::StoreTransform_Response & msg)
{
  return ros2_aruco_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<ros2_aruco_interfaces::srv::StoreTransform_Response>()
{
  return "ros2_aruco_interfaces::srv::StoreTransform_Response";
}

template<>
inline const char * name<ros2_aruco_interfaces::srv::StoreTransform_Response>()
{
  return "ros2_aruco_interfaces/srv/StoreTransform_Response";
}

template<>
struct has_fixed_size<ros2_aruco_interfaces::srv::StoreTransform_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<ros2_aruco_interfaces::srv::StoreTransform_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<ros2_aruco_interfaces::srv::StoreTransform_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<ros2_aruco_interfaces::srv::StoreTransform>()
{
  return "ros2_aruco_interfaces::srv::StoreTransform";
}

template<>
inline const char * name<ros2_aruco_interfaces::srv::StoreTransform>()
{
  return "ros2_aruco_interfaces/srv/StoreTransform";
}

template<>
struct has_fixed_size<ros2_aruco_interfaces::srv::StoreTransform>
  : std::integral_constant<
    bool,
    has_fixed_size<ros2_aruco_interfaces::srv::StoreTransform_Request>::value &&
    has_fixed_size<ros2_aruco_interfaces::srv::StoreTransform_Response>::value
  >
{
};

template<>
struct has_bounded_size<ros2_aruco_interfaces::srv::StoreTransform>
  : std::integral_constant<
    bool,
    has_bounded_size<ros2_aruco_interfaces::srv::StoreTransform_Request>::value &&
    has_bounded_size<ros2_aruco_interfaces::srv::StoreTransform_Response>::value
  >
{
};

template<>
struct is_service<ros2_aruco_interfaces::srv::StoreTransform>
  : std::true_type
{
};

template<>
struct is_service_request<ros2_aruco_interfaces::srv::StoreTransform_Request>
  : std::true_type
{
};

template<>
struct is_service_response<ros2_aruco_interfaces::srv::StoreTransform_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__TRAITS_HPP_
