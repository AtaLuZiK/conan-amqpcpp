find_path(AMQPCPP_INCLUDE_DIR NAMES amqpcpp.h PATHS ${CONAN_INCLUDE_DIRS_AMQPCPP})
find_library(AMQPCPP_LIBRARY NAMES amqpcpp PATHS ${CONAN_LIB_DIRS_AMQPCPP})
find_library(AMQPCPPROTATE_LIBRARY NAMES AMQPCPProtate ${CONAN_LIB_DIRS_AMQPCPP})

add_library(amqpcpp INTERFACE IMPORTED)
target_include_directories(amqpcpp INTERFACE ${AMQPCPP_INCLUDE_DIR})
target_link_libraries(amqpcpp INTERFACE ${AMQPCPP_LIBRARY})

mark_as_advanced(AMQPCPP_INCLUDE_DIR AMQPCPP_LIBRARY_DIR AMQPCPP_LIBRARY)

message("** AMQP-CPP found by Conan!")
set(AMQPCPP_FOUND TRUE)
message("   - includes: ${AMQPCPP_INCLUDE_DIR}")
message("   - libraries: ${AMQPCPP_LIBRARY}")
