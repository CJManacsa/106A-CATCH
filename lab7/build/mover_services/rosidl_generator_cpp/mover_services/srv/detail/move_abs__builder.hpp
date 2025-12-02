// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mover_services:srv/MoveAbs.idl
// generated code does not contain a copyright notice

#ifndef MOVER_SERVICES__SRV__DETAIL__MOVE_ABS__BUILDER_HPP_
#define MOVER_SERVICES__SRV__DETAIL__MOVE_ABS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mover_services/srv/detail/move_abs__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mover_services
{

namespace srv
{

namespace builder
{

class Init_MoveAbs_Request_z
{
public:
  explicit Init_MoveAbs_Request_z(::mover_services::srv::MoveAbs_Request & msg)
  : msg_(msg)
  {}
  ::mover_services::srv::MoveAbs_Request z(::mover_services::srv::MoveAbs_Request::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mover_services::srv::MoveAbs_Request msg_;
};

class Init_MoveAbs_Request_y
{
public:
  explicit Init_MoveAbs_Request_y(::mover_services::srv::MoveAbs_Request & msg)
  : msg_(msg)
  {}
  Init_MoveAbs_Request_z y(::mover_services::srv::MoveAbs_Request::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_MoveAbs_Request_z(msg_);
  }

private:
  ::mover_services::srv::MoveAbs_Request msg_;
};

class Init_MoveAbs_Request_x
{
public:
  Init_MoveAbs_Request_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveAbs_Request_y x(::mover_services::srv::MoveAbs_Request::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_MoveAbs_Request_y(msg_);
  }

private:
  ::mover_services::srv::MoveAbs_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::mover_services::srv::MoveAbs_Request>()
{
  return mover_services::srv::builder::Init_MoveAbs_Request_x();
}

}  // namespace mover_services


namespace mover_services
{

namespace srv
{

namespace builder
{

class Init_MoveAbs_Response_message
{
public:
  explicit Init_MoveAbs_Response_message(::mover_services::srv::MoveAbs_Response & msg)
  : msg_(msg)
  {}
  ::mover_services::srv::MoveAbs_Response message(::mover_services::srv::MoveAbs_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mover_services::srv::MoveAbs_Response msg_;
};

class Init_MoveAbs_Response_success
{
public:
  Init_MoveAbs_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveAbs_Response_message success(::mover_services::srv::MoveAbs_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MoveAbs_Response_message(msg_);
  }

private:
  ::mover_services::srv::MoveAbs_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::mover_services::srv::MoveAbs_Response>()
{
  return mover_services::srv::builder::Init_MoveAbs_Response_success();
}

}  // namespace mover_services

#endif  // MOVER_SERVICES__SRV__DETAIL__MOVE_ABS__BUILDER_HPP_
