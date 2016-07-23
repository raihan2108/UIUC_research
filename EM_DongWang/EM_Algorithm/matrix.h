#ifndef _MATRIX_
#define _MATRIX_

#include <exception>
#include <vector>
#include <fstream>
#include <iostream>
#include <cstdio>
#include <math.h>
#include <time.h>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <algorithm>

//class MatrixException : public std::exception {
//public:
//	MatrixException(std::string msg) : std::exception(msg.c_str()) {}
//};

class Matrix {
private:
	double* data;
	size_t rows;
	size_t columns;

	// Filters allow to choose only a subset of rows or columns to be considered
	std::vector<size_t>* rows_filter;
	std::vector<size_t>* columns_filter;

public:

	Matrix(size_t _rows, size_t _columns);
	Matrix(size_t _rows, size_t _columns, std::vector<double> d);
	Matrix(const Matrix& matrix);
	//Default Constructor-Dong
	Matrix();
	//Filtered Matrix Constructor-Dong
	//rc_flg:0-row filter, rc_flg:1-column filter
	Matrix(size_t rc_flg, std::vector<size_t>  filter, const Matrix& matrix);
	
	~Matrix() {delete [] data;}

	double get(size_t row, size_t column) const {return data[bufferIndex(row, column)];}
	void set(size_t row, size_t column, double value) ;
	size_t getRows()const;
	size_t getColumns()const;
	inline size_t numRows() const; // Returns the filtered number of rows
	inline size_t numColumns() const; // Returns the filtered number of columns

	void setRowsFilter(std::vector<size_t> * filter) {rows_filter = filter;}
	void setColumnsFilter(std::vector<size_t> * filter) {columns_filter = filter;}

	Matrix operator * (const Matrix& right) const;
	Matrix operator + (const Matrix& right) const;
	Matrix operator - (const Matrix& right) const;
	Matrix operator ! () const;

	void operator = (const Matrix& matrix);
	void operator += (const Matrix& matrix);
	void operator -= (const Matrix& matrix);
	
	Matrix invert() const;
	double eigenvalue() const;
	double squareNorm() const;

	size_t getMemoryUsage() const;
	void print() const;

private:

	Matrix(size_t _rows, size_t _columns, double* d) : 
	   rows(_rows), columns(_columns), data(d), rows_filter(0), columns_filter(0) {}

	inline size_t bufferIndex(size_t row, size_t column) const;
};

#endif
