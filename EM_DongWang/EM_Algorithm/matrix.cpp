#include "matrix.h"
#include <math.h>
#include <limits>
#include <iostream>
#include <cstdio>

using namespace std;


Matrix::Matrix() : rows(1), columns(1), rows_filter(0), columns_filter(0) {
	//rows=columns=1;
	data = new double[rows*columns];
}

Matrix::Matrix(size_t _rows, size_t _columns) : rows(_rows), columns(_columns), rows_filter(0), columns_filter(0) {
	if (rows == 0 || columns == 0)
		//throw MatrixException("Invalid Matrix: 0x0");
		cout<<"Invalid Matrix: 0x0"<<endl;
	data = new double[rows*columns];
}

Matrix::Matrix(size_t _rows, size_t _columns, std::vector<double> _data) : rows(_rows), columns(_columns), rows_filter(0), columns_filter(0) {
	if (rows == 0 || columns == 0)
		//throw MatrixException("Invalid Matrix: 0x0");
		cout<<"Invalid Matrix: 0x0"<<endl;
	data = new double[rows*columns];
	for (size_t i = 0; i < rows; i++)
		for (size_t j = 0; j < columns; j++)
			data[i*columns + j] = _data[i*columns + j];	
}

Matrix::Matrix(const Matrix& matrix) {
	rows = matrix.rows;
	columns = matrix.columns;
	rows_filter = matrix.rows_filter;
	columns_filter = matrix.columns_filter;

	data = new double[rows*columns];
	for (size_t i = 0; i < rows; i++)
		for (size_t j = 0; j < columns; j++)
			data[i*columns + j] = matrix.data[i*columns + j];
}

Matrix::Matrix(size_t rc_flg, std::vector<size_t> filter, const Matrix& matrix){
	if (rc_flg==0){//Row filter
		rows = filter.size();
		columns = matrix.columns;
		}
	else{//Column filter
		rows = matrix.rows;
		columns = filter.size();
		}

	rows_filter = matrix.rows_filter;
	columns_filter = matrix.columns_filter;
	
	data = new double[rows*columns];

	if(rc_flg==0){//Row filter
	for (size_t i = 0; i < rows; i++)
		for (size_t j = 0; j < columns; j++)
			data[i*columns + j] = matrix.data[filter[i]*matrix.columns + j];
		}
	else{ //Column filter
		for (size_t i = 0; i < rows; i++)
		for (size_t j = 0; j < columns; j++)
			data[i*columns + j] = matrix.data[i*matrix.columns + filter[j]];
		}
}

size_t Matrix::getRows() const{
	if (rows_filter)
		return rows_filter->size();
	else
		return rows;
	}

size_t Matrix::getColumns()const {
	if (columns_filter)
		return columns_filter->size();
	else 
		return columns;
	}

void Matrix::set(size_t row, size_t column, double value) {
	data[bufferIndex(row, column)]=value;
	}

size_t Matrix::bufferIndex(size_t row, size_t column) const 
{
	if (rows_filter) 
		row = (*rows_filter)[row];
	if (columns_filter)
		column = (*columns_filter)[column];

	return row*columns + column;
}

size_t Matrix::numRows() const
{
	if (rows_filter)
		return rows_filter->size();
	else
		return rows;
}
	
size_t Matrix::numColumns() const
{
	if (columns_filter)
		return columns_filter->size();
	else 
		return columns;
}

Matrix Matrix::operator + (const Matrix& right) const 
{
	size_t columns = numColumns();
	size_t rows = numRows();
	if ((columns != right.numColumns()) || (rows != right.numRows()))
		//throw MatrixException("Number of rows and columns does not match");
		cout<<"Number of rows and columns does not match"<<endl;

	double* d = new double[rows*columns];

	for (size_t i = 0; i < rows; i++)
		for (size_t j = 0; j < columns; j++) 
			d[i*columns + j] = get(i, j) + right.get(i, j);
		
	return Matrix(rows, columns, d);
}

