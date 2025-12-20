// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from catch_custom_msgs:msg/PointVel.idl
// generated code does not contain a copyright notice

#ifndef CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__STRUCT_HPP_
#define CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__catch_custom_msgs__msg__PointVel __attribute__((deprecated))
#else
# define DEPRECATED__catch_custom_msgs__msg__PointVel __declspec(deprecated)
#endif

namespace catch_custom_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PointVel_
{
  using Type = PointVel_<ContainerAllocator>;

  explicit PointVel_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->vx = 0.0f;
      this->vy = 0.0f;
      this->vz = 0.0f;
    }
  }

  explicit PointVel_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->vx = 0.0f;
      this->vy = 0.0f;
      this->vz = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _x_type =
    float;
  _x_type x;
  using _y_type =
    float;
  _y_type y;
  using _z_type =
    float;
  _z_type z;
  using _vx_type =
    float;
  _vx_type vx;
  using _vy_type =
    float;
  _vy_type vy;
  using _vz_type =
    float;
  _vz_type vz;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__x(
    const float & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const float & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const float & _arg)
  {
    this->z = _arg;
    return *this;
  }
  Type & set__vx(
    const float & _arg)
  {
    this->vx = _arg;
    return *this;
  }
  Type & set__vy(
    const float & _arg)
  {
    this->vy = _arg;
    return *this;
  }
  Type & set__vz(
    const float & _arg)
  {
    this->vz = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    catch_custom_msgs::msg::PointVel_<ContainerAllocator> *;
  using ConstRawPtr =
    const catch_custom_msgs::msg::PointVel_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<catch_custom_msgs::msg::PointVel_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<catch_custom_msgs::msg::PointVel_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      catch_custom_msgs::msg::PointVel_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<catch_custom_msgs::msg::PointVel_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      catch_custom_msgs::msg::PointVel_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<catch_custom_msgs::msg::PointVel_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<catch_custom_msgs::msg::PointVel_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<catch_custom_msgs::msg::PointVel_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__catch_custom_msgs__msg__PointVel
    std::shared_ptr<catch_custom_msgs::msg::PointVel_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__catch_custom_msgs__msg__PointVel
    std::shared_ptr<catch_custom_msgs::msg::PointVel_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PointVel_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    if (this->vx != other.vx) {
      return false;
    }
    if (this->vy != other.vy) {
      return false;
    }
    if (this->vz != other.vz) {
      return false;
    }
    return true;
  }
  bool operator!=(const PointVel_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PointVel_

// alias to use template instance with default allocator
using PointVel =
  catch_custom_msgs::msg::PointVel_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace catch_custom_msgs

#endif  // CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__STRUCT_HPP_
