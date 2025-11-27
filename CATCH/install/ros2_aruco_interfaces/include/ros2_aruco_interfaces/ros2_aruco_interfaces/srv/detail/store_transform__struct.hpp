// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from ros2_aruco_interfaces:srv/StoreTransform.idl
// generated code does not contain a copyright notice

#ifndef ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__STRUCT_HPP_
#define ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__ros2_aruco_interfaces__srv__StoreTransform_Request __attribute__((deprecated))
#else
# define DEPRECATED__ros2_aruco_interfaces__srv__StoreTransform_Request __declspec(deprecated)
#endif

namespace ros2_aruco_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct StoreTransform_Request_
{
  using Type = StoreTransform_Request_<ContainerAllocator>;

  explicit StoreTransform_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->parent_frame = "";
      this->child_frame = "";
    }
  }

  explicit StoreTransform_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : parent_frame(_alloc),
    child_frame(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->parent_frame = "";
      this->child_frame = "";
    }
  }

  // field types and members
  using _parent_frame_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _parent_frame_type parent_frame;
  using _child_frame_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _child_frame_type child_frame;

  // setters for named parameter idiom
  Type & set__parent_frame(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->parent_frame = _arg;
    return *this;
  }
  Type & set__child_frame(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->child_frame = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ros2_aruco_interfaces__srv__StoreTransform_Request
    std::shared_ptr<ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ros2_aruco_interfaces__srv__StoreTransform_Request
    std::shared_ptr<ros2_aruco_interfaces::srv::StoreTransform_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const StoreTransform_Request_ & other) const
  {
    if (this->parent_frame != other.parent_frame) {
      return false;
    }
    if (this->child_frame != other.child_frame) {
      return false;
    }
    return true;
  }
  bool operator!=(const StoreTransform_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct StoreTransform_Request_

// alias to use template instance with default allocator
using StoreTransform_Request =
  ros2_aruco_interfaces::srv::StoreTransform_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace ros2_aruco_interfaces


#ifndef _WIN32
# define DEPRECATED__ros2_aruco_interfaces__srv__StoreTransform_Response __attribute__((deprecated))
#else
# define DEPRECATED__ros2_aruco_interfaces__srv__StoreTransform_Response __declspec(deprecated)
#endif

namespace ros2_aruco_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct StoreTransform_Response_
{
  using Type = StoreTransform_Response_<ContainerAllocator>;

  explicit StoreTransform_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit StoreTransform_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ros2_aruco_interfaces__srv__StoreTransform_Response
    std::shared_ptr<ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ros2_aruco_interfaces__srv__StoreTransform_Response
    std::shared_ptr<ros2_aruco_interfaces::srv::StoreTransform_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const StoreTransform_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const StoreTransform_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct StoreTransform_Response_

// alias to use template instance with default allocator
using StoreTransform_Response =
  ros2_aruco_interfaces::srv::StoreTransform_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace ros2_aruco_interfaces

namespace ros2_aruco_interfaces
{

namespace srv
{

struct StoreTransform
{
  using Request = ros2_aruco_interfaces::srv::StoreTransform_Request;
  using Response = ros2_aruco_interfaces::srv::StoreTransform_Response;
};

}  // namespace srv

}  // namespace ros2_aruco_interfaces

#endif  // ROS2_ARUCO_INTERFACES__SRV__DETAIL__STORE_TRANSFORM__STRUCT_HPP_
