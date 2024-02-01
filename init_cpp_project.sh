#!/usr/bin/env bash

parent_path="$1"
if [ -z "${parent_path}" ]; then
    parent_path="."
fi
cd "${parent_path}" || echo "${parent_path} not dir" && exit

read -rp "Project name[my_project]: " project_name
if [ -z "${project_name}" ]; then
    project_name="my_project"
fi

read -rp "Sub module name[sub_project]: " sub_project_name
if [ -z "${sub_project_name}" ]; then
    sub_project_name="sub_project"
fi

mkdir "cmake"
cat << EOF > cmake/my_useful_funcs.cmake
macro (my_add_target name type)
    # Usage: my_add_target(target_name EXECUTABLE)
    file(GLOB_RECURSE srcs CONFIGURE_DEPENDS src/*.cpp src/*.h)
    if ("\${type}" MATCHES "EXECUTABLE")
        add_executable(\${name} \${srcs})
    else()
        add_library(\${name} \${type} \${srcs})
    endif()
    target_include_directories(\${name} PUBLIC include)
endmacro()

set(SOME_USEFUL_GLOBAL_VAR    ON)
set(ANOTHER_USEFUL_GLOBAL_VAR OFF)
EOF

cat << EOF > CMakeLists.txt
cmake_minimum_required(VERSION 3.10)

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG \${CMAKE_CURRENT_LIST_DIR}/build/bin/debug)    
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE \${CMAKE_CURRENT_LIST_DIR}/build/bin/release)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG \${CMAKE_CURRENT_LIST_DIR}/build/lib/debug)    
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE \${CMAKE_CURRENT_LIST_DIR}/build/lib/release)
set(CMAKE_MODULE_PATH "\${CMAKE_CURRENT_LIST_DIR}/cmake;\${CMAKE_MODULE_PATH}")

project(${project_name} LANGUAGES CXX)

include(my_useful_funcs)

add_subdirectory(${sub_project_name})
EOF

mkdir "${sub_project_name}" && cd "${sub_project_name}" || echo "${sub_project_name} not dir" && exit
directories=(
    "src"
    "include/${sub_project_name}"
)
for dir in "${directories[@]}"; do
    mkdir -p "${dir}"
done

cat << EOF > include/"${sub_project_name}"/my_module.h
#pragma once
namespace ${sub_project_name} {
}
EOF

cat << EOF > src/my_module.cpp
#include "${sub_project_name}/my_module.h"
namespace ${sub_project_name} {
}
EOF

cat << EOF > src/main.cpp
#include "${sub_project_name}/my_module.h"
#include <iostream>
int main() { 
    std::cout << "Hello, World!" << std::endl; 
    return 0; 
}
EOF

cat << EOF > CMakeLists.txt
file(GLOB_RECURSE srcs CONFIGURE_DEPENDS src/*.cpp)
# add_library(${sub_project_name} STATIC \${srcs})
add_executable(${sub_project_name} \${srcs})
target_include_directories(${sub_project_name} PUBLIC include)
# find_package(ExampleLibrary REQUIRED)
# target_link_libraries(${sub_project_name} PRIVATE ExampleLibrary)
EOF