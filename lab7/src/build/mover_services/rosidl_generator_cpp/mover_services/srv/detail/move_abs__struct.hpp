// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mover_services:srv/MoveAbs.idl
// generated code does not contain a copyright notice

#ifndef MOVER_SERVICES__SRV__DETAIL__MOVE_ABS__STRUCT_HPP_
#define MOVER_SERVICES__SRV__DETAIL__MOVE_ABS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__mover_services__srv__MoveAbs_Request __attribute__((deprecated))
#else
# define DEPRECATED__mover_services__srv__MoveAbs_Request __declspec(deprecated)
#endif

namespace mover_services
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveAbs_Request_
{
  using Type = MoveAbs_Request_<ContainerAllocator>;

  explicit MoveAbs_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
    }
  }

  explicit MoveAbs_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
    }
  }

  // field types and members
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _z_type =
    double;
  _z_type z;

  // setters for named parameter idiom
  Type & set__x(
    const double & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const double & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const double & _arg)
  {
    this->z = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mover_services::srv::MoveAbs_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const mover_services::srv::MoveAbs_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mover_services::srv::MoveAbs_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mover_services::srv::MoveAbs_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mover_services::srv::MoveAbs_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mover_services::srv::MoveAbs_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mover_services::srv::MoveAbs_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mover_services::srv::MoveAbs_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mover_services::srv::MoveAbs_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mover_services::srv::MoveAbs_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mover_services__srv__MoveAbs_Request
    std::shared_ptr<mover_services::srv::MoveAbs_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mover_services__srv__MoveAbs_Request
    std::shared_ptr<mover_services::srv::MoveAbs_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveAbs_Request_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveAbs_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveAbs_Request_

// alias to use template instance with default allocator
using MoveAbs_Request =
  mover_services::srv::MoveAbs_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace mover_services


#ifndef _WIN32
# define DEPRECATED__mover_services__srv__MoveAbs_Response __attribute__((deprecated))
#else
# define DEPRECATED__mover_services__srv__MoveAbs_Response __declspec(deprecated)
#endif

namespace mover_services
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveAbs_Response_
{
  using Type = MoveAbs_Response_<ContainerAllocator>;

  explicit MoveAbs_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit MoveAbs_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mover_services::srv::MoveAbs_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const mover_services::srv::MoveAbs_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mover_services::srv::MoveAbs_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mover_services::srv::MoveAbs_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mover_services::srv::MoveAbs_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mover_services::srv::MoveAbs_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mover_services::srv::MoveAbs_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mover_services::srv::MoveAbs_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mover_services::srv::MoveAbs_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mover_services::srv::MoveAbs_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mover_services__srv__MoveAbs_Response
    std::shared_ptr<mover_services::srv::MoveAbs_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mover_services__srv__MoveAbs_Response
    std::shared_ptr<mover_services::srv::MoveAbs_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveAbs_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveAbs_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveAbs_Response_

// alias to use template instance with default allocator
using MoveAbs_Response =
  mover_services::srv::MoveAbs_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace mover_services

namespace mover_services
{

namespace srv
{

struct MoveAbs
{
  using Request = mover_services::srv::MoveAbs_Request;
  using Response = mover_services::srv::MoveAbs_Response;
};

}  // namespace srv

}  // namespace mover_services

#endif  // MOVER_SERVICES__SRV__DETAIL__MOVE_ABS__STRUCT_HPP_
