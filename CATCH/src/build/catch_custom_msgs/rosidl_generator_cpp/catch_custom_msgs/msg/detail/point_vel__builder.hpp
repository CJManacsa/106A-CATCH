// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from catch_custom_msgs:msg/PointVel.idl
// generated code does not contain a copyright notice

#ifndef CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__BUILDER_HPP_
#define CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "catch_custom_msgs/msg/detail/point_vel__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace catch_custom_msgs
{

namespace msg
{

namespace builder
{

class Init_PointVel_vz
{
public:
  explicit Init_PointVel_vz(::catch_custom_msgs::msg::PointVel & msg)
  : msg_(msg)
  {}
  ::catch_custom_msgs::msg::PointVel vz(::catch_custom_msgs::msg::PointVel::_vz_type arg)
  {
    msg_.vz = std::move(arg);
    return std::move(msg_);
  }

private:
  ::catch_custom_msgs::msg::PointVel msg_;
};

class Init_PointVel_vy
{
public:
  explicit Init_PointVel_vy(::catch_custom_msgs::msg::PointVel & msg)
  : msg_(msg)
  {}
  Init_PointVel_vz vy(::catch_custom_msgs::msg::PointVel::_vy_type arg)
  {
    msg_.vy = std::move(arg);
    return Init_PointVel_vz(msg_);
  }

private:
  ::catch_custom_msgs::msg::PointVel msg_;
};

class Init_PointVel_vx
{
public:
  explicit Init_PointVel_vx(::catch_custom_msgs::msg::PointVel & msg)
  : msg_(msg)
  {}
  Init_PointVel_vy vx(::catch_custom_msgs::msg::PointVel::_vx_type arg)
  {
    msg_.vx = std::move(arg);
    return Init_PointVel_vy(msg_);
  }

private:
  ::catch_custom_msgs::msg::PointVel msg_;
};

class Init_PointVel_z
{
public:
  explicit Init_PointVel_z(::catch_custom_msgs::msg::PointVel & msg)
  : msg_(msg)
  {}
  Init_PointVel_vx z(::catch_custom_msgs::msg::PointVel::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_PointVel_vx(msg_);
  }

private:
  ::catch_custom_msgs::msg::PointVel msg_;
};

class Init_PointVel_y
{
public:
  explicit Init_PointVel_y(::catch_custom_msgs::msg::PointVel & msg)
  : msg_(msg)
  {}
  Init_PointVel_z y(::catch_custom_msgs::msg::PointVel::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_PointVel_z(msg_);
  }

private:
  ::catch_custom_msgs::msg::PointVel msg_;
};

class Init_PointVel_x
{
public:
  explicit Init_PointVel_x(::catch_custom_msgs::msg::PointVel & msg)
  : msg_(msg)
  {}
  Init_PointVel_y x(::catch_custom_msgs::msg::PointVel::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_PointVel_y(msg_);
  }

private:
  ::catch_custom_msgs::msg::PointVel msg_;
};

class Init_PointVel_header
{
public:
  Init_PointVel_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PointVel_x header(::catch_custom_msgs::msg::PointVel::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_PointVel_x(msg_);
  }

private:
  ::catch_custom_msgs::msg::PointVel msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::catch_custom_msgs::msg::PointVel>()
{
  return catch_custom_msgs::msg::builder::Init_PointVel_header();
}

}  // namespace catch_custom_msgs

#endif  // CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__BUILDER_HPP_
