// file_exporter.h
#ifndef FILE_EXPORTER_H
#define FILE_EXPORTER_H

#include <string>
#include "cmos_generator.h"

void export_to_file(const Circuit& circuit, const std::string& filename);

#endif
