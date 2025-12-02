// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from mover_services:srv/MoveDir.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "mover_services/srv/detail/move_dir__struct.h"
#include "mover_services/srv/detail/move_dir__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace mover_services
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _MoveDir_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveDir_Request_type_support_ids_t;

static const _MoveDir_Request_type_support_ids_t _MoveDir_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveDir_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveDir_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveDir_Request_type_support_symbol_names_t _MoveDir_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, mover_services, srv, MoveDir_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mover_services, srv, MoveDir_Request)),
  }
};

typedef struct _MoveDir_Request_type_support_data_t
{
  void * data[2];
} _MoveDir_Request_type_support_data_t;

static _MoveDir_Request_type_support_data_t _MoveDir_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveDir_Request_message_typesupport_map = {
  2,
  "mover_services",
  &_MoveDir_Request_message_typesupport_ids.typesupport_identifier[0],
  &_MoveDir_Request_message_typesupport_symbol_names.symbol_name[0],
  &_MoveDir_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveDir_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveDir_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace mover_services

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, mover_services, srv, MoveDir_Request)() {
  return &::mover_services::srv::rosidl_typesupport_c::MoveDir_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "mover_services/srv/detail/move_dir__struct.h"
// already included above
// #include "mover_services/srv/detail/move_dir__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace mover_services
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _MoveDir_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveDir_Response_type_support_ids_t;

static const _MoveDir_Response_type_support_ids_t _MoveDir_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveDir_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveDir_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveDir_Response_type_support_symbol_names_t _MoveDir_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, mover_services, srv, MoveDir_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mover_services, srv, MoveDir_Response)),
  }
};

typedef struct _MoveDir_Response_type_support_data_t
{
  void * data[2];
} _MoveDir_Response_type_support_data_t;

static _MoveDir_Response_type_support_data_t _MoveDir_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveDir_Response_message_typesupport_map = {
  2,
  "mover_services",
  &_MoveDir_Response_message_typesupport_ids.typesupport_identifier[0],
  &_MoveDir_Response_message_typesupport_symbol_names.symbol_name[0],
  &_MoveDir_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveDir_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveDir_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace mover_services

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, mover_services, srv, MoveDir_Response)() {
  return &::mover_services::srv::rosidl_typesupport_c::MoveDir_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "mover_services/srv/detail/move_dir__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace mover_services
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _MoveDir_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveDir_type_support_ids_t;

static const _MoveDir_type_support_ids_t _MoveDir_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveDir_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveDir_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveDir_type_support_symbol_names_t _MoveDir_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, mover_services, srv, MoveDir)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mover_services, srv, MoveDir)),
  }
};

typedef struct _MoveDir_type_support_data_t
{
  void * data[2];
} _MoveDir_type_support_data_t;

static _MoveDir_type_support_data_t _MoveDir_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveDir_service_typesupport_map = {
  2,
  "mover_services",
  &_MoveDir_service_typesupport_ids.typesupport_identifier[0],
  &_MoveDir_service_typesupport_symbol_names.symbol_name[0],
  &_MoveDir_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t MoveDir_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveDir_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace mover_services

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, mover_services, srv, MoveDir)() {
  return &::mover_services::srv::rosidl_typesupport_c::MoveDir_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
