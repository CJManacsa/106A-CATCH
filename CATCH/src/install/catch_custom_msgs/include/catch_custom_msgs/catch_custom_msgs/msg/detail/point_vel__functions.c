// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from catch_custom_msgs:msg/PointVel.idl
// generated code does not contain a copyright notice
#include "catch_custom_msgs/msg/detail/point_vel__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
catch_custom_msgs__msg__PointVel__init(catch_custom_msgs__msg__PointVel * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    catch_custom_msgs__msg__PointVel__fini(msg);
    return false;
  }
  // x
  // y
  // z
  // vx
  // vy
  // vz
  return true;
}

void
catch_custom_msgs__msg__PointVel__fini(catch_custom_msgs__msg__PointVel * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // x
  // y
  // z
  // vx
  // vy
  // vz
}

bool
catch_custom_msgs__msg__PointVel__are_equal(const catch_custom_msgs__msg__PointVel * lhs, const catch_custom_msgs__msg__PointVel * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // vx
  if (lhs->vx != rhs->vx) {
    return false;
  }
  // vy
  if (lhs->vy != rhs->vy) {
    return false;
  }
  // vz
  if (lhs->vz != rhs->vz) {
    return false;
  }
  return true;
}

bool
catch_custom_msgs__msg__PointVel__copy(
  const catch_custom_msgs__msg__PointVel * input,
  catch_custom_msgs__msg__PointVel * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // vx
  output->vx = input->vx;
  // vy
  output->vy = input->vy;
  // vz
  output->vz = input->vz;
  return true;
}

catch_custom_msgs__msg__PointVel *
catch_custom_msgs__msg__PointVel__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  catch_custom_msgs__msg__PointVel * msg = (catch_custom_msgs__msg__PointVel *)allocator.allocate(sizeof(catch_custom_msgs__msg__PointVel), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(catch_custom_msgs__msg__PointVel));
  bool success = catch_custom_msgs__msg__PointVel__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
catch_custom_msgs__msg__PointVel__destroy(catch_custom_msgs__msg__PointVel * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    catch_custom_msgs__msg__PointVel__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
catch_custom_msgs__msg__PointVel__Sequence__init(catch_custom_msgs__msg__PointVel__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  catch_custom_msgs__msg__PointVel * data = NULL;

  if (size) {
    data = (catch_custom_msgs__msg__PointVel *)allocator.zero_allocate(size, sizeof(catch_custom_msgs__msg__PointVel), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = catch_custom_msgs__msg__PointVel__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        catch_custom_msgs__msg__PointVel__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
catch_custom_msgs__msg__PointVel__Sequence__fini(catch_custom_msgs__msg__PointVel__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      catch_custom_msgs__msg__PointVel__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

catch_custom_msgs__msg__PointVel__Sequence *
catch_custom_msgs__msg__PointVel__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  catch_custom_msgs__msg__PointVel__Sequence * array = (catch_custom_msgs__msg__PointVel__Sequence *)allocator.allocate(sizeof(catch_custom_msgs__msg__PointVel__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = catch_custom_msgs__msg__PointVel__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
catch_custom_msgs__msg__PointVel__Sequence__destroy(catch_custom_msgs__msg__PointVel__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    catch_custom_msgs__msg__PointVel__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
catch_custom_msgs__msg__PointVel__Sequence__are_equal(const catch_custom_msgs__msg__PointVel__Sequence * lhs, const catch_custom_msgs__msg__PointVel__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!catch_custom_msgs__msg__PointVel__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
catch_custom_msgs__msg__PointVel__Sequence__copy(
  const catch_custom_msgs__msg__PointVel__Sequence * input,
  catch_custom_msgs__msg__PointVel__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(catch_custom_msgs__msg__PointVel);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    catch_custom_msgs__msg__PointVel * data =
      (catch_custom_msgs__msg__PointVel *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!catch_custom_msgs__msg__PointVel__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          catch_custom_msgs__msg__PointVel__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!catch_custom_msgs__msg__PointVel__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
