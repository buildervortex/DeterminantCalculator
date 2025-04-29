import copy
class MatrixDeterminantCalculator:
    # multiply a given list with the scaler
    def multiplyRow(self, row: list[float], scaler: float) -> list[float]:
        scaledRow = []
        for number in row:
            scaledRow.append(number*scaler)
        return scaledRow

    # returns the difference of given list
    def substractRow(self, row1: list[float], row2: list[float]) -> list[float]:
        subRow = []
        for index in range(0, len(row2)):
            subRow.append(row1[index] - row2[index])
        return subRow

    # Validate the matrix by checking whether it is a square matrix or not
    def isSquareMatrix(self, matrix: list[list[float]]) -> bool:
        rowCount = len(matrix)

        for row in matrix:
            if len(row) != rowCount:
                return False

        return True

    # sort the matrix by swapping the rows to make the diagonal line non zero. move all the pivot column 0's to the bottom to make it easy to create the upper triangle
    def sortPivotPoints(self, matrix: list[list[float]]) -> tuple[int, list[list[float]]]:
        # get the deep copy of the matrix to make the function pure by not altering the inputs
        matrixCopy = copy.deepcopy(matrix)
        sign = 1
        for rowIndex in range(0, len(matrixCopy)):
            if rowIndex == len(matrixCopy) - 1:
                break

            # get the pivot point index for the current row
            pivotIndex = rowIndex

            # check whether the pivot point is zero
            if matrixCopy[rowIndex][pivotIndex] == 0:
                swapped = False
                # if the pivot point is zero, then go through the bottom rows and checks a row that has a non zero element at the pivot index
                for downRowIndex in range(rowIndex+1, len(matrixCopy)):
                    if matrixCopy[downRowIndex][pivotIndex] != 0:
                        # if found a non zero pivot point indexed row, swap that row with current row
                        matrixCopy[rowIndex], matrixCopy[downRowIndex] = matrixCopy[downRowIndex], matrixCopy[rowIndex]
                        # change the sign to keep track of the swap
                        sign *= -1
                        swapped = True
                        break

                # If no non-zero pivot was found in the column, determinant is 0
                if not swapped and rowIndex < len(matrixCopy)-1:
                    # Check if the entire column is zeros
                    all_zeros = True
                    for r in range(rowIndex, len(matrixCopy)):
                        if matrixCopy[r][pivotIndex] != 0:
                            all_zeros = False
                            break

                    if all_zeros:
                        return 0, matrixCopy  # Determinant is 0

        return sign, matrixCopy

    # created the upper triangle by multiplying the rows and subtracting from other rows.
    def createUpperTriangleMatrix(self, matrix: list[list[float]]):
        # get a deep copy of input matrix to make the function pure
        matrixCopy = copy.deepcopy(matrix)
        for rowIndex in range(0, len(matrixCopy)):
            # if this is the last row break the loop because when it comes to last row there is nothing to do
            if rowIndex == len(matrixCopy) - 1:
                break
            # get the main current row pivot point index
            pivotIndex = rowIndex

            # Skip if pivot is zero (this would cause division by zero)
            if abs(matrixCopy[rowIndex][pivotIndex]) < 1e-10:
                continue

            # loop through all the down rows and multiply each row by a scaler to make the pivot index 0
            for downRowIndex in range(rowIndex + 1, len(matrixCopy)):
                # if the row pivot index already 0, then continue to next row below this
                if abs(matrixCopy[downRowIndex][pivotIndex]) < 1e-10:
                    continue

                # calculate the multiplier which makes the current down row pivot index 0
                multiplier = matrixCopy[downRowIndex][pivotIndex] / \
                    matrixCopy[rowIndex][pivotIndex]

                # multiply the root current row with calculated multiplier
                substractor = self.multiplyRow(
                    matrixCopy[rowIndex], multiplier)

                # subtract the substractor from current down row to make its pivot point index 0
                matrixCopy[downRowIndex] = self.substractRow(
                    matrixCopy[downRowIndex], substractor)
        return matrixCopy

    # calculate the determinant of a upper triangle matrix by multiplying all the values in the diagonal
    def determinantOfUpperTriangleMatrix(self, matrix: list[list[float]], sign: int):
        # If sign is 0, return 0 immediately
        if sign == 0:
            return 0

        pivotPoints = []
        determinant = 1

        # loop through the matrix and save all the diagonal numbers in the pivotPoints list
        for rowIndex in range(0, len(matrix)):
            pivotPoints.append(matrix[rowIndex][rowIndex])

        # calculate the multiplier of diagonal line numbers
        for point in pivotPoints:
            determinant *= point

        # multiply the determinant by the sign
        return determinant * sign

    # combine all the above methods to create single point of use
    def calculateMatrixDeterminant(self, matrix: list[list[float]]) -> float:
        if not self.isSquareMatrix(matrix=matrix):
            raise ValueError("Matrix is not a square matrix")

        sign, sortMatrix = self.sortPivotPoints(matrix)

        # If sign is 0, determinant is 0
        if sign == 0:
            return 0

        upperTriangleMatrix = self.createUpperTriangleMatrix(sortMatrix)
        result = self.determinantOfUpperTriangleMatrix(
            upperTriangleMatrix, sign)

        # Round to handle floating point errors, but don't use ceil
        if abs(result - round(result)) < 1e-10:
            return round(result)
        return result
