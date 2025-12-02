// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mover_services:srv/MoveDir.idl
// generated code does not contain a copyright notice

#ifndef MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__STRUCT_HPP_
#define MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__mover_services__srv__MoveDir_Request __attribute__((deprecated))
#else
# define DEPRECATED__mover_services__srv__MoveDir_Request __declspec(deprecated)
#endif

namespace mover_services
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveDir_Request_
{
  using Type = MoveDir_Request_<ContainerAllocator>;

  explicit MoveDir_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->direction = "";
      this->distance = 0.0;
    }
  }

  explicit MoveDir_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : direction(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->direction = "";
      this->distance = 0.0;
    }
  }

  // field types and members
  using _direction_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _direction_type direction;
  using _distance_type =
    double;
  _distance_type distance;

  // setters for named parameter idiom
  Type & set__direction(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->direction = _arg;
    return *this;
  }
  Type & set__distance(
    const double & _arg)
  {
    this->distance = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mover_services::srv::MoveDir_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const mover_services::srv::MoveDir_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mover_services::srv::MoveDir_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mover_services::srv::MoveDir_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mover_services::srv::MoveDir_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mover_services::srv::MoveDir_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mover_services::srv::MoveDir_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mover_services::srv::MoveDir_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mover_services::srv::MoveDir_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mover_services::srv::MoveDir_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mover_services__srv__MoveDir_Request
    std::shared_ptr<mover_services::srv::MoveDir_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mover_services__srv__MoveDir_Request
    std::shared_ptr<mover_services::srv::MoveDir_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveDir_Request_ & other) const
  {
    if (this->direction != other.direction) {
      return false;
    }
    if (this->distance != other.distance) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveDir_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveDir_Request_

// alias to use template instance with default allocator
using MoveDir_Request =
  mover_services::srv::MoveDir_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace mover_services


#ifndef _WIN32
# define DEPRECATED__mover_services__srv__MoveDir_Response __attribute__((deprecated))
#else
# define DEPRECATED__mover_services__srv__MoveDir_Response __declspec(deprecated)
#endif

namespace mover_services
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveDir_Response_
{
  using Type = MoveDir_Response_<ContainerAllocator>;

  explicit MoveDir_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit MoveDir_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    mover_services::srv::MoveDir_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const mover_services::srv::MoveDir_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mover_services::srv::MoveDir_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mover_services::srv::MoveDir_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mover_services::srv::MoveDir_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mover_services::srv::MoveDir_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mover_services::srv::MoveDir_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mover_services::srv::MoveDir_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mover_services::srv::MoveDir_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mover_services::srv::MoveDir_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mover_services__srv__MoveDir_Response
    std::shared_ptr<mover_services::srv::MoveDir_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mover_services__srv__MoveDir_Response
    std::shared_ptr<mover_services::srv::MoveDir_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveDir_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveDir_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveDir_Response_

// alias to use template instance with default allocator
using MoveDir_Response =
  mover_services::srv::MoveDir_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace mover_services

namespace mover_services
{

namespace srv
{

struct MoveDir
{
  using Request = mover_services::srv::MoveDir_Request;
  using Response = mover_services::srv::MoveDir_Response;
};

}  // namespace srv

}  // namespace mover_services

#endif  // MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__STRUCT_HPP_
