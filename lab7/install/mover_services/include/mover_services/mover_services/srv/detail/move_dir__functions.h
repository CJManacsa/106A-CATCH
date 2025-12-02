// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from mover_services:srv/MoveDir.idl
// generated code does not contain a copyright notice

#ifndef MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__FUNCTIONS_H_
#define MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "mover_services/msg/rosidl_generator_c__visibility_control.h"

#include "mover_services/srv/detail/move_dir__struct.h"

/// Initialize srv/MoveDir message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * mover_services__srv__MoveDir_Request
 * )) before or use
 * mover_services__srv__MoveDir_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Request__init(mover_services__srv__MoveDir_Request * msg);

/// Finalize srv/MoveDir message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
void
mover_services__srv__MoveDir_Request__fini(mover_services__srv__MoveDir_Request * msg);

/// Create srv/MoveDir message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * mover_services__srv__MoveDir_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
mover_services__srv__MoveDir_Request *
mover_services__srv__MoveDir_Request__create();

/// Destroy srv/MoveDir message.
/**
 * It calls
 * mover_services__srv__MoveDir_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
void
mover_services__srv__MoveDir_Request__destroy(mover_services__srv__MoveDir_Request * msg);

/// Check for srv/MoveDir message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Request__are_equal(const mover_services__srv__MoveDir_Request * lhs, const mover_services__srv__MoveDir_Request * rhs);

/// Copy a srv/MoveDir message.
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
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Request__copy(
  const mover_services__srv__MoveDir_Request * input,
  mover_services__srv__MoveDir_Request * output);

/// Initialize array of srv/MoveDir messages.
/**
 * It allocates the memory for the number of elements and calls
 * mover_services__srv__MoveDir_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Request__Sequence__init(mover_services__srv__MoveDir_Request__Sequence * array, size_t size);

/// Finalize array of srv/MoveDir messages.
/**
 * It calls
 * mover_services__srv__MoveDir_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
void
mover_services__srv__MoveDir_Request__Sequence__fini(mover_services__srv__MoveDir_Request__Sequence * array);

/// Create array of srv/MoveDir messages.
/**
 * It allocates the memory for the array and calls
 * mover_services__srv__MoveDir_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
mover_services__srv__MoveDir_Request__Sequence *
mover_services__srv__MoveDir_Request__Sequence__create(size_t size);

/// Destroy array of srv/MoveDir messages.
/**
 * It calls
 * mover_services__srv__MoveDir_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
void
mover_services__srv__MoveDir_Request__Sequence__destroy(mover_services__srv__MoveDir_Request__Sequence * array);

/// Check for srv/MoveDir message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Request__Sequence__are_equal(const mover_services__srv__MoveDir_Request__Sequence * lhs, const mover_services__srv__MoveDir_Request__Sequence * rhs);

/// Copy an array of srv/MoveDir messages.
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
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Request__Sequence__copy(
  const mover_services__srv__MoveDir_Request__Sequence * input,
  mover_services__srv__MoveDir_Request__Sequence * output);

/// Initialize srv/MoveDir message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * mover_services__srv__MoveDir_Response
 * )) before or use
 * mover_services__srv__MoveDir_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Response__init(mover_services__srv__MoveDir_Response * msg);

/// Finalize srv/MoveDir message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
void
mover_services__srv__MoveDir_Response__fini(mover_services__srv__MoveDir_Response * msg);

/// Create srv/MoveDir message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * mover_services__srv__MoveDir_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
mover_services__srv__MoveDir_Response *
mover_services__srv__MoveDir_Response__create();

/// Destroy srv/MoveDir message.
/**
 * It calls
 * mover_services__srv__MoveDir_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
void
mover_services__srv__MoveDir_Response__destroy(mover_services__srv__MoveDir_Response * msg);

/// Check for srv/MoveDir message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Response__are_equal(const mover_services__srv__MoveDir_Response * lhs, const mover_services__srv__MoveDir_Response * rhs);

/// Copy a srv/MoveDir message.
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
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Response__copy(
  const mover_services__srv__MoveDir_Response * input,
  mover_services__srv__MoveDir_Response * output);

/// Initialize array of srv/MoveDir messages.
/**
 * It allocates the memory for the number of elements and calls
 * mover_services__srv__MoveDir_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Response__Sequence__init(mover_services__srv__MoveDir_Response__Sequence * array, size_t size);

/// Finalize array of srv/MoveDir messages.
/**
 * It calls
 * mover_services__srv__MoveDir_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
void
mover_services__srv__MoveDir_Response__Sequence__fini(mover_services__srv__MoveDir_Response__Sequence * array);

/// Create array of srv/MoveDir messages.
/**
 * It allocates the memory for the array and calls
 * mover_services__srv__MoveDir_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
mover_services__srv__MoveDir_Response__Sequence *
mover_services__srv__MoveDir_Response__Sequence__create(size_t size);

/// Destroy array of srv/MoveDir messages.
/**
 * It calls
 * mover_services__srv__MoveDir_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
void
mover_services__srv__MoveDir_Response__Sequence__destroy(mover_services__srv__MoveDir_Response__Sequence * array);

/// Check for srv/MoveDir message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Response__Sequence__are_equal(const mover_services__srv__MoveDir_Response__Sequence * lhs, const mover_services__srv__MoveDir_Response__Sequence * rhs);

/// Copy an array of srv/MoveDir messages.
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
ROSIDL_GENERATOR_C_PUBLIC_mover_services
bool
mover_services__srv__MoveDir_Response__Sequence__copy(
  const mover_services__srv__MoveDir_Response__Sequence * input,
  mover_services__srv__MoveDir_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MOVER_SERVICES__SRV__DETAIL__MOVE_DIR__FUNCTIONS_H_
