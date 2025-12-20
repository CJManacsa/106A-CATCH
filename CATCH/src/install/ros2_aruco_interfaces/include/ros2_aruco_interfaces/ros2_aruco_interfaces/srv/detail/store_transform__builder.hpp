// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from ros2_aruco_interfaces:srv/StoreTransform.idl
// generated code does not contain a copyright notice

#ifndef ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__BUILDER_HPP_
#define ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "ros2_aruco_interfaces/srv/detail/store_transform__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace ros2_aruco_interfaces
{

namespace srv
{

namespace builder
{

class Init_StoreTransform_Request_child_frame
{
public:
  explicit Init_StoreTransform_Request_child_frame(::ros2_aruco_interfaces::srv::StoreTransform_Request & msg)
  : msg_(msg)
  {}
  ::ros2_aruco_interfaces::srv::StoreTransform_Request child_frame(::ros2_aruco_interfaces::srv::StoreTransform_Request::_child_frame_type arg)
  {
    msg_.child_frame = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ros2_aruco_interfaces::srv::StoreTransform_Request msg_;
};

class Init_StoreTransform_Request_parent_frame
{
public:
  Init_StoreTransform_Request_parent_frame()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_StoreTransform_Request_child_frame parent_frame(::ros2_aruco_interfaces::srv::StoreTransform_Request::_parent_frame_type arg)
  {
    msg_.parent_frame = std::move(arg);
    return Init_StoreTransform_Request_child_frame(msg_);
  }

private:
  ::ros2_aruco_interfaces::srv::StoreTransform_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::ros2_aruco_interfaces::srv::StoreTransform_Request>()
{
  return ros2_aruco_interfaces::srv::builder::Init_StoreTransform_Request_parent_frame();
}

}  // namespace ros2_aruco_interfaces


namespace ros2_aruco_interfaces
{

namespace srv
{

namespace builder
{

class Init_StoreTransform_Response_message
{
public:
  explicit Init_StoreTransform_Response_message(::ros2_aruco_interfaces::srv::StoreTransform_Response & msg)
  : msg_(msg)
  {}
  ::ros2_aruco_interfaces::srv::StoreTransform_Response message(::ros2_aruco_interfaces::srv::StoreTransform_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ros2_aruco_interfaces::srv::StoreTransform_Response msg_;
};

class Init_StoreTransform_Response_success
{
public:
  Init_StoreTransform_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_StoreTransform_Response_message success(::ros2_aruco_interfaces::srv::StoreTransform_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_StoreTransform_Response_message(msg_);
  }

private:
  ::ros2_aruco_interfaces::srv::StoreTransform_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::ros2_aruco_interfaces::srv::StoreTransform_Response>()
{
  return ros2_aruco_interfaces::srv::builder::Init_StoreTransform_Response_success();
}

}  // namespace ros2_aruco_interfaces

#endif  // ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__BUILDER_HPP_
