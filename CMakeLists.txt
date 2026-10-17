cmake_minimum_required(VERSION 3.25)
project(AI_Sign_Translate LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

set(SDL_TESTS OFF CACHE BOOL "" FORCE)
set(SDL_EXAMPLES OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
    SDL3
    GIT_REPOSITORY https://github.com/libsdl-org/SDL.git
    GIT_TAG release-3.2.28
    GIT_SHALLOW TRUE
)
FetchContent_MakeAvailable(SDL3)

find_package(Python3 COMPONENTS Interpreter REQUIRED)

set(VENV_DIR "${CMAKE_CURRENT_SOURCE_DIR}/.venv")

if(WIN32)
    set(VENV_PYTHON "${VENV_DIR}/Scripts/python.exe")
    set(VENV_ACTIVATE "${VENV_DIR}/Scripts/activate.bat")
else()
    set(VENV_PYTHON "${VENV_DIR}/bin/python")
    set(VENV_ACTIVATE "${VENV_DIR}/bin/activate")
endif()

if(NOT EXISTS "${VENV_PYTHON}")
    execute_process(COMMAND "${Python3_EXECUTABLE}" -m venv "${VENV_DIR}")
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt")
    set(REQ_FILE "${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt")
else()
    set(REQ_FILE "${CMAKE_CURRENT_SOURCE_DIR}/requirement.txt")
endif()

execute_process(COMMAND "${VENV_PYTHON}" -m pip install -r "${REQ_FILE}")

if(WIN32)
    file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/activate.bat" "call \"${VENV_ACTIVATE}\"\r\n")
else()
    file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/activate.sh" "#!/usr/bin/env bash\nsource \"${VENV_ACTIVATE}\"\n")
    execute_process(COMMAND chmod +x "${CMAKE_CURRENT_BINARY_DIR}/activate.sh")
endif()

add_executable(ai_sign_translate_ui src/main.cpp)
target_link_libraries(ai_sign_translate_ui PRIVATE SDL3::SDL3)
