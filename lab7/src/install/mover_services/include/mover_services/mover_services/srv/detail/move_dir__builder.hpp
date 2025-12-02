// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mover_services:srv/MoveDir.idl
// generated code does not contain a copyright notice

#ifndef MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__BUILDER_HPP_
#define MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mover_services/srv/detail/move_dir__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mover_services
{

namespace srv
{

namespace builder
{

class Init_MoveDir_Request_distance
{
public:
  explicit Init_MoveDir_Request_distance(::mover_services::srv::MoveDir_Request & msg)
  : msg_(msg)
  {}
  ::mover_services::srv::MoveDir_Request distance(::mover_services::srv::MoveDir_Request::_distance_type arg)
  {
    msg_.distance = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mover_services::srv::MoveDir_Request msg_;
};

class Init_MoveDir_Request_direction
{
public:
  Init_MoveDir_Request_direction()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveDir_Request_distance direction(::mover_services::srv::MoveDir_Request::_direction_type arg)
  {
    msg_.direction = std::move(arg);
    return Init_MoveDir_Request_distance(msg_);
  }

private:
  ::mover_services::srv::MoveDir_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::mover_services::srv::MoveDir_Request>()
{
  return mover_services::srv::builder::Init_MoveDir_Request_direction();
}

}  // namespace mover_services


namespace mover_services
{

namespace srv
{

namespace builder
{

class Init_MoveDir_Response_message
{
public:
  explicit Init_MoveDir_Response_message(::mover_services::srv::MoveDir_Response & msg)
  : msg_(msg)
  {}
  ::mover_services::srv::MoveDir_Response message(::mover_services::srv::MoveDir_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mover_services::srv::MoveDir_Response msg_;
};

class Init_MoveDir_Response_success
{
public:
  Init_MoveDir_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveDir_Response_message success(::mover_services::srv::MoveDir_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MoveDir_Response_message(msg_);
  }

private:
  ::mover_services::srv::MoveDir_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::mover_services::srv::MoveDir_Response>()
{
  return mover_services::srv::builder::Init_MoveDir_Response_success();
}

}  // namespace mover_services

#endif  // MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__BUILDER_HPP_
