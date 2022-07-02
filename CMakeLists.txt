cmake_minimum_required( VERSION 3.5.1 )
project( iutils )

if( CMAKE_BUILD_TYPE MATCHES Debug )
    message( "** Using debug mode." )
    add_definitions(-DDEBUG)
    set( CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC" )
    set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -std=gnu++0x" )
else()
    message( "** Using release mode." )
    set( CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC -O3" )
    set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -O3 -std=gnu++0x" )
endif( )

set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)

add_subdirectory(lib) 

