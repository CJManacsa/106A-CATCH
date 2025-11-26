// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from catch_custom_msgs:msg/PointVel.idl
// generated code does not contain a copyright notice

#ifndef CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__FUNCTIONS_H_
#define CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "catch_custom_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "catch_custom_msgs/msg/detail/point_vel__struct.h"

/// Initialize msg/PointVel message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * catch_custom_msgs__msg__PointVel
 * )) before or use
 * catch_custom_msgs__msg__PointVel__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
bool
catch_custom_msgs__msg__PointVel__init(catch_custom_msgs__msg__PointVel * msg);

/// Finalize msg/PointVel message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
void
catch_custom_msgs__msg__PointVel__fini(catch_custom_msgs__msg__PointVel * msg);

/// Create msg/PointVel message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * catch_custom_msgs__msg__PointVel__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
catch_custom_msgs__msg__PointVel *
catch_custom_msgs__msg__PointVel__create();

/// Destroy msg/PointVel message.
/**
 * It calls
 * catch_custom_msgs__msg__PointVel__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
void
catch_custom_msgs__msg__PointVel__destroy(catch_custom_msgs__msg__PointVel * msg);

/// Check for msg/PointVel message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
bool
catch_custom_msgs__msg__PointVel__are_equal(const catch_custom_msgs__msg__PointVel * lhs, const catch_custom_msgs__msg__PointVel * rhs);

/// Copy a msg/PointVel message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
bool
catch_custom_msgs__msg__PointVel__copy(
  const catch_custom_msgs__msg__PointVel * input,
  catch_custom_msgs__msg__PointVel * output);

/// Initialize array of msg/PointVel messages.
/**
 * It allocates the memory for the number of elements and calls
 * catch_custom_msgs__msg__PointVel__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
bool
catch_custom_msgs__msg__PointVel__Sequence__init(catch_custom_msgs__msg__PointVel__Sequence * array, size_t size);

/// Finalize array of msg/PointVel messages.
/**
 * It calls
 * catch_custom_msgs__msg__PointVel__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
void
catch_custom_msgs__msg__PointVel__Sequence__fini(catch_custom_msgs__msg__PointVel__Sequence * array);

/// Create array of msg/PointVel messages.
/**
 * It allocates the memory for the array and calls
 * catch_custom_msgs__msg__PointVel__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
catch_custom_msgs__msg__PointVel__Sequence *
catch_custom_msgs__msg__PointVel__Sequence__create(size_t size);

/// Destroy array of msg/PointVel messages.
/**
 * It calls
 * catch_custom_msgs__msg__PointVel__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
void
catch_custom_msgs__msg__PointVel__Sequence__destroy(catch_custom_msgs__msg__PointVel__Sequence * array);

/// Check for msg/PointVel message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
bool
catch_custom_msgs__msg__PointVel__Sequence__are_equal(const catch_custom_msgs__msg__PointVel__Sequence * lhs, const catch_custom_msgs__msg__PointVel__Sequence * rhs);

/// Copy an array of msg/PointVel messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_catch_custom_msgs
bool
catch_custom_msgs__msg__PointVel__Sequence__copy(
  const catch_custom_msgs__msg__PointVel__Sequence * input,
  catch_custom_msgs__msg__PointVel__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // CATCH_CUSTOM_MSGS__MSG__DETAIL__POINT_VEL__FUNCTIONS_H_