Matrix Matrix::operator - (const Matrix& right) const 
{
	size_t columns = numColumns();
	size_t rows = numRows();
	if ((columns != right.numColumns()) || (rows != right.numRows()))
		//throw MatrixException("Number of rows and columns does not match");
		cout<<"Number of rows and columns does not match"<<endl;

	double* d = new double[rows*columns];

	for (size_t i = 0; i < rows; i++)
		for (size_t j = 0; j < columns; j++) 
			d[i*columns + j] = get(i, j) - right.get(i, j);

	return Matrix(rows, columns, d);
}

Matrix Matrix::operator * (const Matrix& right) const {
	size_t result_rows = numRows();
	size_t result_columns = right.numColumns();
	if (numColumns() != right.numRows())
		//throw MatrixException("Number of rows and columns does not match");
		cout<<"Number of rows and columns does not match"<<endl;

	double* d = new double[result_rows*result_columns];

	for (size_t i = 0; i < result_rows; i++)
		for (size_t j = 0; j < result_columns; j++) {
			d[i*result_columns + j] = 0;
			for (size_t c = 0; c < numColumns(); c++) 
				d[i*result_columns + j] += get(i,c)*right.get(c, j);
		}
	return Matrix(result_rows, result_columns, d);
};

Matrix Matrix::operator ! () const {
	size_t result_rows = numColumns();
	size_t result_columns = numRows();

	double* d = new double[result_rows*result_columns];
	for (size_t i = 0; i < result_columns; i++)
		for (size_t j = 0; j < result_rows; j++)
			d[j*result_columns + i] = get(i, j);

	return Matrix(result_rows, result_columns, d);
}

void Matrix::operator = (const Matrix& right) {
	rows = right.rows;
	columns = right.columns;
	rows_filter = right.rows_filter;
	columns_filter = right.columns_filter;

	data = new double[rows*columns];
	for (size_t i = 0; i < rows; i++)
		for (size_t j = 0; j < columns; j++)
			data[i*columns + j] = right.data[i*columns + j];
}

/**
 * NOTE: This method ignores the row and column filters
 */
void Matrix::operator += (const Matrix& right)
{
	if ((columns != right.columns) || (rows != right.rows))
		//throw MatrixException("Number of rows and columns does not match");
		cout<<"Number of rows and columns does not match"<<endl;

	for (size_t i = 0; i < rows; i++)
		for (size_t j = 0; j < columns; j++) 
			data[i * columns + j] += right.data[i * columns + j];
}

/**
 * NOTE: This method ignores the row and column filters
 */

void Matrix::operator -= (const Matrix& right)
{
	if ((columns != right.columns) || (rows != right.rows))
		//throw MatrixException("Number of rows and columns does not match");
		cout<<"Number of rows and columns does not match"<<endl;

	for (size_t i = 0; i < rows; i++)
		for (size_t j = 0; j < columns; j++) 
			data[i * columns + j] -= right.data[i * columns + j];
}

Matrix Matrix::invert() const 
{
	if (numRows() != numColumns())
		//throw MatrixException("Square matrix required for inversion");
		cout<<"Number of rows and columns does not match"<<endl;

	size_t n = numRows();
	double* d = new double[n*n];
	for (size_t i = 0; i < n; i++)
		for (size_t j = 0; j < n; j++) 
			d[i*n + j] = get(i, j);
 
	for (size_t j = 1; j < n; j++) 
		d[j] /= d[0]; // normalize row 0

	for (size_t i = 1; i < n; i++)  { 
		for (size_t j = i; j < n; j++)  { // do a column of L
			for (size_t k = 0; k < i; k++)  
				d[j*n+i] -= d[j*n+k] * d[k*n+i];
		}

		if (i == n-1) 
			continue;
		
		for (size_t j=i+1; j < n; j++)  {  // do a row of U
			for (size_t k = 0; k < i; k++)
				d[i*n+j] -= d[i*n+k]*d[k*n+j];
			
			d[i*n+j] /= d[i*n+i];
		}
	}

	for ( size_t i = 0; i < n; i++ ) { // invert L
		d[i*n+i] = 1.0 / d[i*n+i];
		for ( size_t j = i + 1; j < n; j++ )  {
			double x = 0.0;
			for (size_t k = i; k < j; k++ ) 
		        x -= d[j*n+k]*d[k*n+i];
			d[j*n+i] = x / d[j*n+j];
		}
	}
	
	for ( size_t i = 0; i < n; i++ )   // invert U
		for ( size_t j = i; j < n; j++ )  {
			if ( i == j ) 
				continue;
			
			double sum = 0.0;
			for ( size_t k = i; k < j; k++ )
				sum += d[k*n+j]*( (i==k) ? 1.0 : d[i*n+k] );
			d[i*n+j] = -sum;
		}
		
	for ( size_t i = 0; i < n; i++ )   // final inversion
		for ( size_t j = 0; j < n; j++ )  {
			double sum = 0.0;
			for ( size_t k = ((i>j)?i:j); k < n; k++ )  
				sum += ((j==k)?1.0:d[j*n+k])*d[k*n+i];
			if ((sum != sum) || fabs(sum) == std::numeric_limits<double>::infinity()) {
				delete d;
				//throw MatrixException("Unable to invert a singular matrix");
				cout<<"Unable to invert a singular matrix"<<endl;
			}
		
			d[j*n+i] = sum;
		}

	return Matrix(n, n, d);
}

