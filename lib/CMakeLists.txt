find_package(PNG REQUIRED)  
add_library(iutils SHARED flow_viz.cpp heatmap_viz.cpp)
target_link_libraries(iutils png16)
