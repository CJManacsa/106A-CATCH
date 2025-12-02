// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from mover_services:srv/MoveDir.idl
// generated code does not contain a copyright notice

#ifndef MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__TRAITS_HPP_
#define MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "mover_services/srv/detail/move_dir__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace mover_services
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveDir_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: direction
  {
    out << "direction: ";
    rosidl_generator_traits::value_to_yaml(msg.direction, out);
    out << ", ";
  }

  // member: distance
  {
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveDir_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: direction
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "direction: ";
    rosidl_generator_traits::value_to_yaml(msg.direction, out);
    out << "\n";
  }

  // member: distance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveDir_Request & msg, bool use_flow_style = false)
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

}  // namespace mover_services

namespace rosidl_generator_traits
{

[[deprecated("use mover_services::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const mover_services::srv::MoveDir_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  mover_services::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use mover_services::srv::to_yaml() instead")]]
inline std::string to_yaml(const mover_services::srv::MoveDir_Request & msg)
{
  return mover_services::srv::to_yaml(msg);
}

template<>
inline const char * data_type<mover_services::srv::MoveDir_Request>()
{
  return "mover_services::srv::MoveDir_Request";
}

template<>
inline const char * name<mover_services::srv::MoveDir_Request>()
{
  return "mover_services/srv/MoveDir_Request";
}

template<>
struct has_fixed_size<mover_services::srv::MoveDir_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<mover_services::srv::MoveDir_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<mover_services::srv::MoveDir_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace mover_services
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveDir_Response & msg,
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
  const MoveDir_Response & msg,
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

inline std::string to_yaml(const MoveDir_Response & msg, bool use_flow_style = false)
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

}  // namespace mover_services

namespace rosidl_generator_traits
{

[[deprecated("use mover_services::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const mover_services::srv::MoveDir_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  mover_services::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use mover_services::srv::to_yaml() instead")]]
inline std::string to_yaml(const mover_services::srv::MoveDir_Response & msg)
{
  return mover_services::srv::to_yaml(msg);
}

template<>
inline const char * data_type<mover_services::srv::MoveDir_Response>()
{
  return "mover_services::srv::MoveDir_Response";
}

template<>
inline const char * name<mover_services::srv::MoveDir_Response>()
{
  return "mover_services/srv/MoveDir_Response";
}

template<>
struct has_fixed_size<mover_services::srv::MoveDir_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<mover_services::srv::MoveDir_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<mover_services::srv::MoveDir_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<mover_services::srv::MoveDir>()
{
  return "mover_services::srv::MoveDir";
}

template<>
inline const char * name<mover_services::srv::MoveDir>()
{
  return "mover_services/srv/MoveDir";
}

template<>
struct has_fixed_size<mover_services::srv::MoveDir>
  : std::integral_constant<
    bool,
    has_fixed_size<mover_services::srv::MoveDir_Request>::value &&
    has_fixed_size<mover_services::srv::MoveDir_Response>::value
  >
{
};

template<>
struct has_bounded_size<mover_services::srv::MoveDir>
  : std::integral_constant<
    bool,
    has_bounded_size<mover_services::srv::MoveDir_Request>::value &&
    has_bounded_size<mover_services::srv::MoveDir_Response>::value
  >
{
};

template<>
struct is_service<mover_services::srv::MoveDir>
  : std::true_type
{
};

template<>
struct is_service_request<mover_services::srv::MoveDir_Request>
  : std::true_type
{
};

template<>
struct is_service_response<mover_services::srv::MoveDir_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__TRAITS_HPP_
