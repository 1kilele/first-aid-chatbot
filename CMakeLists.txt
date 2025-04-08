cmake_minimum_required(VERSION 3.10)
project(ChatbotProject)

set(CMAKE_CXX_STANDARD 14)

find_package(pybind11 REQUIRED)

add_library(chatbot_module MODULE chatbot_bindings.cpp)
target_link_libraries(chatbot_module PRIVATE pybind11::module)