double pythag(double a, double b)
{  // Returns the square root of (a*a + b*b)
   // without overflow or destructive underflow
   double p, r, s, t, u;

   t = fabs(a);
   u = fabs(b);

   p = ((t >= u) ? t : u);
   if (p > 0){
       r = ((t <= u) ? t : u);
       r /= p;
       r *= r;
       t = 4.0 + r;

       while (t > 4.0){
            s = r/t;
            u = 1.0 + 2.0*s;
            p = u*p;
            t = s/u;
            r *= t*t;
            t = 4.0 + r;
       } // while (t > 4.0);
   } // End if (p > 0)

   return p;
} // End pythag

double Matrix::eigenvalue() const
{
	if (numRows() != numColumns())
		//throw MatrixException("Eigenvalue is limited to square matrices");
		cout<<"Eigenvalue is limited to square matrices"<<endl;

	int n = numRows();

	double** A = NULL; //Pointer to rows of A Matrix
	double* fv1 = new double[n]; // Temporary vector
	double* wr = new double[n]; // Vector for eigenvalues
	int i, ii, ierr = -1, j, k, l, l1, l2;
	double c, c2, c3, dl1, el1, f, g, h, p, r, s, s2, scale, tst1, tst2;

	A = new double*[n];
	for (i = 0; i < n; i++) {
		A[i] = new double[n];
		for (j = 0; j < n; j++)
			A[i][j] = get(j, i);
	}

	// ======BEGINNING OF TRED1 ===================================

	ii = n - 1;
	for (i = 0; i < ii; i++){
		wr[i] = A[ii][i];
		A[ii][i] = A[i][i];
	}//End for i
	wr[ii] = A[ii][ii]; // Take last assignment out of loop

	for (i = (n - 1); i >= 0; i--) {
		l = i - 1;
		scale = h = 0.0;

		if (l < 0){
			fv1[i] = 0.0;
			continue;
		} // End if (l < 0)

		for (j = 0; j <= l; j++)
			scale += fabs(wr[j]);

		if (scale == 0.0){
			for (j = 0; j <= l; j++){
				wr[j] = A[l][j];
				A[l][j] = A[i][j];
				A[i][j] = 0.0;
			}//End for j

			fv1[i] = 0.0;
			continue;
		} // End if (scale == 0.0)

		for (j = 0; j <= l; j++){
			wr[j] /= scale;
			h += wr[j]*wr[j];
		}//End for j

		f = wr[l];
		g = ((f >= 0) ? -sqrt(h) : sqrt(h));
		fv1[i] = g*scale;
		h -= f*g;
		wr[l] = f - g;

		if (l != 0){

			for (j = 0; j <= l; j++)
				fv1[j] = 0.0;

			for (j = 0; j <= l; j++){
				f = wr[j];
				g = fv1[j] + f*A[j][j];
				for (ii = (j + 1); ii <= l; ii++){
					g += wr[ii]*A[ii][j];
					fv1[ii] += f*A[ii][j];
				} // End for ii
				fv1[j] = g;
			}//End for j

			// Form p

			f = 0.0;
			for (j = 0; j <= l; j++){
				fv1[j] /= h;
				f += fv1[j]*wr[j];
			}//End for j

			h = f/(h*2);

			// Form q

			for (j = 0; j <= l; j++)
				fv1[j] -= h*wr[j];

			// Form reduced A

			for (j = 0; j <= l; j++){
				f = wr[j];
				g = fv1[j];

			   for (ii = j; ii <= l; ii++)
					A[ii][j] -= f*fv1[ii] + g*wr[ii];

			}//End for j

		} // End if (l != 0)

		for (j = 0; j <= l; j++){
			f = wr[j];
			wr[j] = A[l][j];
			A[l][j] = A[i][j];
			A[i][j] = f*scale;
		}//End for j

	}//End for i

	// ======END OF TRED1 =========================================

	// ======BEGINNING OF TQL1 ===================================

	for (i = 1; i < n; i++)
		fv1[i - 1] = fv1[i];

	fv1[n - 1] = tst1 = f = 0.0;

	for (l = 0; l < n; l++){

		j = 0;
		h = fabs(wr[l]) + fabs(fv1[l]);

		tst1 = ((tst1 < h) ? h : tst1);

	   // Look for small sub-diagonal element

		for (k = l; k < n; k++){
			tst2 = tst1 + fabs(fv1[k]);
			if (tst2 == tst1) break; // fv1[n-1] is always 0, so there is no exit through the bottom of the loop
		}//End for k

		if (k != l){
			do {
				if (j == 30){
					ierr = l;
					break;
				} // End if (j == 30)

				j++;

				// Form shift

				l1 = l + 1;
				l2 = l1 + 1;
				g = wr[l];
				p = (wr[l1] - g)/(2.0*fv1[l]);
				r = pythag(p, 1.0);
				scale = ((p >= 0) ? r : -r); // Use scale as a dummy variable
				scale += p;
				wr[l] = fv1[l]/scale;
				dl1 = wr[l1] = fv1[l]*scale;
				h = g - wr[l];

				for (i = l2; i < n; i++)
					wr[i] -= h;

				f += h;

				// q1 transformation

				p = wr[k];
				c2 = c = 1.0;
				el1 = fv1[l1];
				s = 0.0;

				// Look for i = k - 1 until l in steps of -1

				for (i = (k - 1); i >= l; i--){
					c3 = c2;
					c2 = c;
					s2 = s;
					g = c*fv1[i];
					h = c*p;
					r = pythag(p, fv1[i]);
					fv1[i + 1] = s*r;
					s = fv1[i]/r;
					c = p/r;
					p = c*wr[i] - s*g;
					wr[i + 1] = h + s*(c*g + s*wr[i]);
				}//End for i

				p = -s*s2*c3*el1*fv1[l]/dl1;
				fv1[l] = s*p;
				wr[l] = c*p;
				tst2 = tst1 + fabs(fv1[l]);
			} while (tst2 > tst1); // End do-while loop

		} // End if (k != l)

		if (ierr >= 0) //This check required to ensure we break out of for loop too, not just do-while loop
			break;

		p = wr[l] + f;

		// Order eigenvalues

		// For i = l to 1, in steps of -1
		for (i = l; i >= 1; i--){
			if (p >= wr[i - 1])
				break;
			wr[i] = wr[i - 1];
		}//End for i

		wr[i] = p;

	}//End for l

	// ======END OF TQL1 =========================================

	double min = wr[0];
	for (i = 1; i < n; i++)
		if (wr[i] < min)
			min = wr[i];

	for (i = 0; i < n; i++)
		delete [] A[i];
	delete [] A;
	delete [] fv1; //Release the memory allocated to fv1 before ending program
	delete [] wr;
	return min;
}

double Matrix::squareNorm() const {
	double norm = 0;
	for (size_t i = 0; i < numRows(); i++) 
		for (size_t j = 0; j < numColumns(); j++) 
			norm += get(i,j)*get(i,j);
	return norm;
}

size_t Matrix::getMemoryUsage() const {
	return rows*columns*sizeof(double) + sizeof(rows) + sizeof(columns) + sizeof(rows_filter) + sizeof(columns_filter);
}

void Matrix::print() const {
	for (size_t i = 0; i < numRows(); i++) {
		for (size_t j = 0; j < numColumns(); j++) 
			std::cout << get(i, j) << "\t";
		std::cout << std::endl;
	}
}
